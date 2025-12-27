# SudokuSolver (Python port)

This repository contains a logic-only Sudoku solver.

Features:
- Uses set-based candidates for clarity
- Implements elimination, only-choice (hidden singles), and naked pairs
- No backtracking (keeps the solver purely logic-based)

Usage (CLI):

```
python -m sudoku.cli examples/sudin228.txt
```

By default the CLI reads `examples/sudin228.txt` if no path is given. Use `--max-rounds` to limit iteration rounds and `--quiet` to only print the final grid.