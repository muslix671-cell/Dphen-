from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Any


REACTION_MODES = {"reflective", "impulsive", "restrained", "interrupted"}


@dataclass(frozen=True)
class TurnRequest:
    resident: str
    session_id: str
    turn_id: str
    program: str
    scene: str
    intervention: str
    source_path: Path
    context_pack: str | None = None
    speech_required: bool = True
    history_from: str | None = None


@dataclass(frozen=True)
class ReactionSeed:
    mode: str
    trigger: str
    chosen_interpretation: str
    activation: str
    control: str
    immediate_awareness: str
    impulse: str
    response_cost: str
    response_span: str
    public_tendency: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ReactionSeed":
        seed = cls(**data)
        if seed.mode not in REACTION_MODES:
            raise ValueError(f"Mode de reaction inconnu: {seed.mode}")
        return seed


@dataclass(frozen=True)
class TimelineEvent:
    visibility: str
    kind: str
    text: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TimelineEvent":
        event = cls(**data)
        if event.visibility not in {"private", "public"}:
            raise ValueError(f"Visibilite inconnue: {event.visibility}")
        if event.kind not in {"thought", "sensation", "action", "speech"}:
            raise ValueError(f"Type d'evenement inconnu: {event.kind}")
        if not event.text.strip():
            raise ValueError("Un evenement ne peut pas etre vide.")
        if event.visibility == "private" and event.kind not in {"thought", "sensation"}:
            raise ValueError("Un evenement prive doit etre une pensee ou une sensation.")
        if event.visibility == "public" and event.kind not in {"action", "speech"}:
            raise ValueError("Un evenement public doit etre une action ou une parole.")
        return event


@dataclass(frozen=True)
class SocialImpression:
    person: str
    impression: str
    certainty: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SocialImpression":
        return cls(**data)


@dataclass(frozen=True)
class ResidentState:
    emotional_state: str = "Non etabli"
    active_beliefs: list[str] = field(default_factory=list)
    active_misreadings: list[str] = field(default_factory=list)
    social_impressions: list[SocialImpression] = field(default_factory=list)
    unresolved_tensions: list[str] = field(default_factory=list)
    current_goals: list[str] = field(default_factory=list)
    carry_forward: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ResidentState":
        values = dict(data)
        values["social_impressions"] = [
            SocialImpression.from_dict(item) for item in data.get("social_impressions", [])
        ]
        return cls(**values)

    def to_dict(self) -> dict[str, Any]:
        return {
            "emotional_state": self.emotional_state,
            "active_beliefs": self.active_beliefs,
            "active_misreadings": self.active_misreadings,
            "social_impressions": [
                {
                    "person": item.person,
                    "impression": item.impression,
                    "certainty": item.certainty,
                }
                for item in self.social_impressions
            ],
            "unresolved_tensions": self.unresolved_tensions,
            "current_goals": self.current_goals,
            "carry_forward": self.carry_forward,
        }


@dataclass(frozen=True)
class TurnResult:
    events: list[TimelineEvent]
    state_after: ResidentState

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TurnResult":
        return cls(
            events=[TimelineEvent.from_dict(item) for item in data["events"]],
            state_after=ResidentState.from_dict(data["state_after"]),
        )


REACTION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "mode": {
            "type": "string",
            "enum": ["reflective", "impulsive", "restrained", "interrupted"],
        },
        "trigger": {"type": "string"},
        "chosen_interpretation": {"type": "string"},
        "activation": {"type": "string", "enum": ["low", "medium", "high"]},
        "control": {"type": "string", "enum": ["low", "strained", "good"]},
        "immediate_awareness": {
            "type": "string",
            "enum": ["low", "partial", "good"],
        },
        "impulse": {"type": "string"},
        "response_cost": {
            "type": "string",
            "enum": ["none", "narrowed", "abrupt", "incomplete", "misdirected"],
        },
        "response_span": {
            "type": "string",
            "enum": ["minimal", "clipped", "brief", "normal", "extended"],
        },
        "public_tendency": {"type": "string"},
    },
    "required": [
        "mode",
        "trigger",
        "chosen_interpretation",
        "activation",
        "control",
        "immediate_awareness",
        "impulse",
        "response_cost",
        "response_span",
        "public_tendency",
    ],
}


TURN_RESULT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "events": {
            "type": "array",
            "minItems": 2,
            "items": {
                "anyOf": [
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "visibility": {
                                "type": "string",
                                "enum": ["private"],
                            },
                            "kind": {
                                "type": "string",
                                "enum": ["thought"],
                            },
                            "text": {"type": "string"},
                        },
                        "required": ["visibility", "kind", "text"],
                    },
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "visibility": {
                                "type": "string",
                                "enum": ["private"],
                            },
                            "kind": {
                                "type": "string",
                                "enum": ["sensation"],
                            },
                            "text": {"type": "string"},
                        },
                        "required": ["visibility", "kind", "text"],
                    },
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "visibility": {
                                "type": "string",
                                "enum": ["public"],
                            },
                            "kind": {
                                "type": "string",
                                "enum": ["action"],
                            },
                            "text": {"type": "string"},
                        },
                        "required": ["visibility", "kind", "text"],
                    },
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "visibility": {
                                "type": "string",
                                "enum": ["public"],
                            },
                            "kind": {
                                "type": "string",
                                "enum": ["speech"],
                            },
                            "text": {"type": "string"},
                        },
                        "required": ["visibility", "kind", "text"],
                    },
                ],
            },
        },
        "state_after": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "emotional_state": {"type": "string"},
                "active_beliefs": {"type": "array", "items": {"type": "string"}},
                "active_misreadings": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "social_impressions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "person": {"type": "string"},
                            "impression": {"type": "string"},
                            "certainty": {
                                "type": "string",
                                "enum": ["uncertain", "provisional", "reinforced"],
                            },
                        },
                        "required": ["person", "impression", "certainty"],
                    },
                },
                "unresolved_tensions": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "current_goals": {"type": "array", "items": {"type": "string"}},
                "carry_forward": {"type": "string"},
            },
            "required": [
                "emotional_state",
                "active_beliefs",
                "active_misreadings",
                "social_impressions",
                "unresolved_tensions",
                "current_goals",
                "carry_forward",
            ],
        },
    },
    "required": ["events", "state_after"],
}


FOLLOWUP_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "ask_followup": {"type": "boolean"},
        "reason": {"type": "string"},
        "scene": {"type": "string"},
        "intervention": {"type": "string"},
    },
    "required": ["ask_followup", "reason", "scene", "intervention"],
}


SCENE_QUERY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "answer": {"type": "string"},
        "certainty": {
            "type": "string",
            "enum": ["established", "partially_inferred", "unknown"],
        },
    },
    "required": ["answer", "certainty"],
}


def validate_turn_result(
    result: TurnResult,
    mode: str,
    *,
    speech_required: bool = True,
    response_span: str | None = None,
) -> None:
    if not result.events:
        raise ValueError("La chronologie est vide.")

    private_indices = [
        index for index, event in enumerate(result.events) if event.visibility == "private"
    ]
    public_indices = [
        index for index, event in enumerate(result.events) if event.visibility == "public"
    ]
    speech_indices = [
        index
        for index, event in enumerate(result.events)
        if event.visibility == "public" and event.kind == "speech"
    ]

    if not private_indices or not public_indices:
        raise ValueError("Le tour doit contenir du prive et une sortie publique.")
    if speech_required and not speech_indices:
        raise ValueError("Le tour doit contenir au moins une parole publique.")

    if response_span == "minimal":
        expected_speeches = {1} if speech_required else {0, 1}
        if len(speech_indices) not in expected_speeches:
            if speech_required:
                raise ValueError("Une reponse minimale exige une seule prise de parole.")
            raise ValueError(
                "Une reponse minimale silencieuse accepte au plus une prise de parole."
            )
        if speech_indices:
            words = re.findall(r"[\wÀ-ÿ'-]+", result.events[speech_indices[0]].text)
            if not 1 <= len(words) <= 3:
                raise ValueError("Une reponse minimale doit contenir de un a trois mots.")

    first_private = private_indices[0]
    first_public = public_indices[0]

    if mode in {"reflective", "restrained"} and first_private > first_public:
        raise ValueError(f"Le mode {mode} exige une reaction privee avant la parole.")

    if mode in {"impulsive", "interrupted"}:
        if first_public > first_private:
            raise ValueError(f"Le mode {mode} exige une sortie publique avant la pensee tardive.")
        if not any(index > first_private for index in public_indices):
            raise ValueError(f"Le mode {mode} exige une reprise publique apres la pensee tardive.")
