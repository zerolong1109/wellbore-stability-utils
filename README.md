# wellbore-stability-utils

Small Python utilities for organizing wellbore-stability analysis results.

The package focuses on routine tasks that show up around numerical studies:

- ranking candidate results and selecting the controlling envelope value
- converting equivalent density and pressure-gradient units
- normalizing trajectory angles
- rendering compact validation summaries in Markdown

It is intentionally lightweight and has no runtime dependencies outside the Python standard library.

## Installation

```bash
python -m pip install -e .
```

## Example

```python
from wellbore_stability_utils import CandidateResult, EnvelopeAggregator

candidates = [
    CandidateResult("baseline", 1.18, family="example"),
    CandidateResult("weak-plane", 1.31, family="example"),
    CandidateResult("thermal case", 1.24, family="example"),
]

result = EnvelopeAggregator().select(candidates)
print(result.controlling.name)
```

## Run Tests

```bash
python -m unittest discover -s tests
```

## Repository Layout

```text
src/wellbore_stability_utils/   Python package
tests/                          Unit tests
examples/                       Small usage examples
docs/                           Short project notes
```

## License

MIT License. See [LICENSE](LICENSE).
