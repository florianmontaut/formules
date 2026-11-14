"""
Tables de correspondance dans les formules : steps(x; x1; y1...) (paliers, ex: puissance
du convertisseur) et interp(x; x1; y1...) (interpolation, ex: étalonnage d'un capteur).
"""
import numpy as np
import pytest
from formules import FormulaError, evaluate, parse
from formules.lut import format_call, parse_rows

T = np.array([0.0, 100.0, 200.0, 200.5, 201.0, 300.0, 500.0])


def _eval(formula, **variables):
    return evaluate(parse(formula), variables)


# ---------------- steps / interp ----------------

def test_steps_power_profile():
    """De 0 à 200 s : 200 W, à partir de 201 s : 800 W."""
    out = _eval("steps(time; 0; 200; 201; 800)", time=T)
    np.testing.assert_allclose(out, [200, 200, 200, 200, 800, 800, 800])


def test_steps_before_first_point_and_missing_input():
    out = _eval("steps(time; 10; 1; 20; 2)", time=np.array([5.0, 10.0, np.nan, 25.0]))
    assert np.isnan(out[0]) and out[1] == 1 and np.isnan(out[2]) and out[3] == 2


def test_steps_back_to_zero_with_a_last_row():
    out = _eval("steps(time; 0; 200; 400; 0)", time=np.array([399.0, 400.0, 600.0]))
    np.testing.assert_allclose(out, [200, 0, 0])


def test_interp_calibration_curve():
    out = _eval("interp([V]; 0; -40; 5; 150)", **{"[V]": np.array([-1, 0, 2.5, 5, 6.0])})
    assert np.isnan(out[0])
    np.testing.assert_allclose(out[1:], [-40, 55, 150, 150])


def test_lut_in_an_expression():
    out = _eval("steps(time; 0; 200; 201; 800) * 0.95", time=T)
    np.testing.assert_allclose(out[[0, -1]], [190, 760])


@pytest.mark.parametrize("formula, message", [
    ("steps(time; 0; 200; 201)", "pairs"),
    ("steps(time)", "pairs"),
    ("interp(time; 10; 1; 5; 2)", "strictly increasing"),
    ("steps(time; 0; 1; 0; 2)", "strictly increasing"),
    ("steps(time; time; 1)", "numbers only"),
])
def test_invalid_tables(formula, message):
    with pytest.raises(FormulaError, match=message):
        _eval(formula, time=T)


def test_format_call_round_trip():
    rows = [(-10.5, -40.0), (1e-3, 0.25), (3600, 1500)]
    call = format_call("interp", "[T AMB]", rows)
    assert call == "interp([T AMB]; -10.5; -40; 0.001; 0.25; 3600; 1500)"
    np.testing.assert_allclose(_eval(call, **{"[T AMB]": np.array([-10.5, 3600.0])}),
                               [-40, 1500])


# ---------------- collage depuis Excel ----------------

def test_parse_rows_from_excel():
    text = "Temps\tPuissance\r\n0\t200\r\n201\t800,5\r\n\r\n"
    assert parse_rows(text) == [(0, 200), (201, 800.5)]
    assert parse_rows("0;200\n201;800\n") == [(0, 200), (201, 800)]
    assert parse_rows("0 200\n201 800") == [(0, 200), (201, 800)]
    # colonnes au-delà de la 2e ignorées
    assert parse_rows("0\t200\tcommentaire") == [(0, 200)]


def test_parse_rows_reports_a_bad_line():
    with pytest.raises(ValueError, match="Ligne 3"):
        parse_rows("x\ty\n0\t200\nabc\t800")


# ---------------- voie calculée ----------------
