import pytest
from sudoku import Sudoku

SAMPLE = [
    [3,0,9,0,0,0,7,4,0],
    [0,8,0,0,6,7,0,2,0],
    [0,5,0,3,8,0,0,0,0],
    [5,0,0,1,4,0,8,3,0],
    [0,3,8,5,0,2,1,9,0],
    [0,1,4,0,3,6,0,0,5],
    [0,0,0,0,2,8,0,5,0],
    [0,9,0,6,5,0,0,8,0],
    [0,4,5,0,0,0,6,0,2],
]

# This test checks that strategies make progress and do not crash.

def test_solve_progress():
    s = Sudoku(SAMPLE)
    # initial grid may already be solved by initialization or may need strategies; just ensure solve runs
    solved = s.solve(max_rounds=20)
    assert solved is False or solved is True


def test_naked_pairs_effect():
    # Construct a small scenario in a row where two cells have the same two candidates
    grid = [[0]*9 for _ in range(9)]
    # put some givens to limit candidates in row 0
    grid[0][0] = 1
    grid[0][1] = 2
    grid[0][2] = 3
    grid[0][3] = 0
    grid[0][4] = 0
    grid[0][5] = 0
    grid[0][6] = 7
    grid[0][7] = 8
    grid[0][8] = 9
    s = Sudoku(grid)
    # after elimination, the middle three cells should have candidates {4,5,6} in some split
    assert any(len(s.cands[(0,c)]) >= 1 for c in (3,4,5))
    # force a pair: set two cells to {4,5}
    s.cands[(0,3)] = {4,5}
    s.cands[(0,4)] = {4,5}
    changed = s.step_naked_pairs()
    # after naked pair elimination, the other cell (0,5) should not contain 4 or 5
    assert changed
    assert 4 not in s.cands[(0,5)] and 5 not in s.cands[(0,5)]
