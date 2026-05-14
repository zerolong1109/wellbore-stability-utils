from wellbore_stability_utils import (
    CandidateResult,
    EnvelopeAggregator,
    ProjectSummary,
    ValidationMetric,
    gcc_to_mpa_per_meter,
    kirsch_wall_stress,
    mohr_coulomb_margin,
    principal_stresses,
    render_summary,
    symmetric_stress,
)


def main() -> None:
    candidates = [
        CandidateResult(name="baseline", value=1.18, family="example"),
        CandidateResult(name="weak-plane", value=1.31, family="example"),
        CandidateResult(name="thermal case", value=1.24, family="example"),
    ]

    envelope = EnvelopeAggregator().select(candidates)
    gradient = gcc_to_mpa_per_meter(envelope.controlling.value)
    wall = kirsch_wall_stress(
        symmetric_stress(xx=45.0, yy=38.0, zz=52.0, xy=2.0),
        mud_pressure=18.0,
        theta_deg=90.0,
    )
    margin = mohr_coulomb_margin(principal_stresses(wall), cohesion=12.0, friction_angle_deg=30.0)

    summary = ProjectSummary(
        name="wellbore-stability-utils",
        maintainer="zerolong1109",
        scope="small utilities for organizing wellbore-stability analysis results",
        metrics=(
            ValidationMetric("unit conversion", "ok", f"{gradient:.5f} MPa/m"),
            ValidationMetric("candidate ranking", "ok", envelope.controlling.name),
            ValidationMetric("baseline wall check", "ok", f"{margin:.3f} margin"),
        ),
    )
    print(render_summary(summary, envelope))


if __name__ == "__main__":
    main()
