"""Failure-criterion helpers for compressive-positive stress states."""

from __future__ import annotations

from math import cos, radians, sin, sqrt

from .stress import Vector3


def sorted_principal(stresses: Vector3) -> Vector3:
    """Return principal stresses sorted from maximum to minimum."""

    return tuple(sorted(stresses, reverse=True))  # type: ignore[return-value]


def mohr_coulomb_margin(
    stresses: Vector3,
    cohesion: float,
    friction_angle_deg: float,
) -> float:
    """Return a Mohr-Coulomb safety margin.

    Positive values indicate the stress state remains below the criterion.
    Stresses and cohesion must use the same pressure unit.
    """

    if cohesion < 0:
        raise ValueError("cohesion must be non-negative")
    phi = radians(friction_angle_deg)
    sin_phi = sin(phi)
    if abs(1.0 - sin_phi) < 1.0e-12:
        raise ValueError("friction angle is too close to 90 degrees")

    sigma1, _, sigma3 = sorted_principal(stresses)
    multiplier = (1.0 + sin_phi) / (1.0 - sin_phi)
    intercept = 2.0 * cohesion * cos(phi) / (1.0 - sin_phi)
    strength = sigma3 * multiplier + intercept
    return strength - sigma1


def octahedral_shear(stresses: Vector3) -> float:
    """Return octahedral shear stress for principal stresses."""

    sigma1, sigma2, sigma3 = sorted_principal(stresses)
    return sqrt(
        (sigma1 - sigma2) ** 2
        + (sigma2 - sigma3) ** 2
        + (sigma1 - sigma3) ** 2
    ) / 3.0


def mogi_coulomb_margin(
    stresses: Vector3,
    cohesion: float,
    friction_angle_deg: float,
) -> float:
    """Return a linear Mogi-Coulomb safety margin.

    The helper uses the common linear form based on octahedral shear stress and
    the mean of maximum and minimum principal stresses.
    """

    if cohesion < 0:
        raise ValueError("cohesion must be non-negative")
    phi = radians(friction_angle_deg)
    sigma1, sigma2, sigma3 = sorted_principal(stresses)
    sigma_m2 = 0.5 * (sigma1 + sigma3)
    strength = (2.0 * sqrt(2.0) / 3.0) * (cohesion * cos(phi) + sigma_m2 * sin(phi))
    return strength - octahedral_shear((sigma1, sigma2, sigma3))
