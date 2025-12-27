from typing import List

Grid = List[List[int]]


def read_csv_puzzle(path: str) -> Grid:
    """Read a puzzle where each line is 9 comma-separated integers (0 for empty)."""
    grid: Grid = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            # Allow a trailing comma at the end of a line (e.g. "1,2,3,...,9,")
            parts = [p.strip() for p in line.split(",")]
            if len(parts) > 0 and parts[-1] == "":
                # drop a single trailing empty part produced by a trailing comma
                parts = parts[:-1]
            if len(parts) != 9:
                raise ValueError("Each line must have 9 comma-separated values (trailing comma is allowed)")
            # Treat empty fields as 0 (empty cell)
            row = [int(x) if x != "" else 0 for x in parts]
            grid.append(row)
    if len(grid) != 9:
        raise ValueError("Puzzle must have 9 rows")
    return grid


def format_grid(grid: Grid) -> str:
    lines = []
    for r in range(9):
        lines.append(
            " ".join(str(x) if x != 0 else "." for x in grid[r])
        )
    return "\n".join(lines)
