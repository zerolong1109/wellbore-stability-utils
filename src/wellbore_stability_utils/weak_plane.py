"""Weak-plane traction and slip-margin utilities."""

from __future__ import annotations

from math import radians, sin, cos, sqrt, tan

from .stress import Matrix3, Vector3, mat_vec_mul, normalize


def plane_normal_from_dip(dip_deg: float, dip_direction_deg: float) -> Vector3:
    """Return a unit normal for a plane from dip and dip direction.

    Coordinates are right-handed with z positive upward. Dip is measured from
    horizontal, and dip direction is measured in the x-y plane from +x toward
    +y. The returned pole is the upward-facing normal.
    """

    dip = radians(dip_deg)
    direction = radians(dip_direction_deg)
    return normalize(
        (
            -sin(dip) * cos(direction),
            -sin(dip) * sin(direction),
            cos(dip),
        )
    )


def resolve_traction(stress: Matrix3, normal: Vector3) -> tuple[float, float, Vector3]:
    """Resolve normal stress and shear traction on a plane."""

    n = normalize(normal)
    traction = mat_vec_mul(stress, n)
    normal_stress = traction[0] * n[0] + traction[1] * n[1] + traction[2] * n[2]
    shear = (
        traction[0] - normal_stress * n[0],
        traction[1] - normal_stress * n[1],
        traction[2] - normal_stress * n[2],
    )
    shear_magnitude = sqrt(shear[0] ** 2 + shear[1] ** 2 + shear[2] ** 2)
    return normal_stress, shear_magnitude, shear


def weak_plane_slip_margin(
    stress: Matrix3,
    normal: Vector3,
    cohesion: float,
    friction_angle_deg: float,
) -> float:
    """Return a Coulomb slip margin for a known plane orientation."""

    if cohesion < 0:
        raise ValueError("cohesion must be non-negative")
    normal_stress, shear, _ = resolve_traction(stress, normal)
    strength = cohesion + normal_stress * tan(radians(friction_angle_deg))
    return strength - shear
