# Sudoku

Constraint-based Sudoku solver.

Current active implementation:

- `sudoku_solver.py`

Core ideas:

- Recursive backtracking
- Choosing constrained positions first
- Symbol/position pruning
- Row, column, and box constraints
- Support for puzzle sizes inferred from input length

## Run

From the repository root:

```bash
python sudoku/sudoku_solver.py examples/sudoku/easy.txt

The solver expects a text file where each line is one Sudoku puzzle. Empty cells should be represented with ..

Example puzzle:

53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79

Expected solution:

534678912672195348198342567859761423426853791713924856961537284287419635345286179
Smoke Test

From the repository root:

python tests/smoke_sudoku.py

Expected result:

Sudoku smoke test passed.
Cleanup goals
Add a cleaner puzzle parser
Add a solution validator
Add tests for valid and invalid puzzles
Benchmark solve time across easy, medium, hard, and expert puzzles
Refactor globals into an explicit solver object
