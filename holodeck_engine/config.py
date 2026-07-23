from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv(path: Path) -> None:
    """Load the small KEY=VALUE subset needed by this project."""
    if not path.is_file():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def discover_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "AGENTS.md").is_file() and (candidate / "docs" / "holodeck").is_dir():
            return candidate
    raise RuntimeError("Impossible de trouver la racine du depot Holodeck.")


@dataclass(frozen=True)
class Settings:
    root: Path
    runtime_root: Path
    model: str = "gpt-5.6-sol"
    reasoning_effort: str = "medium"
    max_output_tokens: int = 5000
    max_public_history_chars: int = 16000
    api_key: str | None = None

    @classmethod
    def load(cls, root: Path | None = None) -> "Settings":
        resolved_root = discover_root(root)
        _load_dotenv(resolved_root / ".env")

        runtime_root = resolved_root / "docs" / "holodeck" / "meta" / "engine" / "runtime"
        return cls(
            root=resolved_root,
            runtime_root=runtime_root,
            model=os.getenv("HOLODECK_MODEL", "gpt-5.6-sol"),
            reasoning_effort=os.getenv("HOLODECK_REASONING_EFFORT", "medium"),
            max_output_tokens=int(os.getenv("HOLODECK_MAX_OUTPUT_TOKENS", "5000")),
            max_public_history_chars=int(
                os.getenv("HOLODECK_MAX_PUBLIC_HISTORY_CHARS", "16000")
            ),
            api_key=os.getenv("OPENAI_API_KEY") or None,
        )

    def require_api_key(self) -> str:
        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY est absente. Ajoute-la a .env ou a ton environnement."
            )
        return self.api_key
