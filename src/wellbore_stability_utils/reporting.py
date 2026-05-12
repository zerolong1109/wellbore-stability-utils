"""Markdown reporting helpers."""

from __future__ import annotations

from .envelope import EnvelopeResult
from .models import ProjectSummary, ValidationMetric


def _escape_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def render_validation_table(metrics: tuple[ValidationMetric, ...] | list[ValidationMetric]) -> str:
    """Render validation metrics as a compact Markdown table."""

    lines = ["| Metric | Status | Detail |", "|---|---|---|"]
    for metric in metrics:
        lines.append(
            f"| {_escape_cell(metric.name)} | {_escape_cell(metric.status)} | {_escape_cell(metric.detail)} |"
        )
    return "\n".join(lines)


def render_summary(summary: ProjectSummary, envelope: EnvelopeResult | None = None) -> str:
    """Render a short project summary."""

    lines = [
        f"# {summary.name}",
        "",
        f"- Maintainer: {summary.maintainer}",
        f"- Scope: {summary.scope}",
    ]

    if envelope is not None:
        margin = envelope.margin_to_second
        margin_text = "n/a" if margin is None else f"{margin:.4g}"
        lines.extend(
            [
                f"- Controlling candidate: {envelope.controlling.name}",
                f"- Margin to second candidate: {margin_text}",
            ]
        )

    if summary.metrics:
        lines.extend(["", render_validation_table(summary.metrics)])

    return "\n".join(lines)
