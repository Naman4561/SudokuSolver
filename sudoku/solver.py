from typing import List, Set, Tuple, Dict, Optional

Cell = Tuple[int, int]
Grid = List[List[int]]


def _box_index(r: int, c: int) -> Tuple[int, int]:
    return (r // 3, c // 3)


class Sudoku:
    """Simple logic-only Sudoku solver.

    - Uses sets for candidates
    - Implements elimination, only-choice (hidden singles), and naked pairs
    - Iterates strategies until no progress; no backtracking
    """

    def __init__(self, grid: Grid):
        if len(grid) != 9 or any(len(row) != 9 for row in grid):
            raise ValueError("Grid must be 9x9")
        self.grid: Grid = [[int(x) for x in row] for row in grid]
        self.cands: Dict[Cell, Set[int]] = {}
        self._init_candidates()

    def _init_candidates(self) -> None:
        for r in range(9):
            for c in range(9):
                v = self.grid[r][c]
                if 1 <= v <= 9:
                    self.cands[(r, c)] = {v}
                else:
                    self.cands[(r, c)] = set(range(1, 10))
        # initial elimination
        self._eliminate_all_assigned()

    def _peers(self, r: int, c: int) -> Set[Cell]:
        peers: Set[Cell] = set()
        for i in range(9):
            if i != c:
                peers.add((r, i))
            if i != r:
                peers.add((i, c))
        br, bc = _box_index(r, c)
        for i in range(br * 3, br * 3 + 3):
            for j in range(bc * 3, bc * 3 + 3):
                if (i, j) != (r, c):
                    peers.add((i, j))
        return peers

    def _assign(self, cell: Cell, value: int) -> bool:
        """Assign value to cell (set its candidate set to {value}).
        Returns True if this changes anything, False otherwise.
        """
        if value not in self.cands[cell]:
            # contradiction - trying to assign impossible value
            return False
        if self.cands[cell] == {value}:
            return False
        self.cands[cell] = {value}
        self.grid[cell[0]][cell[1]] = value
        return True

    def _eliminate_from_peer(self, peer: Cell, value: int) -> bool:
        """Remove value from peer candidates. Return True if change."""
        if value in self.cands[peer] and len(self.cands[peer]) > 1:
            self.cands[peer].remove(value)
            return True
        return False

    def _eliminate_all_assigned(self) -> None:
        changed = True
        while changed:
            changed = False
            for cell, s in list(self.cands.items()):
                if len(s) == 1:
                    v = next(iter(s))
                    for peer in self._peers(*cell):
                        if self._eliminate_from_peer(peer, v):
                            changed = True

    def step_eliminate(self) -> bool:
        """Equivalent of step1: basic elimination of assigned digits from peers.
        Returns True if any change was made.
        """
        before = {cell: set(s) for cell, s in self.cands.items()}
        self._eliminate_all_assigned()
        after = self.cands
        return any(before[cell] != after[cell] for cell in before)

    def step_only_choice(self) -> bool:
        """Equivalent of step2 / hidden single: if a candidate digit can only
        appear in one cell within a house, assign it.
        Returns True if any assignment was made.
        """
        changed = False
        # rows
        for r in range(9):
            unit = [(r, c) for c in range(9)]
            changed |= self._only_choice_in_unit(unit)
        # cols
        for c in range(9):
            unit = [(r, c) for r in range(9)]
            changed |= self._only_choice_in_unit(unit)
        # boxes
        for br in range(3):
            for bc in range(3):
                unit = [
                    (r, c)
                    for r in range(br * 3, br * 3 + 3)
                    for c in range(bc * 3, bc * 3 + 3)
                ]
                changed |= self._only_choice_in_unit(unit)
        if changed:
            # after assignments, eliminate
            self._eliminate_all_assigned()
        return changed

    def _only_choice_in_unit(self, unit: List[Cell]) -> bool:
        changed = False
        count_map: Dict[int, List[Cell]] = {d: [] for d in range(1, 10)}
        for cell in unit:
            for d in self.cands[cell]:
                count_map[d].append(cell)
        for d, cells in count_map.items():
            if len(cells) == 1:
                cell = cells[0]
                if self._assign(cell, d):
                    changed = True
        return changed

    def step_naked_pairs(self) -> bool:
        """Detect naked pairs in each unit and eliminate their digits from peers in the unit.
        Returns True if any change made.
        """
        changed = False
        units = []
        # rows
        for r in range(9):
            units.append([(r, c) for c in range(9)])
        # cols
        for c in range(9):
            units.append([(r, c) for r in range(9)])
        # boxes
        for br in range(3):
            for bc in range(3):
                units.append(
                    [
                        (r, c)
                        for r in range(br * 3, br * 3 + 3)
                        for c in range(bc * 3, bc * 3 + 3)
                    ]
                )
        for unit in units:
            # find all cells with 2 candidates
            pair_map: Dict[frozenset, List[Cell]] = {}
            for cell in unit:
                s = self.cands[cell]
                if len(s) == 2:
                    key = frozenset(s)
                    pair_map.setdefault(key, []).append(cell)
            for key, cells in pair_map.items():
                if len(cells) == 2:
                    # eliminate these digits from other cells in unit
                    for cell in unit:
                        if cell not in cells and self.cands[cell] & key:
                            self.cands[cell] = self.cands[cell] - key
                            changed = True
        if changed:
            self._eliminate_all_assigned()
        return changed

    def solve(self, max_rounds: int = 100) -> bool:
        """Apply strategies iteratively until solved or stalled.
        Returns True if solved (all cells have a single value), False otherwise.
        """
        strategies = [self.step_eliminate, self.step_only_choice, self.step_naked_pairs]
        for _ in range(max_rounds):
            progress = False
            for strat in strategies:
                if strat():
                    progress = True
            if self.is_solved():
                return True
            if not progress:
                return False
        return self.is_solved()

    def is_solved(self) -> bool:
        return all(len(self.cands[(r, c)]) == 1 for r in range(9) for c in range(9))

    def to_grid(self) -> Grid:
        return [[next(iter(self.cands[(r, c)])) for c in range(9)] for r in range(9)]

    def __str__(self) -> str:
        lines = []
        for r in range(9):
            row = []
            for c in range(9):
                s = self.cands[(r, c)]
                if len(s) == 1:
                    row.append(str(next(iter(s))))
                else:
                    row.append(".")
            lines.append(" ".join(row))
        return "\n".join(lines)
