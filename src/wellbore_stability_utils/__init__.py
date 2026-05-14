"""Small utilities for wellbore-stability analysis workflows."""

from .envelope import EnvelopeAggregator, EnvelopeResult
from .failure import (
    mogi_coulomb_margin,
    mohr_coulomb_margin,
    octahedral_shear,
    sorted_principal,
)
from .models import CandidateResult, ProjectSummary, ValidationMetric
from .reporting import render_summary, render_validation_table
from .stress import (
    borehole_basis,
    kirsch_wall_stress,
    principal_stresses,
    rotate_stress_to_borehole,
    symmetric_stress,
)
from .units import gcc_to_mpa_per_meter, mpa_per_meter_to_gcc, normalize_degrees
from .weak_plane import (
    plane_normal_from_dip,
    resolve_traction,
    weak_plane_slip_margin,
)

__all__ = [
    "CandidateResult",
    "EnvelopeAggregator",
    "EnvelopeResult",
    "ProjectSummary",
    "ValidationMetric",
    "borehole_basis",
    "gcc_to_mpa_per_meter",
    "kirsch_wall_stress",
    "mogi_coulomb_margin",
    "mpa_per_meter_to_gcc",
    "mohr_coulomb_margin",
    "normalize_degrees",
    "octahedral_shear",
    "plane_normal_from_dip",
    "principal_stresses",
    "render_summary",
    "render_validation_table",
    "resolve_traction",
    "rotate_stress_to_borehole",
    "sorted_principal",
    "symmetric_stress",
    "weak_plane_slip_margin",
]

__version__ = "0.2.0"
