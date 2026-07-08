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
- Opening-book lookup for known early positions

## Run

From the repository root:

```bash
python othello/othello_engine.py

Expected default behavior:

Prints the standard opening board
Marks legal moves with *
Lists possible moves for x
Prints the preferred move

Example default result:

Possible moves for x: 19, 26, 37, 44
The preferred move is: 37
Smoke Test

From the repository root:

python tests/smoke_othello.py

Expected result:

Othello smoke test passed.
Cleanup goals
Split board logic, move generation, evaluation, and search into separate files
Add tests for legal moves and move application
Add benchmarks comparing plain minimax and alpha-beta pruning
