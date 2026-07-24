from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from hashlib import sha256
from dataclasses import dataclass
from pathlib import Path

from .config import Settings
from .context import ContextLoader, ensure_within, parse_turn_note, require_safe_component
from .models import (
    REACTION_SCHEMA,
    SCENE_QUERY_SCHEMA,
    TURN_RESULT_SCHEMA,
    ReactionSeed,
    ResidentState,
    TurnRequest,
    TurnResult,
    validate_turn_result,
)
from .openai_client import JSONGateway
from .prompts import (
    COMMON_DEVELOPER_PROMPT,
    SCENE_QUERY_DEVELOPER_PROMPT,
    reaction_user_prompt,
    scene_query_user_prompt,
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


@dataclass(frozen=True)
class RewindArtifacts:
    turn_id: str
    archive_dir: Path
    input_path: Path


@dataclass(frozen=True)
class SceneQueryArtifacts:
    answer: str
    certainty: str
    query_dir: Path
    usage_records: tuple[UsageRecord, ...]


@dataclass(frozen=True)
class SceneAdjustmentArtifacts:
    scene_file: Path
    audit_file: Path


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


def _render_public_entry(request: TurnRequest, result: TurnResult) -> str:
    return (
        f"## Tour {request.turn_id}\n\n"
        f"*{request.scene.strip()}*\n\n"
        f"**Intervention :** {request.intervention.strip()}\n\n"
        f"{_render_public_events(request.resident, result)}\n"
    )


def _render_private_entry(
    request: TurnRequest,
    seed: ReactionSeed,
    result: TurnResult,
) -> str:
    return (
        f"## Tour {request.turn_id}\n\n"
        f"*Repere observable : {request.scene.strip()}*\n\n"
        f"*Intervention entendue : {request.intervention.strip()}*\n\n"
        f"**Mode causal :** `{seed.mode}`\n\n"
        f"{_render_private_events(result)}\n"
    )


def _turn_sort_key(path: Path) -> tuple[int, int, int, str]:
    match = re.fullmatch(r"(\d+)(?:f(\d*)?)?", path.name)
    if not match:
        return (10**9, 0, 0, path.name)
    base = int(match.group(1))
    suffix = match.group(2)
    if suffix is None:
        return (base, 0, 0, path.name)
    return (base, 1, int(suffix or "1"), path.name)


def _rebuild_session_artifacts(settings: Settings, session_dir: Path) -> None:
    public_entries: list[str] = []
    private_entries: dict[str, list[str]] = {}
    latest_states: dict[str, ResidentState] = {}

    turns_dir = session_dir / "turns"
    for turn_dir in sorted(
        (path for path in turns_dir.iterdir() if path.is_dir()),
        key=_turn_sort_key,
    ):
        input_path = turn_dir / "input.md"
        reaction_path = turn_dir / "reaction.json"
        result_path = turn_dir / "result.json"
        if not all(path.is_file() for path in (input_path, reaction_path, result_path)):
            raise ValueError(f"Tour incomplet pendant la reconstruction: {turn_dir}")

        request = parse_turn_note(input_path, settings.root)
        seed = ReactionSeed.from_dict(
            json.loads(reaction_path.read_text(encoding="utf-8"))
        )
        result = TurnResult.from_dict(
            json.loads(result_path.read_text(encoding="utf-8"))
        )
        public_entries.append(_render_public_entry(request, result))
        private_entries.setdefault(request.resident, []).append(
            _render_private_entry(request, seed, result)
        )
        latest_states[request.resident] = result.state_after

    public_log = session_dir / "public.md"
    if public_entries:
        _atomic_write(public_log, "\n".join(public_entries))
    else:
        public_log.unlink(missing_ok=True)

    private_dir = session_dir / "private"
    if private_dir.is_dir():
        for path in private_dir.glob("*.md"):
            path.unlink()
    for resident, entries in private_entries.items():
        _atomic_write(private_dir / f"{resident}.md", "\n".join(entries))

    state_dir = session_dir / "state"
    if state_dir.is_dir():
        for path in state_dir.glob("*.json"):
            path.unlink()
    for resident, state in latest_states.items():
        _atomic_write(
            state_dir / f"{resident}.json",
            json.dumps(state.to_dict(), ensure_ascii=False, indent=2) + "\n",
        )


def rewind_last_turn(settings: Settings, session_id: str) -> RewindArtifacts:
    session_id = require_safe_component(session_id, "session")
    session_dir = ensure_within(settings.runtime_root / session_id, settings.root)
    turns_dir = ensure_within(session_dir / "turns", settings.root)
    if not turns_dir.is_dir():
        raise ValueError(f"La session {session_id} ne contient aucun tour.")

    turn_dirs = [path for path in turns_dir.iterdir() if path.is_dir()]
    if not turn_dirs:
        raise ValueError(f"La session {session_id} ne contient aucun tour.")
    latest = sorted(turn_dirs, key=_turn_sort_key)[-1]

    source_input = latest / "input.md"
    if not source_input.is_file():
        raise ValueError(f"Le tour {latest.name} ne contient pas son entree.")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    archive_dir = ensure_within(
        session_dir / "replaced" / f"{latest.name}-{timestamp}",
        settings.root,
    )
    archive_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(latest), str(archive_dir))
    _atomic_write(
        archive_dir / "replacement.json",
        json.dumps(
            {
                "turn": latest.name,
                "replaced_at": datetime.now(timezone.utc).isoformat(),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    )

    inbox_path = ensure_within(
        session_dir / "inbox" / f"tour_{latest.name}.md",
        settings.root,
    )
    inbox_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(archive_dir / "input.md", inbox_path)
    _rebuild_session_artifacts(settings, session_dir)

    return RewindArtifacts(
        turn_id=latest.name,
        archive_dir=archive_dir,
        input_path=inbox_path,
    )


def answer_scene_question(
    settings: Settings,
    gateway: JSONGateway,
    *,
    session_id: str,
    question: str,
) -> SceneQueryArtifacts:
    session_id = require_safe_component(session_id, "session")
    question = question.strip()
    if not question:
        raise ValueError("La question sur la scene est vide.")

    session_dir = ensure_within(settings.runtime_root / session_id, settings.root)
    public_log = ensure_within(session_dir / "public.md", settings.root)
    if not public_log.is_file():
        raise ValueError("La session ne contient encore aucune scene publique.")
    public_history = public_log.read_text(encoding="utf-8")
    if len(public_history) > settings.max_public_history_chars:
        public_history = public_history[-settings.max_public_history_chars :]
    scene_file = ensure_within(session_dir / "scene.md", settings.root)
    if scene_file.is_file():
        public_history += (
            "\n\n# AJUSTEMENTS OPERATEUR DE LA SCENE\n"
            + scene_file.read_text(encoding="utf-8")
        )

    usage_start = len(gateway_usage_records(gateway))
    result = gateway.generate(
        schema_name="scene_query",
        schema=SCENE_QUERY_SCHEMA,
        developer_prompt=SCENE_QUERY_DEVELOPER_PROMPT,
        user_prompt=scene_query_user_prompt(public_history, question),
    )
    answer = str(result["answer"]).strip()
    certainty = str(result["certainty"])
    if not answer:
        raise ValueError("La reponse a la question de scene est vide.")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    query_dir = ensure_within(
        session_dir / "queries" / timestamp,
        settings.root,
    )
    query_dir.mkdir(parents=True, exist_ok=False)
    _atomic_write(
        query_dir / "request.json",
        json.dumps(
            {
                "session": session_id,
                "question": question,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    )
    _atomic_write(
        query_dir / "result.json",
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
    )
    usage_records = gateway_usage_records(gateway)[usage_start:]
    write_usage_report(
        query_dir / "usage.json",
        usage_records,
        metadata={
            "scope": "scene_query",
            "session": session_id,
        },
    )
    return SceneQueryArtifacts(
        answer=answer,
        certainty=certainty,
        query_dir=query_dir,
        usage_records=usage_records,
    )


def add_scene_adjustment(
    settings: Settings,
    *,
    session_id: str,
    text: str,
) -> SceneAdjustmentArtifacts:
    session_id = require_safe_component(session_id, "session")
    text = text.strip()
    if not text:
        raise ValueError("L'ajustement de scene est vide.")
    if len(text) > 4000:
        raise ValueError("L'ajustement de scene depasse 4000 caracteres.")

    session_dir = ensure_within(settings.runtime_root / session_id, settings.root)
    if not session_dir.is_dir():
        raise ValueError(f"La session {session_id} n'existe pas.")

    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y%m%dT%H%M%S%fZ")
    scene_file = ensure_within(session_dir / "scene.md", settings.root)
    _append_atomic(
        scene_file,
        f"## Ajustement {timestamp}\n\n{text}\n",
    )

    audit_file = ensure_within(
        session_dir / "adjustments" / f"{timestamp}.json",
        settings.root,
    )
    _atomic_write(
        audit_file,
        json.dumps(
            {
                "session": session_id,
                "created_at": now.isoformat(),
                "text": text,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    )
    return SceneAdjustmentArtifacts(
        scene_file=scene_file,
        audit_file=audit_file,
    )


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
        cache_prefix = context.render_static()

        def cache_key(schema_name: str) -> str:
            context_digest = sha256(cache_prefix.encode("utf-8")).hexdigest()[:12]
            return (
                f"holodeck:{request.resident}:{schema_name}:"
                f"{context_digest}:v1"
            )

        seed_data = self.gateway.generate(
            schema_name="reaction_seed",
            schema=REACTION_SCHEMA,
            developer_prompt=COMMON_DEVELOPER_PROMPT,
            user_prompt=reaction_user_prompt(request, context),
            cache_prefix=cache_prefix,
            prompt_cache_key=cache_key("reaction_seed"),
        )
        seed = ReactionSeed.from_dict(seed_data)

        result_data = self.gateway.generate(
            schema_name="resident_turn",
            schema=TURN_RESULT_SCHEMA,
            developer_prompt=COMMON_DEVELOPER_PROMPT,
            user_prompt=turn_user_prompt(request, context, seed),
            cache_prefix=cache_prefix,
            prompt_cache_key=cache_key("resident_turn"),
        )
        result = TurnResult.from_dict(result_data)
        validate_turn_result(
            result,
            seed.mode,
            speech_required=request.speech_required,
            response_span=seed.response_span,
        )

        public_output = _render_public_events(request.resident, result)
        public_log = session_dir / "public.md"
        private_log = session_dir / "private" / f"{request.resident}.md"
        state_file = session_dir / "state" / f"{request.resident}.json"
        usage_file = turn_dir / "usage.json"

        public_entry = _render_public_entry(request, result)
        private_entry = _render_private_entry(request, seed, result)

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
