"""Envelope-style ranking helpers for candidate results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .models import CandidateResult


@dataclass(frozen=True)
class EnvelopeResult:
    """Deterministic ranking result for a set of candidate outputs."""

    controlling: CandidateResult
    ranked: tuple[CandidateResult, ...]

    @property
    def margin_to_second(self) -> float | None:
        """Return the value gap to the second-ranked candidate."""

        if len(self.ranked) < 2:
            return None
        return self.ranked[0].value - self.ranked[1].value


class EnvelopeAggregator:
    """Rank candidate outputs and select the controlling entry."""

    def __init__(self, *, higher_is_controlling: bool = True) -> None:
        self.higher_is_controlling = higher_is_controlling

    def rank(self, candidates: Sequence[CandidateResult]) -> tuple[CandidateResult, ...]:
        if not candidates:
            raise ValueError("at least one candidate is required")

        direction = -1 if self.higher_is_controlling else 1
        return tuple(
            sorted(
                candidates,
                key=lambda item: (direction * item.value, item.family, item.name),
            )
        )

    def select(self, candidates: Sequence[CandidateResult]) -> EnvelopeResult:
        ranked = self.rank(candidates)
        return EnvelopeResult(controlling=ranked[0], ranked=ranked)
