"""Small utilities for wellbore-stability analysis workflows."""

from .envelope import EnvelopeAggregator, EnvelopeResult
from .models import CandidateResult, ProjectSummary, ValidationMetric
from .reporting import render_summary, render_validation_table
from .units import gcc_to_mpa_per_meter, mpa_per_meter_to_gcc, normalize_degrees

__all__ = [
    "CandidateResult",
    "EnvelopeAggregator",
    "EnvelopeResult",
    "ProjectSummary",
    "ValidationMetric",
    "gcc_to_mpa_per_meter",
    "mpa_per_meter_to_gcc",
    "normalize_degrees",
    "render_summary",
    "render_validation_table",
]

__version__ = "0.1.0"
