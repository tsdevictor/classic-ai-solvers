# Sudoku

Constraint-based Sudoku solver.

Current active implementation:

- `sudoku_solver.py`

Core ideas:

- Recursive backtracking
- Choosing constrained positions first
- Symbol/position pruning
- Row, column, and box constraints

Cleanup goals:

- Add a puzzle parser
- Add a solution validator
- Add tests for valid and invalid puzzles
- Benchmark solve time across easy, medium, hard, and expert puzzles
