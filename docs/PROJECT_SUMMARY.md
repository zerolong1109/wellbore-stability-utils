# Project Summary

`wellbore-stability-utils` is a small supporting package for numerical wellbore-stability workflows.

The package is not a complete geomechanics model. It provides reusable utilities for result organization, deterministic candidate ranking, unit conversion, and Markdown reporting.

## Included Components

- `CandidateResult`: typed candidate values with light validation
- `EnvelopeAggregator`: deterministic ranking and envelope selection
- unit helpers for equivalent density and pressure-gradient conversion
- reporting helpers for compact Markdown validation summaries

## Design Goals

- keep the public API small
- avoid external dependencies
- make examples easy to inspect
- keep behavior covered by unit tests
