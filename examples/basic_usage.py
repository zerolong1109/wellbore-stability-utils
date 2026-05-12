from wellbore_stability_utils import (
    CandidateResult,
    EnvelopeAggregator,
    ProjectSummary,
    ValidationMetric,
    gcc_to_mpa_per_meter,
    render_summary,
)


def main() -> None:
    candidates = [
        CandidateResult(name="baseline", value=1.18, family="example"),
        CandidateResult(name="weak-plane", value=1.31, family="example"),
        CandidateResult(name="thermal case", value=1.24, family="example"),
    ]

    envelope = EnvelopeAggregator().select(candidates)
    gradient = gcc_to_mpa_per_meter(envelope.controlling.value)

    summary = ProjectSummary(
        name="wellbore-stability-utils",
        maintainer="zerolong1109",
        scope="small utilities for organizing wellbore-stability analysis results",
        metrics=(
            ValidationMetric("unit conversion", "ok", f"{gradient:.5f} MPa/m"),
            ValidationMetric("candidate ranking", "ok", envelope.controlling.name),
        ),
    )
    print(render_summary(summary, envelope))


if __name__ == "__main__":
    main()
