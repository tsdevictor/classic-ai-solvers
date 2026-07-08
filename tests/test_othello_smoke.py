def test_othello_imports_and_finds_initial_moves():
    import importlib.util
    from pathlib import Path

    path = Path("othello/othello_engine.py")
    spec = importlib.util.spec_from_file_location("othello_engine", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    mod.set_globals()
    board = "...........................ox......xo..........................."
    moves = mod.findMoves(board, "x")

    assert set(moves) == {19, 26, 37, 44}
