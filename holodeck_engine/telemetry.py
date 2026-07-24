from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class UsageRecord:
    schema_name: str
    model: str
    reasoning_effort: str
    duration_seconds: float
    input_tokens: int
    cached_tokens: int
    cache_write_tokens: int
    output_tokens: int
    reasoning_tokens: int
    total_tokens: int

    @classmethod
    def from_response(
        cls,
        *,
        schema_name: str,
        model: str,
        reasoning_effort: str,
        duration_seconds: float,
        response: Any,
    ) -> "UsageRecord":
        usage = getattr(response, "usage", None)
        input_details = getattr(usage, "input_tokens_details", None)
        output_details = getattr(usage, "output_tokens_details", None)
        return cls(
            schema_name=schema_name,
            model=model,
            reasoning_effort=reasoning_effort,
            duration_seconds=round(duration_seconds, 3),
            input_tokens=_integer_field(usage, "input_tokens"),
            cached_tokens=_integer_field(input_details, "cached_tokens"),
            cache_write_tokens=_integer_field(input_details, "cache_write_tokens"),
            output_tokens=_integer_field(usage, "output_tokens"),
            reasoning_tokens=_integer_field(output_details, "reasoning_tokens"),
            total_tokens=_integer_field(usage, "total_tokens"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_name": self.schema_name,
            "model": self.model,
            "reasoning_effort": self.reasoning_effort,
            "duration_seconds": self.duration_seconds,
            "input_tokens": self.input_tokens,
            "cached_tokens": self.cached_tokens,
            "cache_write_tokens": self.cache_write_tokens,
            "output_tokens": self.output_tokens,
            "reasoning_tokens": self.reasoning_tokens,
            "total_tokens": self.total_tokens,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UsageRecord":
        return cls(
            schema_name=str(data["schema_name"]),
            model=str(data["model"]),
            reasoning_effort=str(data["reasoning_effort"]),
            duration_seconds=float(data["duration_seconds"]),
            input_tokens=int(data["input_tokens"]),
            cached_tokens=int(data["cached_tokens"]),
            cache_write_tokens=int(data["cache_write_tokens"]),
            output_tokens=int(data["output_tokens"]),
            reasoning_tokens=int(data["reasoning_tokens"]),
            total_tokens=int(data["total_tokens"]),
        )


def _integer_field(value: Any, name: str) -> int:
    raw = getattr(value, name, 0) if value is not None else 0
    return int(raw or 0)


def gateway_usage_records(gateway: Any) -> tuple[UsageRecord, ...]:
    records = getattr(gateway, "usage_records", ())
    return tuple(record for record in records if isinstance(record, UsageRecord))


def summarize_usage(records: Iterable[UsageRecord]) -> dict[str, Any]:
    materialized = tuple(records)
    totals = _aggregate(materialized)
    return {
        **totals,
        "by_model": _grouped_summary(materialized, "model"),
        "by_schema": _grouped_summary(materialized, "schema_name"),
    }


def _aggregate(records: tuple[UsageRecord, ...]) -> dict[str, Any]:
    input_tokens = sum(record.input_tokens for record in records)
    cached_tokens = sum(record.cached_tokens for record in records)
    cache_hit_rate = round(cached_tokens / input_tokens, 4) if input_tokens else 0.0
    return {
        "calls": len(records),
        "duration_seconds": round(
            sum(record.duration_seconds for record in records),
            3,
        ),
        "input_tokens": input_tokens,
        "cached_tokens": cached_tokens,
        "cache_write_tokens": sum(record.cache_write_tokens for record in records),
        "cache_hit_rate": cache_hit_rate,
        "output_tokens": sum(record.output_tokens for record in records),
        "reasoning_tokens": sum(record.reasoning_tokens for record in records),
        "total_tokens": sum(record.total_tokens for record in records),
    }


def _grouped_summary(
    records: tuple[UsageRecord, ...],
    attribute: str,
) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[UsageRecord]] = {}
    for record in records:
        key = str(getattr(record, attribute))
        groups.setdefault(key, []).append(record)
    return {
        key: _aggregate(tuple(group_records))
        for key, group_records in sorted(groups.items())
    }


def write_usage_report(
    path: Path,
    records: Iterable[UsageRecord],
    *,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    materialized = tuple(records)
    report = {
        "metadata": metadata or {},
        "summary": summarize_usage(materialized),
        "records": [record.to_dict() for record in materialized],
    }
    _atomic_write(
        path,
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
    )
    return report


def load_session_usage(session_dir: Path) -> tuple[UsageRecord, ...]:
    turns_dir = session_dir / "turns"
    report_paths = sorted(turns_dir.glob("*/usage.json"))
    report_paths.extend(sorted(turns_dir.glob("*/followup_usage.json")))
    replaced_dir = session_dir / "replaced"
    report_paths.extend(sorted(replaced_dir.glob("*/usage.json")))
    report_paths.extend(sorted(replaced_dir.glob("*/followup_usage.json")))
    queries_dir = session_dir / "queries"
    report_paths.extend(sorted(queries_dir.glob("*/usage.json")))
    records: list[UsageRecord] = []
    for report_path in report_paths:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        raw_records = report.get("records", [])
        if not isinstance(raw_records, list):
            raise ValueError(f"Rapport d'utilisation invalide: {report_path}")
        records.extend(UsageRecord.from_dict(item) for item in raw_records)
    return tuple(records)


def render_usage_summary(summary: dict[str, Any]) -> str:
    input_tokens = int(summary.get("input_tokens", 0))
    cached_tokens = int(summary.get("cached_tokens", 0))
    cache_percent = (cached_tokens / input_tokens * 100) if input_tokens else 0.0
    rendered = "\n".join(
        [
            "--- Utilisation API ---",
            f"Appels                 : {int(summary.get('calls', 0)):,}",
            f"Duree API              : {float(summary.get('duration_seconds', 0.0)):.2f} s",
            f"Jetons d'entree        : {input_tokens:,}",
            f"  lus en cache         : {cached_tokens:,} ({cache_percent:.1f} %)",
            f"  ecrits en cache      : {int(summary.get('cache_write_tokens', 0)):,}",
            f"Jetons de sortie       : {int(summary.get('output_tokens', 0)):,}",
            f"  dont raisonnement    : {int(summary.get('reasoning_tokens', 0)):,}",
            f"Jetons totaux          : {int(summary.get('total_tokens', 0)):,}",
        ]
    )
    return rendered.replace(",", " ")


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
        os.replace(temporary_name, path)
    except Exception:
        Path(temporary_name).unlink(missing_ok=True)
        raise
