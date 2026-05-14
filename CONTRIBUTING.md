# Contributing

Contributions are welcome for small, focused improvements.

Good first contributions include:

- documentation fixes
- additional unit tests
- small utility functions with clear inputs and outputs
- examples that make existing APIs easier to understand

## Development Setup

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

## Pull Request Guidelines

- Keep changes focused.
- Add or update tests for behavior changes.
- Avoid adding runtime dependencies unless there is a clear maintenance benefit.
- Prefer explicit units in names and documentation.
- Keep public APIs stable and simple.

## Numerical Changes

For mechanics helpers, include a short reference or derivation note in the docstring or tests. Tests should cover at least one simple analytic or hand-checkable case.
