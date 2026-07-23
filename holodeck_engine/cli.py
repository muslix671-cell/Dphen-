from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from dataclasses import replace
from pathlib import Path

from .config import Settings
from .context import (
    ContextLoader,
    ensure_within,
    parse_turn_note,
    require_safe_component,
)
from .engine import HolodeckEngine, create_followup_note, create_input_note
from .models import FOLLOWUP_SCHEMA
from .openai_client import MockJSONGateway, OpenAIJSONGateway
from .prompts import COMMON_DEVELOPER_PROMPT, followup_user_prompt
from .telemetry import (
    gateway_usage_records,
    load_session_usage,
    render_usage_summary,
    summarize_usage,
    write_usage_report,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="holodeck",
        description="Moteur local des residents du Holodeck.",
    )
    parser.add_argument("--root", type=Path, help="Racine du depot Holodeck.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Creer une note de tour dans Obsidian.")
    init.add_argument("--session", required=True)
    init.add_argument("--resident", required=True)
    init.add_argument("--program", default="DPhen")
    init.add_argument("--turn", required=True)

    run = subparsers.add_parser("run", help="Executer les deux portes de generation.")
    run.add_argument("input", type=Path)
    run.add_argument(
        "--mock",
        action="store_true",
        help="Valider le flux sans appel API ni cout.",
    )
    run.add_argument(
        "--effort",
        choices=("low", "medium", "high"),
        help="Remplacer le niveau de raisonnement pour ce lancement.",
    )

    batch = subparsers.add_parser(
        "batch",
        help="Executer une liste ordonnee de tours avec une seule commande.",
    )
    batch.add_argument("manifest", type=Path)
    batch.add_argument(
        "--mock",
        action="store_true",
        help="Valider tout le lot sans appel API ni cout.",
    )
    batch.add_argument(
        "--check",
        action="store_true",
        help="Verifier notes et contextes sans appel API ni ecriture runtime.",
    )
    batch.add_argument(
        "--effort",
        choices=("low", "medium", "high"),
        help="Remplacer le niveau de raisonnement pour tout le lot.",
    )

    usage = subparsers.add_parser(
        "usage",
        help="Produire le rapport d'une sequence terminee.",
    )
    usage.add_argument("--session", required=True)

    subparsers.add_parser("doctor", help="Verifier la configuration locale.")
    return parser


def _doctor(settings: Settings) -> int:
    calibration_dir = (
        settings.root / "docs" / "holodeck" / "meta" / "resident_calibrations"
    )
    calibrated = sorted(
        path.stem
        for path in calibration_dir.glob("*.md")
        if path.stem.lower() != "readme"
    )
    print(f"Depot                 : {settings.root}")
    print(f"Runtime Obsidian      : {settings.runtime_root}")
    print(f"Modele                : {settings.model}")
    print(f"Effort de raisonnement: {settings.reasoning_effort}")
    print(f"Cle API               : {'presente' if settings.api_key else 'absente'}")
    print(
        "SDK OpenAI            : "
        + ("installe" if importlib.util.find_spec("openai") else "absent")
    )
    print(f"Residents calibres    : {', '.join(calibrated) if calibrated else 'aucun'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        settings = Settings.load(args.root)
        if args.command == "doctor":
            return _doctor(settings)

        if args.command == "init":
            path = create_input_note(
                settings,
                session_id=args.session,
                resident=args.resident,
                program=args.program,
                turn_id=args.turn,
            )
            print(path)
            return 0

        if args.command == "usage":
            session_id = require_safe_component(args.session, "session")
            session_dir = ensure_within(
                settings.runtime_root / session_id,
                settings.root,
            )
            records = load_session_usage(session_dir)
            if not records:
                raise ValueError(
                    f"Aucune utilisation API trouvee pour la session {session_id}."
                )
            summary = summarize_usage(records)
            usage_path = session_dir / "usage-summary.json"
            write_usage_report(
                usage_path,
                records,
                metadata={
                    "scope": "session",
                    "session": session_id,
                },
            )
            print(render_usage_summary(summary))
            print(f"Rapport                : {usage_path}")
            return 0

        if args.command == "run":
            if args.effort:
                settings = replace(settings, reasoning_effort=args.effort)
            if args.mock:
                request = parse_turn_note(args.input, settings.root)
                gateway = MockJSONGateway(request.resident)
            else:
                gateway = OpenAIJSONGateway(settings)

            artifacts = HolodeckEngine(settings, gateway).run(args.input)
            print(artifacts.public_output)
            print(f"\nPublic : {artifacts.public_log}")
            print(f"Prive  : {artifacts.private_log}")
            print(f"Etat   : {artifacts.state_file}")
            return 0

        if args.command == "batch":
            manifest_path = ensure_within(args.manifest, settings.root)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            inputs = manifest.get("inputs")
            if not isinstance(inputs, list) or not inputs:
                raise ValueError("Le manifeste batch doit contenir une liste inputs non vide.")

            effort = args.effort or manifest.get("reasoning_effort")
            if effort:
                if effort not in {"low", "medium", "high"}:
                    raise ValueError("reasoning_effort batch doit valoir low, medium ou high.")
                settings = replace(settings, reasoning_effort=effort)

            followup_turns = set(manifest.get("followup_turns", []))
            if not all(isinstance(item, str) for item in followup_turns):
                raise ValueError("followup_turns doit contenir des identifiants texte.")

            followup_max_depth = manifest.get("followup_max_depth", 1)
            if (
                isinstance(followup_max_depth, bool)
                or not isinstance(followup_max_depth, int)
                or followup_max_depth not in {1, 2}
            ):
                raise ValueError("followup_max_depth doit valoir 1 ou 2.")

            followup_max_total = manifest.get("followup_max_total")
            if followup_max_total is not None and (
                isinstance(followup_max_total, bool)
                or not isinstance(followup_max_total, int)
                or followup_max_total < 0
            ):
                raise ValueError(
                    "followup_max_total doit etre un entier positif ou nul."
                )

            director_style = ""
            director_style_path = manifest.get("director_style")
            if director_style_path:
                if not isinstance(director_style_path, str):
                    raise ValueError("director_style doit etre un chemin texte.")
                style_path = ensure_within(settings.root / director_style_path, settings.root)
                director_style = style_path.read_text(encoding="utf-8")

            gateway = None if (args.mock or args.check) else OpenAIJSONGateway(settings)
            followup_total = 0
            for index, raw_input in enumerate(inputs, start=1):
                if not isinstance(raw_input, str):
                    raise ValueError("Chaque entree inputs doit etre un chemin texte.")
                input_path = ensure_within(settings.root / raw_input, settings.root)
                if args.check:
                    request = parse_turn_note(input_path, settings.root)
                    ContextLoader(settings).load(request)
                    print(
                        f"[check {index}/{len(inputs)}] "
                        f"{request.turn_id} {request.resident}"
                    )
                    continue
                if args.mock:
                    request = parse_turn_note(input_path, settings.root)
                    turn_gateway = MockJSONGateway(request.resident)
                else:
                    turn_gateway = gateway

                print(f"\n=== Batch {index}/{len(inputs)} : {input_path.name} ===")
                request = parse_turn_note(input_path, settings.root)
                artifacts = HolodeckEngine(settings, turn_gateway).run(input_path)
                print(artifacts.public_output)

                if request.turn_id not in followup_turns:
                    continue

                if args.mock:
                    print("[mock] Decision de relance ignoree.")
                    continue

                current_request = request
                current_artifacts = artifacts
                for depth in range(1, followup_max_depth + 1):
                    if (
                        followup_max_total is not None
                        and followup_total >= followup_max_total
                    ):
                        print("[relance] Budget global atteint.")
                        break

                    decision_usage_start = len(gateway_usage_records(gateway))
                    decision = gateway.generate(
                        schema_name="followup_decision",
                        schema=FOLLOWUP_SCHEMA,
                        developer_prompt=COMMON_DEVELOPER_PROMPT,
                        user_prompt=followup_user_prompt(
                            current_request,
                            current_artifacts.public_output,
                            director_style,
                            depth=depth,
                            max_depth=followup_max_depth,
                        ),
                    )
                    decision_path = (
                        current_artifacts.turn_dir / "followup_decision.json"
                    )
                    decision_path.write_text(
                        json.dumps(decision, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8",
                    )
                    write_usage_report(
                        current_artifacts.turn_dir / "followup_usage.json",
                        gateway_usage_records(gateway)[decision_usage_start:],
                        metadata={
                            "scope": "followup_decision",
                            "session": current_request.session_id,
                            "turn": current_request.turn_id,
                            "resident": current_request.resident,
                            "program": current_request.program,
                            "depth": depth,
                        },
                    )
                    if not decision["ask_followup"]:
                        print(f"[relance {depth}] Aucune.")
                        break

                    followup_id = (
                        f"{request.turn_id}f"
                        if depth == 1
                        else f"{request.turn_id}f{depth}"
                    )
                    followup_path = create_followup_note(
                        settings,
                        request=current_request,
                        turn_id=followup_id,
                        scene=decision["scene"],
                        intervention=decision["intervention"],
                    )
                    followup_total += 1
                    print(f"[relance {depth}] {decision['reason']}")
                    current_artifacts = HolodeckEngine(settings, gateway).run(
                        followup_path
                    )
                    current_request = parse_turn_note(followup_path, settings.root)
                    print(current_artifacts.public_output)

            if gateway is not None:
                batch_records = gateway_usage_records(gateway)
                batch_summary = summarize_usage(batch_records)
                usage_path = manifest_path.with_name(
                    f"{manifest_path.stem}.usage.json"
                )
                write_usage_report(
                    usage_path,
                    batch_records,
                    metadata={
                        "scope": "batch",
                        "manifest": str(manifest_path.relative_to(settings.root)),
                        "reasoning_effort": settings.reasoning_effort,
                    },
                )
                print(f"\n{render_usage_summary(batch_summary)}")
                print(f"Rapport                : {usage_path}")

            return 0
    except Exception as exc:
        print(f"Erreur: {exc}", file=sys.stderr)
        return 1

    return 1
