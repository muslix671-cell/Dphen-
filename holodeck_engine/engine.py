from __future__ import annotations

import json
import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .config import Settings
from .context import ContextLoader, ensure_within, parse_turn_note, require_safe_component
from .models import (
    REACTION_SCHEMA,
    TURN_RESULT_SCHEMA,
    ReactionSeed,
    TurnResult,
    validate_turn_result,
)
from .openai_client import JSONGateway
from .prompts import (
    COMMON_DEVELOPER_PROMPT,
    reaction_user_prompt,
    turn_user_prompt,
)
from .telemetry import (
    UsageRecord,
    gateway_usage_records,
    summarize_usage,
    write_usage_report,
)


@dataclass(frozen=True)
class RunArtifacts:
    turn_dir: Path
    public_log: Path
    private_log: Path
    state_file: Path
    usage_file: Path
    usage_records: tuple[UsageRecord, ...]
    usage_summary: dict[str, object]
    public_output: str


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
        os.replace(temporary_name, path)
    except Exception:
        Path(temporary_name).unlink(missing_ok=True)
        raise


def _append_atomic(path: Path, content: str) -> None:
    previous = path.read_text(encoding="utf-8") if path.is_file() else ""
    separator = "\n" if previous and not previous.endswith("\n") else ""
    _atomic_write(path, previous + separator + content)


def _render_public_events(resident: str, result: TurnResult) -> str:
    lines: list[str] = []
    for event in result.events:
        if event.visibility != "public":
            continue
        if event.kind == "action":
            lines.append(f"*{event.text.strip()}*")
        else:
            lines.append(f"**{resident} :** « {event.text.strip()} »")
    return "\n\n".join(lines)


def _render_private_events(result: TurnResult) -> str:
    lines: list[str] = []
    for event in result.events:
        if event.visibility == "private":
            label = "Pensee" if event.kind == "thought" else "Sensation"
            lines.append(f"**{label} privee :** {event.text.strip()}")
        elif event.kind == "action":
            lines.append(f"*{event.text.strip()}*")
        else:
            lines.append(f"**Parole publique :** « {event.text.strip()} »")
    return "\n\n".join(lines)


class HolodeckEngine:
    def __init__(self, settings: Settings, gateway: JSONGateway):
        self.settings = settings
        self.gateway = gateway
        self.context_loader = ContextLoader(settings)

    def run(self, input_path: Path) -> RunArtifacts:
        usage_start = len(gateway_usage_records(self.gateway))
        request = parse_turn_note(input_path, self.settings.root)
        session_dir = ensure_within(
            self.settings.runtime_root / request.session_id, self.settings.root
        )
        turn_dir = session_dir / "turns" / request.turn_id
        if turn_dir.exists():
            raise FileExistsError(
                f"Le tour {request.turn_id} existe deja. Utilise un nouvel identifiant."
            )

        context = self.context_loader.load(request)
        seed_data = self.gateway.generate(
            schema_name="reaction_seed",
            schema=REACTION_SCHEMA,
            developer_prompt=COMMON_DEVELOPER_PROMPT,
            user_prompt=reaction_user_prompt(request, context),
        )
        seed = ReactionSeed.from_dict(seed_data)

        result_data = self.gateway.generate(
            schema_name="resident_turn",
            schema=TURN_RESULT_SCHEMA,
            developer_prompt=COMMON_DEVELOPER_PROMPT,
            user_prompt=turn_user_prompt(request, context, seed),
        )
        result = TurnResult.from_dict(result_data)
        validate_turn_result(
            result,
            seed.mode,
            speech_required=request.speech_required,
        )

        public_output = _render_public_events(request.resident, result)
        private_output = _render_private_events(result)
        public_log = session_dir / "public.md"
        private_log = session_dir / "private" / f"{request.resident}.md"
        state_file = session_dir / "state" / f"{request.resident}.json"
        usage_file = turn_dir / "usage.json"

        public_entry = (
            f"## Tour {request.turn_id}\n\n"
            f"*{request.scene.strip()}*\n\n"
            f"**Intervention :** {request.intervention.strip()}\n\n"
            f"{public_output}\n"
        )
        private_entry = (
            f"## Tour {request.turn_id}\n\n"
            f"*Repere observable : {request.scene.strip()}*\n\n"
            f"*Intervention entendue : {request.intervention.strip()}*\n\n"
            f"**Mode causal :** `{seed.mode}`\n\n"
            f"{private_output}\n"
        )

        turn_dir.mkdir(parents=True)
        shutil.copy2(request.source_path, turn_dir / "input.md")
        _atomic_write(
            turn_dir / "reaction.json",
            json.dumps(seed_data, ensure_ascii=False, indent=2) + "\n",
        )
        _atomic_write(
            turn_dir / "result.json",
            json.dumps(result_data, ensure_ascii=False, indent=2) + "\n",
        )
        _append_atomic(public_log, public_entry)
        _append_atomic(private_log, private_entry)
        _atomic_write(
            state_file,
            json.dumps(result.state_after.to_dict(), ensure_ascii=False, indent=2) + "\n",
        )
        usage_records = gateway_usage_records(self.gateway)[usage_start:]
        write_usage_report(
            usage_file,
            usage_records,
            metadata={
                "scope": "turn",
                "session": request.session_id,
                "turn": request.turn_id,
                "resident": request.resident,
                "program": request.program,
            },
        )

        return RunArtifacts(
            turn_dir=turn_dir,
            public_log=public_log,
            private_log=private_log,
            state_file=state_file,
            usage_file=usage_file,
            usage_records=usage_records,
            usage_summary=summarize_usage(usage_records),
            public_output=public_output,
        )


def create_input_note(
    settings: Settings,
    *,
    session_id: str,
    resident: str,
    program: str,
    turn_id: str,
) -> Path:
    session_id = require_safe_component(session_id, "session")
    resident = require_safe_component(resident, "resident")
    program = require_safe_component(program, "program")
    turn_id = require_safe_component(turn_id, "turn")

    inbox = settings.runtime_root / session_id / "inbox"
    path = inbox / f"tour_{turn_id}.md"
    if path.exists():
        raise FileExistsError(f"La note existe deja: {path}")

    content = f"""---
resident: {resident}
session: {session_id}
turn: {turn_id}
program: {program}
---

# Tour {turn_id} - {resident}

## Scene observable

Decris uniquement ce que {resident} peut voir ou entendre avant ton intervention.

## Intervention publique

Ecris ici ton geste, ta replique ou ta question.
"""
    _atomic_write(path, content)
    return path


def create_followup_note(
    settings: Settings,
    *,
    request: TurnRequest,
    turn_id: str,
    scene: str,
    intervention: str,
) -> Path:
    turn_id = require_safe_component(turn_id, "turn")
    inbox = settings.runtime_root / request.session_id / "inbox"
    path = inbox / f"tour_{turn_id}.md"
    if path.exists():
        raise FileExistsError(f"La relance existe deja: {path}")

    metadata = [
        "---",
        f"resident: {request.resident}",
        f"session: {request.session_id}",
        f"turn: {turn_id}",
        f"program: {request.program}",
    ]
    if request.context_pack:
        metadata.append(f"context_pack: {request.context_pack}")
    if request.history_from:
        metadata.append(f"history_from: {request.history_from}")
    metadata.extend(
        [
            "---",
            "",
            f"# Relance {turn_id} - {request.resident}",
            "",
            "## Scene observable",
            "",
            scene.strip(),
            "",
            "## Intervention publique",
            "",
            intervention.strip(),
            "",
        ]
    )
    _atomic_write(path, "\n".join(metadata))
    return path
