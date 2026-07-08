# Crossword Generator

Crossword grid generator.

Current active implementation:

- `crossword_generator.py`

Core ideas:

- Rotational symmetry
- Block placement constraints
- Minimum word length constraints
- Connectivity checks with flood fill
- Recursive search
- Dictionary-based fill with uniqueness constraints

## Run

From the repository root:

```bash
python crosswords/crossword_generator.py crosswords/examples/tiny_dictionary.txt 3x3 0

Arguments:

Dictionary file
Grid size, such as 3x3 or 15x15
Number of blocking squares

Example dictionary:

crosswords/examples/tiny_dictionary.txt

The tiny example is a 3x3 puzzle with no blocks. It is intended as a fast smoke test, not a realistic crossword.

Smoke Test

From the repository root:

python tests/smoke_crosswords.py

Expected result:

Crossword smoke test passed.
Cleanup goals
Separate grid representation from search
Add generated examples
Add validity tests for symmetry, connectivity, and word lengths
Document the search/pruning strategy
Refactor global state into explicit solver/config objects
