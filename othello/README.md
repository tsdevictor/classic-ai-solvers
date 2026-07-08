# Othello

Othello/Reversi AI engine.

Current active implementation:

- `othello_engine.py`

Core ideas:

- Legal move generation
- Board updates and disc flipping
- Mobility, corner, and stability-style evaluation
- Move ordering
- Alpha-beta pruning

Cleanup goals:

- Split board logic, move generation, evaluation, and search into separate files
- Add tests for legal moves and move application
- Add benchmarks comparing plain minimax and alpha-beta pruning
