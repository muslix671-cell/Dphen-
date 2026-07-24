from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
import json
import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from holodeck_engine.cli import main
from holodeck_engine.config import Settings
from holodeck_engine.context import ContextBundle, ContextLoader, parse_turn_note
from holodeck_engine.engine import (
    HolodeckEngine,
    add_scene_adjustment,
    answer_scene_question,
    rewind_last_turn,
)
from holodeck_engine.models import (
    REACTION_SCHEMA,
    TURN_RESULT_SCHEMA,
    ReactionSeed,
    ResidentState,
    TimelineEvent,
    TurnResult,
    validate_turn_result,
)
from holodeck_engine.openai_client import OpenAIJSONGateway
from holodeck_engine.prompts import (
    COMMON_DEVELOPER_PROMPT,
    followup_user_prompt,
    turn_user_prompt,
)
from holodeck_engine.telemetry import UsageRecord, load_session_usage


class FakeGateway:
    def __init__(self) -> None:
        self.usage_records: list[UsageRecord] = []
        self.user_prompts: list[str] = []

    def generate(
        self,
        *,
        schema_name: str,
        schema: dict[str, Any],
        developer_prompt: str,
        user_prompt: str,
        cache_prefix: str | None = None,
        prompt_cache_key: str | None = None,
    ) -> dict[str, Any]:
        self.user_prompts.append(user_prompt)
        del schema, developer_prompt, cache_prefix, prompt_cache_key
        if schema_name == "reaction_seed":
            self.usage_records.append(
                UsageRecord(
                    schema_name=schema_name,
                    model="fake-model",
                    reasoning_effort="medium",
                    duration_seconds=0.1,
                    input_tokens=100,
                    cached_tokens=40,
                    cache_write_tokens=10,
                    output_tokens=20,
                    reasoning_tokens=5,
                    total_tokens=120,
                )
            )
        else:
            self.usage_records.append(
                UsageRecord(
                    schema_name=schema_name,
                    model="fake-model",
                    reasoning_effort="medium",
                    duration_seconds=0.2,
                    input_tokens=120,
                    cached_tokens=60,
                    cache_write_tokens=0,
                    output_tokens=30,
                    reasoning_tokens=10,
                    total_tokens=150,
                )
            )
        if schema_name == "reaction_seed":
            return {
                "mode": "impulsive",
                "trigger": "Une critique touche sa competence.",
                "chosen_interpretation": "Il croit qu'on minimise son travail.",
                "activation": "high",
                "control": "strained",
                "immediate_awareness": "low",
                "impulse": "Contredire tout de suite.",
                "response_cost": "narrowed",
                "response_span": "brief",
                "public_tendency": "Reponse seche, puis precision moins defensive.",
            }
        if schema_name == "scene_query":
            return {
                "answer": (
                    "Adrian se trouve face au directeur; sa position exacte "
                    "n'est pas entierement etablie."
                ),
                "certainty": "partially_inferred",
            }
        return {
            "events": [
                {"visibility": "public", "kind": "speech", "text": "Non. Ce n'est pas exact."},
                {
                    "visibility": "private",
                    "kind": "thought",
                    "text": "Tu as repondu trop vite, Adrian. Il parlait peut-etre du document.",
                },
                {
                    "visibility": "public",
                    "kind": "speech",
                    "text": "Je vais preciser : le probleme est dans le document, pas dans l'intention.",
                },
            ],
            "state_after": {
                "emotional_state": "Irrite, puis plus controle.",
                "active_beliefs": ["Sa competence vient d'etre mise en doute."],
                "active_misreadings": ["Il attribue trop vite la critique a son travail."],
                "social_impressions": [
                    {
                        "person": "le directeur",
                        "impression": "Il teste sa reaction a la critique.",
                        "certainty": "uncertain",
                    }
                ],
                "unresolved_tensions": ["La critique reste irritante."],
                "current_goals": ["Reprendre la precision de l'echange."],
                "carry_forward": "Adrian demeure un peu plus defensif au prochain tour.",
            },
        }


class EngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "AGENTS.md").write_text("test", encoding="utf-8")
        for directory in (
            "docs/holodeck/residents",
            "docs/holodeck/residents/private/Camille",
            "docs/holodeck/meta/resident_calibrations",
            "docs/holodeck/contexts",
        ):
            (self.root / directory).mkdir(parents=True, exist_ok=True)

        (self.root / "docs/holodeck/residents/Adrian.md").write_text(
            "Adrian public", encoding="utf-8"
        )
        (self.root / "docs/holodeck/meta/resident_calibrations/Adrian.md").write_text(
            "Adrian calibration", encoding="utf-8"
        )
        (self.root / "docs/holodeck/contexts/DPhen.md").write_text(
            "DPhen public", encoding="utf-8"
        )
        (self.root / "docs/holodeck/residents/private/Camille/secret.md").write_text(
            "SECRET_DE_CAMILLE", encoding="utf-8"
        )
        self.settings = Settings(
            root=self.root,
            runtime_root=self.root / "docs/holodeck/meta/engine/runtime",
        )
        self.note = self.root / "turn.md"
        self.note.write_text(
            """---
resident: Adrian
session: test-session
turn: 001
program: DPhen
---

## Scene observable

Le directeur croise les bras.

## Intervention publique

Est-ce vraiment ton meilleur travail?
""",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_note_parser(self) -> None:
        request = parse_turn_note(self.note, self.root)
        self.assertEqual(request.resident, "Adrian")
        self.assertEqual(request.turn_id, "001")
        self.assertIn("croise les bras", request.scene)

    def test_turn_schema_only_allows_valid_event_pairs(self) -> None:
        variants = TURN_RESULT_SCHEMA["properties"]["events"]["items"]["anyOf"]
        pairs = {
            (
                variant["properties"]["visibility"]["enum"][0],
                variant["properties"]["kind"]["enum"][0],
            )
            for variant in variants
        }
        self.assertEqual(
            pairs,
            {
                ("private", "thought"),
                ("private", "sensation"),
                ("public", "action"),
                ("public", "speech"),
            },
        )

    def test_template_placeholder_is_rejected(self) -> None:
        note = self.root / "placeholder.md"
        note.write_text(
            """---
resident: Adrian
session: test-session
turn: 002
program: DPhen
---

## Scene observable

Decris uniquement ce que Adrian peut voir.

## Intervention publique

Ecris ici ton geste, ta replique ou ta question.
""",
            encoding="utf-8",
        )
        with self.assertRaises(ValueError):
            parse_turn_note(note, self.root)

    def test_context_never_loads_another_residents_private_file(self) -> None:
        request = parse_turn_note(self.note, self.root)
        rendered = ContextLoader(self.settings).load(request).render()
        self.assertNotIn("SECRET_DE_CAMILLE", rendered)

    def test_context_pack_replaces_cumulative_resident_context(self) -> None:
        pack = (
            self.root
            / "docs"
            / "holodeck"
            / "meta"
            / "engine"
            / "context_packs"
            / "BlindAdrian"
        )
        pack.mkdir(parents=True)
        (pack / "profile.md").write_text("CV AVEUGLE", encoding="utf-8")
        (pack / "calibration.md").write_text("CALIBRATION AVEUGLE", encoding="utf-8")
        (pack / "program.md").write_text("PROGRAMME AVEUGLE", encoding="utf-8")

        packed_note = self.root / "packed.md"
        packed_note.write_text(
            """---
resident: Adrian
session: packed-session
turn: 001
program: DPhen
context_pack: BlindAdrian
---

## Scene observable

Le theatre est vide.

## Intervention publique

Bonjour.
""",
            encoding="utf-8",
        )
        request = parse_turn_note(packed_note, self.root)
        rendered = ContextLoader(self.settings).load(request).render()
        self.assertIn("CV AVEUGLE", rendered)
        self.assertIn("CALIBRATION AVEUGLE", rendered)
        self.assertNotIn("Adrian public", rendered)
        self.assertNotIn("Adrian calibration", rendered)

    def test_silent_turn_can_omit_public_speech(self) -> None:
        silent = TurnResult(
            events=[
                TimelineEvent("private", "thought", "Personne ne vient."),
                TimelineEvent("public", "action", "Adrian consulte l'heure."),
            ],
            state_after=ResidentState(),
        )
        validate_turn_result(silent, "reflective", speech_required=False)
        with self.assertRaises(ValueError):
            validate_turn_result(silent, "reflective")

    def test_history_can_start_at_resident_entry(self) -> None:
        session_dir = self.settings.runtime_root / "history-session"
        session_dir.mkdir(parents=True)
        (session_dir / "public.md").write_text(
            "## Tour 001\n\nSECRET_AVANT_ENTREE\n\n"
            "## Tour 010\n\nCamille entre dans la salle.\n",
            encoding="utf-8",
        )
        note = self.root / "history.md"
        note.write_text(
            """---
resident: Adrian
session: history-session
turn: 011
program: DPhen
history_from: 010
---

## Scene observable

Camille est maintenant assise dans la salle.

## Intervention publique

Bonjour.
""",
            encoding="utf-8",
        )
        request = parse_turn_note(note, self.root)
        rendered = ContextLoader(self.settings).load(request).render()
        self.assertNotIn("SECRET_AVANT_ENTREE", rendered)
        self.assertIn("Camille entre", rendered)

    def test_impulsive_order_is_enforced(self) -> None:
        invalid = TurnResult(
            events=[
                TimelineEvent("private", "thought", "Je reflechis."),
                TimelineEvent("public", "speech", "Je reponds."),
            ],
            state_after=ResidentState(),
        )
        with self.assertRaises(ValueError):
            validate_turn_result(invalid, "impulsive")

    def test_private_content_does_not_enter_public_log(self) -> None:
        artifacts = HolodeckEngine(self.settings, FakeGateway()).run(self.note)
        public = artifacts.public_log.read_text(encoding="utf-8")
        private = artifacts.private_log.read_text(encoding="utf-8")
        state = json.loads(artifacts.state_file.read_text(encoding="utf-8"))
        usage = json.loads(artifacts.usage_file.read_text(encoding="utf-8"))

        self.assertNotIn("Tu as repondu trop vite", public)
        self.assertIn("Tu as repondu trop vite", private)
        self.assertIn("Non. Ce n'est pas exact.", public)
        self.assertEqual(state["active_misreadings"][0], "Il attribue trop vite la critique a son travail.")
        self.assertEqual(usage["summary"]["calls"], 2)
        self.assertEqual(usage["summary"]["input_tokens"], 220)
        self.assertEqual(usage["summary"]["cached_tokens"], 100)
        self.assertEqual(usage["summary"]["cache_write_tokens"], 10)
        self.assertEqual(usage["summary"]["reasoning_tokens"], 15)

    def test_duplicate_turn_is_rejected(self) -> None:
        engine = HolodeckEngine(self.settings, FakeGateway())
        engine.run(self.note)
        with self.assertRaises(FileExistsError):
            engine.run(self.note)

    def test_rewind_archives_last_turn_and_rebuilds_session(self) -> None:
        HolodeckEngine(self.settings, FakeGateway()).run(self.note)
        second_note = self.root / "turn-002.md"
        second_note.write_text(
            self.note.read_text(encoding="utf-8")
            .replace("turn: 001", "turn: 002")
            .replace(
                "Est-ce vraiment ton meilleur travail?",
                "Pourquoi as-tu choisi ce projet?",
            ),
            encoding="utf-8",
        )
        HolodeckEngine(self.settings, FakeGateway()).run(second_note)

        session_dir = self.settings.runtime_root / "test-session"
        self.assertIn(
            "## Tour 002",
            (session_dir / "public.md").read_text(encoding="utf-8"),
        )

        artifacts = rewind_last_turn(self.settings, "test-session")

        self.assertEqual(artifacts.turn_id, "002")
        self.assertTrue((artifacts.archive_dir / "result.json").is_file())
        self.assertTrue((artifacts.archive_dir / "replacement.json").is_file())
        self.assertTrue(artifacts.input_path.is_file())
        self.assertFalse((session_dir / "turns" / "002").exists())
        self.assertNotIn(
            "## Tour 002",
            (session_dir / "public.md").read_text(encoding="utf-8"),
        )
        self.assertNotIn(
            "## Tour 002",
            (session_dir / "private" / "Adrian.md").read_text(encoding="utf-8"),
        )
        self.assertEqual(len(load_session_usage(session_dir)), 4)

    def test_scene_query_does_not_advance_or_modify_resident_state(self) -> None:
        HolodeckEngine(self.settings, FakeGateway()).run(self.note)
        session_dir = self.settings.runtime_root / "test-session"
        public_before = (session_dir / "public.md").read_text(encoding="utf-8")
        private_before = (session_dir / "private" / "Adrian.md").read_text(
            encoding="utf-8"
        )
        state_before = (session_dir / "state" / "Adrian.json").read_text(
            encoding="utf-8"
        )

        artifacts = answer_scene_question(
            self.settings,
            FakeGateway(),
            session_id="test-session",
            question="Ou est Adrian?",
        )

        self.assertEqual(artifacts.certainty, "partially_inferred")
        self.assertIn("position exacte", artifacts.answer)
        self.assertTrue((artifacts.query_dir / "request.json").is_file())
        self.assertTrue((artifacts.query_dir / "result.json").is_file())
        self.assertEqual(
            (session_dir / "public.md").read_text(encoding="utf-8"),
            public_before,
        )
        self.assertEqual(
            (session_dir / "private" / "Adrian.md").read_text(encoding="utf-8"),
            private_before,
        )
        self.assertEqual(
            (session_dir / "state" / "Adrian.json").read_text(encoding="utf-8"),
            state_before,
        )
        self.assertEqual(
            [path.name for path in (session_dir / "turns").iterdir()],
            ["001"],
        )
        self.assertEqual(len(load_session_usage(session_dir)), 3)

    def test_scene_adjustment_is_public_context_without_advancing_turn(self) -> None:
        HolodeckEngine(self.settings, FakeGateway()).run(self.note)
        session_dir = self.settings.runtime_root / "test-session"
        public_before = (session_dir / "public.md").read_text(encoding="utf-8")
        state_before = (session_dir / "state" / "Adrian.json").read_text(
            encoding="utf-8"
        )

        artifacts = add_scene_adjustment(
            self.settings,
            session_id="test-session",
            text=(
                "Deux tableaux blancs se trouvent derriere la causeuse. "
                "Ils portent des traces mal effacees."
            ),
        )

        self.assertTrue(artifacts.scene_file.is_file())
        self.assertTrue(artifacts.audit_file.is_file())
        self.assertIn(
            "Deux tableaux blancs",
            ContextLoader(self.settings)
            .load(parse_turn_note(self.note, self.root))
            .render_dynamic(),
        )
        self.assertEqual(
            (session_dir / "public.md").read_text(encoding="utf-8"),
            public_before,
        )
        self.assertEqual(
            (session_dir / "state" / "Adrian.json").read_text(encoding="utf-8"),
            state_before,
        )
        self.assertEqual(
            [path.name for path in (session_dir / "turns").iterdir()],
            ["001"],
        )

        gateway = FakeGateway()
        answer_scene_question(
            self.settings,
            gateway,
            session_id="test-session",
            question="Qu'y a-t-il derriere la causeuse?",
        )
        self.assertIn("Deux tableaux blancs", gateway.user_prompts[-1])

    def test_session_usage_is_reported_only_when_requested(self) -> None:
        HolodeckEngine(self.settings, FakeGateway()).run(self.note)
        output = StringIO()
        with redirect_stdout(output):
            exit_code = main(
                [
                    "--root",
                    str(self.root),
                    "usage",
                    "--session",
                    "test-session",
                ]
            )

        report_path = (
            self.settings.runtime_root
            / "test-session"
            / "usage-summary.json"
        )
        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(exit_code, 0)
        self.assertIn("--- Utilisation API ---", output.getvalue())
        self.assertEqual(report["summary"]["calls"], 2)
        self.assertEqual(report["summary"]["cached_tokens"], 100)

    def test_common_prompt_protects_neutral_program_openings(self) -> None:
        self.assertIn("ancrage minimal", COMMON_DEVELOPER_PROMPT)
        self.assertIn("un decor inhabituel", COMMON_DEVELOPER_PROMPT)
        self.assertIn("un choix esthetique peut etre gratuit", COMMON_DEVELOPER_PROMPT)
        self.assertIn(
            "une forte activation exigent un indice observable supplementaire",
            COMMON_DEVELOPER_PROMPT,
        )

    def test_second_followup_requires_new_information(self) -> None:
        request = parse_turn_note(self.note, self.root)
        prompt = followup_user_prompt(
            request,
            "Je ne suis pas d'accord.",
            "Stephane pose des questions directes.",
            depth=2,
            max_depth=2,
        )
        self.assertIn("Cette deuxieme relance est exceptionnelle", prompt)
        self.assertIn("element nouveau", prompt)
        self.assertIn("Aucune troisieme relance", prompt)
        self.assertIn("Par defaut, passe a la prochaine question", prompt)

    def test_response_cost_must_reach_public_answer(self) -> None:
        self.assertIn("response_cost", REACTION_SCHEMA["properties"])
        self.assertIn(
            "narrowed",
            REACTION_SCHEMA["properties"]["response_cost"]["enum"],
        )
        self.assertIn(
            "une formulation reellement maladroite",
            COMMON_DEVELOPER_PROMPT,
        )
        self.assertIn(
            "une position qui heurte une valeur fondamentale",
            COMMON_DEVELOPER_PROMPT,
        )
        self.assertIn("un simple desaccord ne suffit pas", COMMON_DEVELOPER_PROMPT)
        self.assertIn(
            "ne compense pas automatiquement par une reponse professionnelle complete",
            COMMON_DEVELOPER_PROMPT,
        )

    def test_low_awareness_does_not_require_a_verbal_thought(self) -> None:
        request = parse_turn_note(self.note, self.root)
        context = ContextLoader(self.settings).load(request)
        seed = ReactionSeed(
            mode="impulsive",
            trigger="Le mot saboter.",
            chosen_interpretation="On soupconne sa loyaute.",
            activation="medium",
            control="strained",
            immediate_awareness="low",
            impulse="Rejeter la premisse.",
            response_cost="narrowed",
            response_span="minimal",
            public_tendency="Un refus immediat.",
        )
        prompt = turn_user_prompt(request, context, seed)
        self.assertIn(
            "ne transforme pas l'interpretation choisie en pensee privee complete",
            prompt,
        )
        self.assertIn("une comprehension tardive", prompt)

    def test_minimal_response_accepts_one_to_three_words(self) -> None:
        minimal = TurnResult(
            events=[
                TimelineEvent("private", "thought", "Je n'ai plus envie d'expliquer."),
                TimelineEvent("public", "action", "Adrian referme son carnet."),
                TimelineEvent("public", "speech", "Pas maintenant."),
            ],
            state_after=ResidentState(),
        )
        validate_turn_result(
            minimal,
            "restrained",
            response_span="minimal",
        )

    def test_minimal_response_rejects_public_explanation(self) -> None:
        explained = TurnResult(
            events=[
                TimelineEvent("private", "thought", "Je vais fermer la discussion."),
                TimelineEvent(
                    "public",
                    "speech",
                    "Non. Je ne veux pas expliquer davantage.",
                ),
            ],
            state_after=ResidentState(),
        )
        with self.assertRaises(ValueError):
            validate_turn_result(
                explained,
                "restrained",
                response_span="minimal",
            )

    def test_minimal_response_can_remain_silent_when_speech_is_optional(self) -> None:
        silent = TurnResult(
            events=[
                TimelineEvent("private", "thought", "Pas besoin de remplir l'attente."),
                TimelineEvent("public", "action", "Camille relit le tableau efface."),
            ],
            state_after=ResidentState(),
        )
        validate_turn_result(
            silent,
            "reflective",
            speech_required=False,
            response_span="minimal",
        )

    def test_context_bundle_separates_stable_and_turn_specific_content(self) -> None:
        context = ContextBundle(
            resident_profile="profil stable",
            calibration="calibration stable",
            program_context="programme stable",
            prior_state=ResidentState(emotional_state="etat variable"),
            public_history="historique variable",
        )

        static = context.render_static()
        dynamic = context.render_dynamic()

        self.assertIn("profil stable", static)
        self.assertIn("calibration stable", static)
        self.assertIn("programme stable", static)
        self.assertNotIn("etat variable", static)
        self.assertNotIn("historique variable", static)
        self.assertIn("etat variable", dynamic)
        self.assertIn("historique variable", dynamic)
        self.assertNotIn("profil stable", dynamic)

    @unittest.skipUnless(importlib.util.find_spec("openai"), "SDK OpenAI absent")
    def test_openai_gateway_uses_responses_structured_output(self) -> None:
        settings = Settings(
            root=self.root,
            runtime_root=self.settings.runtime_root,
            api_key="test-key",
        )
        gateway = OpenAIJSONGateway(settings)
        captured: dict[str, Any] = {}

        class Responses:
            def create(self, **kwargs: Any) -> SimpleNamespace:
                captured.update(kwargs)
                return SimpleNamespace(
                    status="completed",
                    output_text='{"ok": true}',
                    usage=SimpleNamespace(
                        input_tokens=200,
                        input_tokens_details=SimpleNamespace(
                            cached_tokens=120,
                            cache_write_tokens=40,
                        ),
                        output_tokens=50,
                        output_tokens_details=SimpleNamespace(reasoning_tokens=30),
                        total_tokens=250,
                    ),
                )

        gateway.client = SimpleNamespace(responses=Responses())
        result = gateway.generate(
            schema_name="test_schema",
            schema={
                "type": "object",
                "additionalProperties": False,
                "properties": {"ok": {"type": "boolean"}},
                "required": ["ok"],
            },
            developer_prompt="instructions",
            user_prompt="input",
            cache_prefix="stable context",
            prompt_cache_key="holodeck:test",
        )

        self.assertEqual(result, {"ok": True})
        self.assertEqual(captured["model"], "gpt-5.6-sol")
        self.assertEqual(captured["reasoning"], {"effort": "medium"})
        self.assertEqual(captured["text"]["format"]["type"], "json_schema")
        self.assertEqual(
            captured["input"][0]["content"][0]["text"],
            "stable context",
        )
        self.assertEqual(
            captured["input"][0]["content"][0]["prompt_cache_breakpoint"],
            {"mode": "explicit"},
        )
        self.assertEqual(captured["input"][0]["content"][1]["text"], "input")
        self.assertEqual(captured["prompt_cache_key"], "holodeck:test")
        self.assertEqual(
            captured["prompt_cache_options"],
            {"mode": "explicit", "ttl": "30m"},
        )
        self.assertFalse(captured["store"])
        self.assertEqual(len(gateway.usage_records), 1)
        self.assertEqual(gateway.usage_records[0].cached_tokens, 120)
        self.assertEqual(gateway.usage_records[0].cache_write_tokens, 40)
        self.assertEqual(gateway.usage_records[0].reasoning_tokens, 30)

        captured.clear()
        gateway.generate(
            schema_name="test_schema",
            schema={
                "type": "object",
                "additionalProperties": False,
                "properties": {"ok": {"type": "boolean"}},
                "required": ["ok"],
            },
            developer_prompt="instructions",
            user_prompt="dynamic only",
        )
        self.assertEqual(captured["input"], "dynamic only")
        self.assertEqual(
            captured["prompt_cache_options"],
            {"mode": "explicit", "ttl": "30m"},
        )
        self.assertNotIn("prompt_cache_key", captured)


if __name__ == "__main__":
    unittest.main()
