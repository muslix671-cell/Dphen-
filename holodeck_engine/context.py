from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from .config import Settings
from .models import ResidentState, TurnRequest


SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9._-]+$")


def require_safe_component(value: str, label: str) -> str:
    if not value or not SAFE_COMPONENT.fullmatch(value):
        raise ValueError(
            f"{label} doit contenir seulement lettres ASCII, chiffres, point, tiret ou soulignement."
        )
    return value


def ensure_within(path: Path, root: Path) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"Le chemin sort du depot Holodeck: {resolved}") from exc
    return resolved


def _heading_key(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", ascii_value.lower()).strip()


def parse_turn_note(path: Path, root: Path) -> TurnRequest:
    source_path = ensure_within(path, root)
    text = source_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("La note doit commencer par un frontmatter delimite par ---.")

    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration as exc:
        raise ValueError("Le frontmatter de la note n'est pas ferme.") from exc

    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"Ligne de frontmatter invalide: {line}")
        key, value = line.split(":", 1)
        metadata[key.strip().lower()] = value.strip().strip('"').strip("'")

    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines[end + 1 :]:
        if line.startswith("## "):
            current = _heading_key(line[3:])
            sections[current] = []
        elif current is not None:
            sections[current].append(line)

    def section(*names: str) -> str:
        for name in names:
            value = "\n".join(sections.get(_heading_key(name), [])).strip()
            if value:
                return value
        raise ValueError(f"Section manquante: {names[0]}")

    required = {"resident", "session", "turn", "program"}
    missing = sorted(required - metadata.keys())
    if missing:
        raise ValueError(f"Metadonnees manquantes: {', '.join(missing)}")

    resident = require_safe_component(metadata["resident"], "resident")
    session_id = require_safe_component(metadata["session"], "session")
    turn_id = require_safe_component(metadata["turn"], "turn")
    program = require_safe_component(metadata["program"], "program")
    context_pack = metadata.get("context_pack") or None
    if context_pack is not None:
        context_pack = require_safe_component(context_pack, "context_pack")

    speech_required_value = metadata.get("speech_required", "true").lower()
    if speech_required_value not in {"true", "false"}:
        raise ValueError("speech_required doit valoir true ou false.")
    speech_required = speech_required_value == "true"
    history_from = metadata.get("history_from") or None
    if history_from is not None:
        history_from = require_safe_component(history_from, "history_from")

    scene = section("Scene observable", "Scene")
    intervention = section("Intervention publique", "Intervention")
    placeholder_fragments = (
        "Decris uniquement ce que",
        "Decrire seulement ce que",
        "Ecris ici ton geste",
        "Ecrire ici le geste",
    )
    if any(fragment in scene or fragment in intervention for fragment in placeholder_fragments):
        raise ValueError(
            "La note contient encore le texte indicatif du gabarit. Remplace-le avant le lancement."
        )

    return TurnRequest(
        resident=resident,
        session_id=session_id,
        turn_id=turn_id,
        program=program,
        scene=scene,
        intervention=intervention,
        source_path=source_path,
        context_pack=context_pack,
        speech_required=speech_required,
        history_from=history_from,
    )


@dataclass(frozen=True)
class ContextBundle:
    resident_profile: str
    calibration: str
    program_context: str
    prior_state: ResidentState
    public_history: str

    def render(self) -> str:
        return "\n\n".join(
            [
                "# DOSSIER PUBLIC DU RESIDENT\n" + self.resident_profile,
                "# CALIBRATION PRIVEE DU RESIDENT\n" + self.calibration,
                "# CONTEXTE PUBLIC DU PROGRAMME\n" + self.program_context,
                "# ETAT PRIVE COMPACT AVANT CE TOUR\n"
                + json.dumps(self.prior_state.to_dict(), ensure_ascii=False, indent=2),
                "# HISTORIQUE PUBLIC RECENT\n" + (self.public_history or "Aucun."),
            ]
        )


class ContextLoader:
    def __init__(self, settings: Settings):
        self.settings = settings

    def load(self, request: TurnRequest) -> ContextBundle:
        root = self.settings.root
        if request.context_pack:
            pack_dir = (
                root
                / "docs"
                / "holodeck"
                / "meta"
                / "engine"
                / "context_packs"
                / request.context_pack
            )
            resident_path = ensure_within(pack_dir / "profile.md", root)
            calibration_path = ensure_within(pack_dir / "calibration.md", root)
            program_path = ensure_within(pack_dir / "program.md", root)
        else:
            resident_path = ensure_within(
                root / "docs" / "holodeck" / "residents" / f"{request.resident}.md",
                root,
            )
            calibration_path = ensure_within(
                root
                / "docs"
                / "holodeck"
                / "meta"
                / "resident_calibrations"
                / f"{request.resident}.md",
                root,
            )
            program_path = ensure_within(
                root / "docs" / "holodeck" / "contexts" / f"{request.program}.md",
                root,
            )

        for label, path in (
            ("dossier du resident", resident_path),
            ("calibration du resident", calibration_path),
            ("contexte du programme", program_path),
        ):
            if not path.is_file():
                raise FileNotFoundError(f"{label} introuvable: {path}")

        session_dir = self.settings.runtime_root / request.session_id
        state_path = session_dir / "state" / f"{request.resident}.json"
        public_path = session_dir / "public.md"

        if state_path.is_file():
            prior_state = ResidentState.from_dict(
                json.loads(state_path.read_text(encoding="utf-8"))
            )
        else:
            prior_state = ResidentState()

        public_history = public_path.read_text(encoding="utf-8") if public_path.is_file() else ""
        if request.history_from and public_history:
            marker = f"## Tour {request.history_from}"
            marker_index = public_history.find(marker)
            public_history = (
                public_history[marker_index:] if marker_index >= 0 else ""
            )
        public_history = public_history[-self.settings.max_public_history_chars :]

        return ContextBundle(
            resident_profile=resident_path.read_text(encoding="utf-8"),
            calibration=calibration_path.read_text(encoding="utf-8"),
            program_context=program_path.read_text(encoding="utf-8"),
            prior_state=prior_state,
            public_history=public_history,
        )
