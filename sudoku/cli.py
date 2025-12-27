from typing import List, Optional
import argparse
import sys

from .io import read_csv_puzzle, format_grid
from .solver import Sudoku


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Solve a Sudoku puzzle file (CSV rows of 9 integers).")
    parser.add_argument("puzzle", nargs="?", default="examples/sudin228.txt", help="Path to puzzle file")
    parser.add_argument("--max-rounds", type=int, default=100, help="Maximum strategy rounds")
    parser.add_argument("--quiet", action="store_true", help="Only print solved grid")
    args = parser.parse_args(argv)

    try:
        grid = read_csv_puzzle(args.puzzle)
    except Exception as e:
        print(f"Error reading puzzle: {e}", file=sys.stderr)
        return 2

    s = Sudoku(grid)
    solved = s.solve(max_rounds=args.max_rounds)

    if not args.quiet:
        print("Initial:")
        print(format_grid(grid))
        print()

    print("Solved:" if solved else "Stalled (not fully solved):")
    print(format_grid(s.to_grid() if solved else [[0 if len(s.cands[(r,c)])>1 else next(iter(s.cands[(r,c)])) for c in range(9)] for r in range(9)]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
