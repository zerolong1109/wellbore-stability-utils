"""Stress-tensor helpers for wellbore-stability calculations.

The functions in this module use a compressive-positive convention and plain
Python tuples so they can be reused in lightweight notebooks and scripts.
"""

from __future__ import annotations

from math import acos, cos, pi, radians, sin, sqrt

Vector3 = tuple[float, float, float]
Matrix3 = tuple[Vector3, Vector3, Vector3]


def _dot(a: Vector3, b: Vector3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a: Vector3, b: Vector3) -> Vector3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _norm(v: Vector3) -> float:
    return sqrt(_dot(v, v))


def normalize(v: Vector3) -> Vector3:
    """Return a unit-length copy of a 3D vector."""

    length = _norm(v)
    if length == 0.0:
        raise ValueError("cannot normalize a zero vector")
    return (v[0] / length, v[1] / length, v[2] / length)


def symmetric_stress(
    xx: float,
    yy: float,
    zz: float,
    xy: float = 0.0,
    xz: float = 0.0,
    yz: float = 0.0,
) -> Matrix3:
    """Build a symmetric 3x3 stress tensor."""

    return ((xx, xy, xz), (xy, yy, yz), (xz, yz, zz))


def mat_vec_mul(matrix: Matrix3, vector: Vector3) -> Vector3:
    """Multiply a 3x3 matrix by a 3D vector."""

    return (
        _dot(matrix[0], vector),
        _dot(matrix[1], vector),
        _dot(matrix[2], vector),
    )


def mat_mul(left: Matrix3, right: Matrix3) -> Matrix3:
    """Multiply two 3x3 matrices."""

    cols = transpose(right)
    return tuple(
        tuple(_dot(row, col) for col in cols) for row in left
    )  # type: ignore[return-value]


def transpose(matrix: Matrix3) -> Matrix3:
    """Transpose a 3x3 matrix."""

    return (
        (matrix[0][0], matrix[1][0], matrix[2][0]),
        (matrix[0][1], matrix[1][1], matrix[2][1]),
        (matrix[0][2], matrix[1][2], matrix[2][2]),
    )


def borehole_basis(inclination_deg: float, azimuth_deg: float) -> Matrix3:
    """Return local borehole basis vectors as rows.

    Inclination is measured from the global vertical z-axis. Azimuth is measured
    in the global x-y plane from +x toward +y. The third basis vector is aligned
    with the borehole axis.
    """

    inc = radians(inclination_deg)
    azi = radians(azimuth_deg)
    axis = normalize((sin(inc) * cos(azi), sin(inc) * sin(azi), cos(inc)))

    vertical = (0.0, 0.0, 1.0)
    if abs(_dot(axis, vertical)) > 0.999999:
        local_x = (1.0, 0.0, 0.0)
    else:
        local_x = normalize(_cross(vertical, axis))
    local_y = normalize(_cross(axis, local_x))
    return (local_x, local_y, axis)


def rotate_stress_to_borehole(
    stress: Matrix3,
    inclination_deg: float,
    azimuth_deg: float,
) -> Matrix3:
    """Rotate a global stress tensor into the local borehole coordinate frame."""

    basis = borehole_basis(inclination_deg, azimuth_deg)
    return mat_mul(mat_mul(basis, stress), transpose(basis))


def principal_stresses(stress: Matrix3) -> Vector3:
    """Return principal stresses sorted from maximum to minimum.

    The implementation follows the closed-form eigenvalue method for real
    symmetric 3x3 matrices.
    """

    a11, a12, a13 = stress[0]
    _, a22, a23 = stress[1]
    _, _, a33 = stress[2]
    p1 = a12 * a12 + a13 * a13 + a23 * a23

    if p1 == 0.0:
        return tuple(sorted((a11, a22, a33), reverse=True))  # type: ignore[return-value]

    q = (a11 + a22 + a33) / 3.0
    p2 = (
        (a11 - q) * (a11 - q)
        + (a22 - q) * (a22 - q)
        + (a33 - q) * (a33 - q)
        + 2.0 * p1
    )
    p = sqrt(p2 / 6.0)
    shifted = (
        ((a11 - q) / p, a12 / p, a13 / p),
        (a12 / p, (a22 - q) / p, a23 / p),
        (a13 / p, a23 / p, (a33 - q) / p),
    )
    r = _det3(shifted) / 2.0
    r = max(-1.0, min(1.0, r))
    phi = acos(r) / 3.0

    eig1 = q + 2.0 * p * cos(phi)
    eig3 = q + 2.0 * p * cos(phi + 2.0 * pi / 3.0)
    eig2 = 3.0 * q - eig1 - eig3
    return tuple(sorted((eig1, eig2, eig3), reverse=True))  # type: ignore[return-value]


def kirsch_wall_stress(
    local_stress: Matrix3,
    mud_pressure: float,
    theta_deg: float,
    poisson_ratio: float = 0.25,
) -> Matrix3:
    """Compute the elastic wall stress state for a circular borehole.

    The input stress tensor must already be expressed in the borehole frame,
    with local z aligned to the borehole axis. The returned tensor is expressed
    in local cylindrical coordinates at the borehole wall: radial, tangential,
    axial.
    """

    sx, sy, sz = local_stress[0][0], local_stress[1][1], local_stress[2][2]
    txy, txz, tyz = local_stress[0][1], local_stress[0][2], local_stress[1][2]

    theta = radians(theta_deg)
    cos2 = cos(2.0 * theta)
    sin2 = sin(2.0 * theta)
    sin1 = sin(theta)
    cos1 = cos(theta)

    radial = mud_pressure
    tangential = sx + sy - 2.0 * (sx - sy) * cos2 - 4.0 * txy * sin2 - mud_pressure
    axial = sz - 2.0 * poisson_ratio * ((sx - sy) * cos2 + 2.0 * txy * sin2)
    shear_tangential_axial = 2.0 * (-txz * sin1 + tyz * cos1)

    return (
        (radial, 0.0, 0.0),
        (0.0, tangential, shear_tangential_axial),
        (0.0, shear_tangential_axial, axial),
    )


def _det3(matrix: Matrix3) -> float:
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
