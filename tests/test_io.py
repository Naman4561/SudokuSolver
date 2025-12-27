from sudoku.io import read_csv_puzzle


def test_read_trailing_comma(tmp_path):
    content = (
        "3, 0, 9, 0, 0, 0, 7, 4, 0,\n"
        "0, 8, 0, 0, 6, 7, 0, 2, 0,\n"
        "0, 5, 0, 3, 8, 0, 0, 0, 0,\n"
        "5, 0, 0, 1, 4, 0, 8, 3, 0,\n"
        "0, 3, 8, 5, 0, 2, 1, 9, 0,\n"
        "0, 1, 4, 0, 3, 6, 0, 0, 5,\n"
        "0, 0, 0, 0, 2, 8, 0, 5, 0,\n"
        "0, 9, 0, 6, 5, 0, 0, 8, 0,\n"
        "0, 4, 5, 0, 0, 0, 6, 0, 2,\n"
    )
    p = tmp_path / "puzzle.txt"
    p.write_text(content)
    grid = read_csv_puzzle(str(p))
    assert grid[0] == [3, 0, 9, 0, 0, 0, 7, 4, 0]
    assert grid[8] == [0, 4, 5, 0, 0, 0, 6, 0, 2]


def test_read_internal_empty_field(tmp_path):
    # internal empty field between commas should be treated as 0
    line = "1,2,,4,5,6,7,8,9\n"
    content = line * 9
    p = tmp_path / "p2.txt"
    p.write_text(content)
    grid = read_csv_puzzle(str(p))
    for r in grid:
        assert r == [1, 2, 0, 4, 5, 6, 7, 8, 9]
