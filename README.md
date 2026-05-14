# wellbore-stability-utils

Small Python utilities and baseline mechanics helpers for wellbore-stability
analysis.

[![CI](https://github.com/zerolong1109/wellbore-stability-utils/actions/workflows/ci.yml/badge.svg)](https://github.com/zerolong1109/wellbore-stability-utils/actions/workflows/ci.yml)

The package focuses on routine tasks that show up around numerical studies:

- ranking candidate results and selecting the controlling envelope value
- converting equivalent density and pressure-gradient units
- normalizing trajectory angles
- rotating stress tensors into a borehole coordinate frame
- evaluating simple Kirsch wall stresses
- computing Mohr-Coulomb and Mogi-Coulomb safety margins
- resolving normal and shear traction on weak planes
- rendering compact validation summaries in Markdown

It is intentionally lightweight and has no runtime dependencies outside the Python standard library.

## Project Status

This is an actively maintained public utility package for a specialized
scientific and engineering workflow. The current scope is deliberately small:
well-tested baseline mechanics helpers, result-ranking utilities, and reporting
helpers that can be reused in scripts, notebooks, and validation pipelines.

The maintainer handles API design, implementation, tests, issue triage, release
notes, and repository maintenance.

## Installation

```bash
python -m pip install -e .
```

## Example

```python
from wellbore_stability_utils import (
    CandidateResult,
    EnvelopeAggregator,
    kirsch_wall_stress,
    mohr_coulomb_margin,
    principal_stresses,
    symmetric_stress,
)

candidates = [
    CandidateResult("baseline", 1.18, family="example"),
    CandidateResult("weak-plane", 1.31, family="example"),
    CandidateResult("thermal case", 1.24, family="example"),
]

result = EnvelopeAggregator().select(candidates)
print(result.controlling.name)

far_field = symmetric_stress(xx=45.0, yy=38.0, zz=52.0, xy=2.0)
wall = kirsch_wall_stress(far_field, mud_pressure=18.0, theta_deg=90.0)
margin = mohr_coulomb_margin(principal_stresses(wall), cohesion=12.0, friction_angle_deg=30.0)
print(round(margin, 3))
```

## Run Tests

```bash
python -m unittest discover -s tests
```

## Maintenance

- Issues and pull requests are welcome for bug reports, documentation fixes, and small utility additions.
- New numerical helpers should include unit tests and a short example when useful.
- Security issues should be reported according to [SECURITY.md](SECURITY.md).
- Contributor guidance is in [CONTRIBUTING.md](CONTRIBUTING.md).

## Repository Layout

```text
src/wellbore_stability_utils/   Python package
tests/                          Unit tests
examples/                       Small usage examples
docs/                           Short project notes
```

## License

MIT License. See [LICENSE](LICENSE).
