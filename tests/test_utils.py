from unittest import TestCase

from wellbore_stability_utils import (
    CandidateResult,
    EnvelopeAggregator,
    ProjectSummary,
    ValidationMetric,
    gcc_to_mpa_per_meter,
    mpa_per_meter_to_gcc,
    normalize_degrees,
    render_summary,
    render_validation_table,
)


class UnitHelperTests(TestCase):
    def test_density_gradient_roundtrip(self) -> None:
        density = 1.25
        gradient = gcc_to_mpa_per_meter(density)

        self.assertAlmostEqual(mpa_per_meter_to_gcc(gradient), density)

    def test_normalize_degrees(self) -> None:
        self.assertEqual(normalize_degrees(370.0), 10.0)
        self.assertEqual(normalize_degrees(-10.0), 350.0)


class CandidateResultTests(TestCase):
    def test_rejects_empty_name(self) -> None:
        with self.assertRaises(ValueError):
            CandidateResult(name=" ", value=1.0)

    def test_rejects_nonfinite_value(self) -> None:
        with self.assertRaises(ValueError):
            CandidateResult(name="candidate", value=float("nan"))


class EnvelopeAggregatorTests(TestCase):
    def test_selects_highest_value_by_default(self) -> None:
        result = EnvelopeAggregator().select(
            [
                CandidateResult("baseline", 1.1, family="demo"),
                CandidateResult("envelope", 1.3, family="demo"),
                CandidateResult("adjusted", 1.2, family="demo"),
            ]
        )

        self.assertEqual(result.controlling.name, "envelope")
        self.assertAlmostEqual(result.margin_to_second, 0.1)

    def test_tie_breaking_is_deterministic(self) -> None:
        result = EnvelopeAggregator().select(
            [
                CandidateResult("b", 1.0, family="demo"),
                CandidateResult("a", 1.0, family="demo"),
            ]
        )

        self.assertEqual([item.name for item in result.ranked], ["a", "b"])


class ReportingTests(TestCase):
    def test_render_validation_table_escapes_pipes(self) -> None:
        table = render_validation_table(
            [ValidationMetric("A|B", "pass", "stable\ncompact")]
        )

        self.assertIn("A\\|B", table)
        self.assertIn("stable compact", table)

    def test_render_summary(self) -> None:
        summary = ProjectSummary(
            name="utils",
            maintainer="zerolong1109",
            scope="result organization",
            metrics=(ValidationMetric("tests", "pass", "public API"),),
        )

        text = render_summary(summary)

        self.assertIn("# utils", text)
        self.assertIn("Maintainer: zerolong1109", text)
        self.assertIn("| tests | pass | public API |", text)
