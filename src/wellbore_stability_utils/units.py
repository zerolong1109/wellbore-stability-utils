"""Unit helpers commonly used in wellbore-stability calculations."""

from __future__ import annotations

STANDARD_GRAVITY = 9.80665
GCC_TO_KG_PER_M3 = 1000.0
PA_TO_MPA = 1.0e-6


def gcc_to_mpa_per_meter(density_gcc: float) -> float:
    """Convert equivalent density in g/cm^3 to pressure gradient in MPa/m."""

    if density_gcc < 0:
        raise ValueError("density_gcc must be non-negative")
    return density_gcc * GCC_TO_KG_PER_M3 * STANDARD_GRAVITY * PA_TO_MPA


def mpa_per_meter_to_gcc(gradient_mpa_per_m: float) -> float:
    """Convert pressure gradient in MPa/m to equivalent density in g/cm^3."""

    if gradient_mpa_per_m < 0:
        raise ValueError("gradient_mpa_per_m must be non-negative")
    return gradient_mpa_per_m / (GCC_TO_KG_PER_M3 * STANDARD_GRAVITY * PA_TO_MPA)


def normalize_degrees(angle_deg: float) -> float:
    """Normalize an angle to the half-open interval [0, 360)."""

    return angle_deg % 360.0
