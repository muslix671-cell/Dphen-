from __future__ import annotations

import json
from time import perf_counter
from typing import Any, Protocol

from .config import Settings
from .telemetry import UsageRecord


class JSONGateway(Protocol):
    def generate(
        self,
        *,
        schema_name: str,
        schema: dict[str, Any],
        developer_prompt: str,
        user_prompt: str,
        cache_prefix: str | None = None,
        prompt_cache_key: str | None = None,
    ) -> dict[str, Any]: ...


class OpenAIJSONGateway:
    def __init__(self, settings: Settings):
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "Le paquet openai n'est pas installe. Lance: python -m pip install -e ."
            ) from exc

        self.settings = settings
        self.client = OpenAI(api_key=settings.require_api_key(), timeout=120.0)
        self.usage_records: list[UsageRecord] = []

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
        request_input: str | list[dict[str, Any]] = user_prompt
        cache_arguments: dict[str, Any] = {
            "prompt_cache_options": {
                "mode": "explicit",
                "ttl": "30m",
            }
        }
        if cache_prefix:
            request_input = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": cache_prefix,
                            "prompt_cache_breakpoint": {"mode": "explicit"},
                        },
                        {
                            "type": "input_text",
                            "text": user_prompt,
                        },
                    ],
                }
            ]
            if prompt_cache_key:
                cache_arguments["prompt_cache_key"] = prompt_cache_key

        started_at = perf_counter()
        response = self.client.responses.create(
            model=self.settings.model,
            instructions=developer_prompt,
            input=request_input,
            reasoning={"effort": self.settings.reasoning_effort},
            text={
                "format": {
                    "type": "json_schema",
                    "name": schema_name,
                    "strict": True,
                    "schema": schema,
                }
            },
            max_output_tokens=self.settings.max_output_tokens,
            store=False,
            **cache_arguments,
        )
        self.usage_records.append(
            UsageRecord.from_response(
                schema_name=schema_name,
                model=self.settings.model,
                reasoning_effort=self.settings.reasoning_effort,
                duration_seconds=perf_counter() - started_at,
                response=response,
            )
        )
        if getattr(response, "status", None) != "completed":
            details = getattr(response, "incomplete_details", None)
            raise RuntimeError(
                f"La reponse {schema_name} n'est pas complete: {details or response.status}"
            )
        if not response.output_text:
            raise RuntimeError(f"La reponse {schema_name} ne contient aucun texte exploitable.")
        try:
            return json.loads(response.output_text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"La reponse structuree {schema_name} n'est pas un JSON valide."
            ) from exc


class MockJSONGateway:
    """Deterministic local gateway used to validate the full file flow."""

    def __init__(self, resident: str):
        self.resident = resident
        self.usage_records: list[UsageRecord] = []

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
        del schema, developer_prompt, user_prompt, cache_prefix, prompt_cache_key
        if schema_name == "reaction_seed":
            return {
                "mode": "reflective",
                "trigger": "Une question directe dans un cadre encore evaluatif.",
                "chosen_interpretation": "Le directeur veut une reponse situee, pas un expose complet.",
                "activation": "low",
                "control": "good",
                "immediate_awareness": "partial",
                "impulse": "Verifier la premisse avant de repondre.",
                "response_cost": "none",
                "response_span": "brief",
                "public_tendency": "Reponse breve, prudente et legerement reservee.",
            }
        if schema_name == "resident_turn":
            return {
                "events": [
                    {
                        "visibility": "private",
                        "kind": "thought",
                        "text": "Il attend probablement une reponse nette. Reste sur la question.",
                    },
                    {
                        "visibility": "public",
                        "kind": "action",
                        "text": f"{self.resident} prend une seconde avant de repondre.",
                    },
                    {
                        "visibility": "public",
                        "kind": "speech",
                        "text": "Je vais partir de ce que je sais, sans remplir les blancs.",
                    },
                ],
                "state_after": {
                    "emotional_state": "Attentif et reserve.",
                    "active_beliefs": ["Le cadre demeure evaluatif."],
                    "active_misreadings": [],
                    "social_impressions": [
                        {
                            "person": "le directeur",
                            "impression": "Il prefere une reponse situee.",
                            "certainty": "uncertain",
                        }
                    ],
                    "unresolved_tensions": [],
                    "current_goals": ["Repondre sans surinterpreter."],
                    "carry_forward": "Aucune evolution durable etablie.",
                },
            }
        if schema_name == "scene_query":
            return {
                "answer": (
                    f"La position actuelle de {self.resident} n'est pas "
                    "entierement etablie par la chronologie publique."
                ),
                "certainty": "partially_inferred",
            }
        raise ValueError(f"Schema mock inconnu: {schema_name}")
