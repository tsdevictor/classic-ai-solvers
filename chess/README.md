# Chess

Chess engine and GUI project.

Important folders:

- `engine/`
- `gui/`
- `pgn/`

Core ideas:

- Board representation
- Pieces and legal moves
- Player state
- Move objects
- PGN/FEN utilities
- GUI layer
- Minimax-based AI search

## Engine Smoke Test

From the repository root:

```bash
python tests/smoke_chess.py

Expected result:

Chess smoke test passed.
White pieces: 16
Black pieces: 16
White legal moves: 20
Black legal moves: 20

This smoke test avoids the GUI and verifies that the chess engine can initialize the standard board and compute legal opening moves.

Existing AI Test

There is also an older minimax test:

PYTHONPATH=chess python chess/engine/players/ai/test.py

This creates a board, makes several moves, and runs the minimax strategy.

GUI

The GUI is Tkinter-based and lives in:

chess/gui/

The GUI should be treated as a separate layer from the engine.

Cleanup goals
Verify and document the main GUI entry point
Separate GUI from engine logic
Add tests for legal moves and board state transitions
Add tests for special rules if supported: castling, en passant, promotion, check, checkmate, and stalemate
Replace legacy script-style tests with proper test files
