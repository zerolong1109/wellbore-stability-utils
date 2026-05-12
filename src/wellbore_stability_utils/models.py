"""Typed data models used by the utility functions."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from typing import Mapping


def _require_text(value: str, field_name: str) -> str:
    text = value.strip()
    if not text:
        raise ValueError(f"{field_name} must not be empty")
    return text


@dataclass(frozen=True)
class CandidateResult:
    """A named candidate value used in envelope-style comparisons."""

    name: str
    value: float
    family: str = "general"
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _require_text(self.name, "name"))
        object.__setattr__(self, "family", _require_text(self.family, "family"))
        if not isfinite(self.value):
            raise ValueError("value must be finite")


@dataclass(frozen=True)
class ValidationMetric:
    """One validation or release-readiness metric."""

    name: str
    status: str
    detail: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _require_text(self.name, "name"))
        object.__setattr__(self, "status", _require_text(self.status, "status"))
        object.__setattr__(self, "detail", _require_text(self.detail, "detail"))


@dataclass(frozen=True)
class ProjectSummary:
    """Compact metadata for generated project summaries."""

    name: str
    maintainer: str
    scope: str
    metrics: tuple[ValidationMetric, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _require_text(self.name, "name"))
        object.__setattr__(self, "maintainer", _require_text(self.maintainer, "maintainer"))
        object.__setattr__(self, "scope", _require_text(self.scope, "scope"))
