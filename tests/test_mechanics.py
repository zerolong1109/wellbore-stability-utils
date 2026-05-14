from math import sqrt
from unittest import TestCase

from wellbore_stability_utils import (
    kirsch_wall_stress,
    mogi_coulomb_margin,
    mohr_coulomb_margin,
    octahedral_shear,
    plane_normal_from_dip,
    principal_stresses,
    resolve_traction,
    rotate_stress_to_borehole,
    symmetric_stress,
    weak_plane_slip_margin,
)


class StressHelperTests(TestCase):
    def test_principal_stresses_for_diagonal_tensor(self) -> None:
        stress = symmetric_stress(xx=10.0, yy=30.0, zz=20.0)

        self.assertEqual(principal_stresses(stress), (30.0, 20.0, 10.0))

    def test_vertical_borehole_rotation_keeps_global_axes(self) -> None:
        stress = symmetric_stress(xx=10.0, yy=20.0, zz=30.0)

        self.assertEqual(rotate_stress_to_borehole(stress, 0.0, 0.0), stress)

    def test_kirsch_wall_stress_under_equal_horizontal_stress(self) -> None:
        stress = symmetric_stress(xx=10.0, yy=10.0, zz=12.0)
        wall = kirsch_wall_stress(stress, mud_pressure=3.0, theta_deg=45.0)

        self.assertAlmostEqual(wall[0][0], 3.0)
        self.assertAlmostEqual(wall[1][1], 17.0)
        self.assertAlmostEqual(wall[2][2], 12.0)


class FailureCriterionTests(TestCase):
    def test_mohr_coulomb_margin_is_positive_for_stable_example(self) -> None:
        margin = mohr_coulomb_margin((30.0, 20.0, 10.0), cohesion=10.0, friction_angle_deg=30.0)

        self.assertGreater(margin, 0.0)

    def test_octahedral_shear_matches_manual_value(self) -> None:
        value = octahedral_shear((30.0, 20.0, 10.0))

        self.assertAlmostEqual(value, sqrt(600.0) / 3.0)

    def test_mogi_coulomb_margin_returns_finite_value(self) -> None:
        margin = mogi_coulomb_margin((30.0, 20.0, 10.0), cohesion=10.0, friction_angle_deg=30.0)

        self.assertGreater(margin, 0.0)


class WeakPlaneTests(TestCase):
    def test_horizontal_plane_normal_points_upward(self) -> None:
        self.assertEqual(plane_normal_from_dip(0.0, 0.0), (0.0, 0.0, 1.0))

    def test_resolve_traction_on_principal_plane(self) -> None:
        stress = symmetric_stress(xx=10.0, yy=20.0, zz=30.0)
        normal_stress, shear, shear_vector = resolve_traction(stress, (1.0, 0.0, 0.0))

        self.assertAlmostEqual(normal_stress, 10.0)
        self.assertAlmostEqual(shear, 0.0)
        self.assertEqual(shear_vector, (0.0, 0.0, 0.0))

    def test_weak_plane_margin_for_no_shear_case(self) -> None:
        stress = symmetric_stress(xx=10.0, yy=20.0, zz=30.0)
        margin = weak_plane_slip_margin(stress, (1.0, 0.0, 0.0), cohesion=2.0, friction_angle_deg=30.0)

        self.assertGreater(margin, 0.0)
