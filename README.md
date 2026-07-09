# Classic AI Solvers

A merged collection of classic AI/search projects: chess, crossword generation, Othello, and Sudoku.

The repository currently preserves the original project implementations while organizing the strongest versions into a cleaner structure. The focus is on classical AI techniques rather than machine learning libraries:

- Game-tree search
- Minimax and alpha-beta pruning
- Board evaluation heuristics
- Constraint satisfaction
- Recursive backtracking
- Graph/flood-fill validation
- Puzzle and board-state representations

## Projects

### Othello

Othello/Reversi engine with legal move generation, board updates, heuristic evaluation, move ordering, and alpha-beta search.

Active file:

- `othello/othello_engine.py`

### Sudoku

Constraint-based Sudoku solver using recursive backtracking and pruning heuristics.

Active file:

- `sudoku/sudoku_solver.py`

### Crossword Generation

Crossword grid generator with rotational symmetry constraints, connectivity checks, and recursive block placement.

Active file:

- `crosswords/crossword_generator.py`

### Chess

Chess engine/game implementation with board, piece, move, player, GUI, and PGN utilities.

Main folders:

- `chess/engine/`
- `chess/gui/`
- `chess/pgn/`

## Current status

This is a consolidation repo. The strongest versions of several classic AI/search projects have been moved into a cleaner public structure, while older experiments are preserved under `archive/`.

## Future improvements

- Add clean command-line entry points for each solver.
- Add more tests for board logic and puzzle validation.
- Add benchmarks for search depth and solve time.
- Refactor the strongest implementations into importable modules.
- Add iterative deepening and stronger stability/frontier heuristics to Othello.
