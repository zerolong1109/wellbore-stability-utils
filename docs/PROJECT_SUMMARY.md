# Project Summary

`wellbore-stability-utils` is a supporting package for numerical wellbore-stability workflows.

The package is not a complete geomechanics simulator. It provides reusable utilities for result organization, deterministic candidate ranking, unit conversion, stress-tensor manipulation, baseline failure-criterion checks, and Markdown reporting.

## Included Components

- `CandidateResult`: typed candidate values with light validation
- `EnvelopeAggregator`: deterministic ranking and envelope selection
- unit helpers for equivalent density and pressure-gradient conversion
- stress helpers for symmetric tensors, principal stresses, and borehole-frame rotation
- baseline Kirsch wall-stress helper for circular boreholes
- Mohr-Coulomb and Mogi-Coulomb safety-margin helpers
- weak-plane normal and shear traction resolution
- reporting helpers for compact Markdown validation summaries

## Design Goals

- keep the public API small
- avoid external dependencies
- make examples easy to inspect
- keep behavior covered by unit tests
