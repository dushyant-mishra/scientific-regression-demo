"""Keep the first example easy to run and aligned with the scientific rules."""

from try_examples import main


def test_examples_explain_all_three_rules(capsys):
    main()
    output = capsys.readouterr().out

    assert "MEASURED_ZERO" in output
    assert "UNMEASURED" in output
    assert "Rows: 1000" in output
    assert "Distinct donors: 2" in output
    assert "Combined status: NOT_ESTIMABLE" in output
