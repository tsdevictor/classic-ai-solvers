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

Cleanup goals:

- Separate grid representation from search
- Add generated examples
- Add validity tests for symmetry, connectivity, and word lengths
- Document the search/pruning strategy
