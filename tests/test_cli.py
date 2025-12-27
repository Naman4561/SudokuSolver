from sudoku import cli


def test_cli_runs_and_solves(capsys):
    rc = cli.main(["examples/sudin228.txt"])
    assert rc == 0
    captured = capsys.readouterr()
    # should contain Solved and a 9x9 grid
    assert "Solved:" in captured.out
    lines = [l for l in captured.out.splitlines() if l.strip()]
    # last 9 non-empty lines should be the grid
    grid_lines = [l for l in lines[-9:]]
    assert len(grid_lines) == 9
    # each grid line should have 9 tokens
    for ln in grid_lines:
        assert len(ln.split()) == 9
