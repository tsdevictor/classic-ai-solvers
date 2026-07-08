import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "sudoku" / "sudoku_solver.py"
PUZZLES = ROOT / "sudoku" / "examples" / "easy.txt"

EXPECTED_SOLUTION = (
    "534678912672195348198342567859761423426853791713924856961537284287419635345286179"
)

def main():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(PUZZLES)],
        capture_output=True,
        text=True,
        check=True,
    )

    output = result.stdout

    if EXPECTED_SOLUTION not in output:
        print("Sudoku smoke test failed.")
        print("Expected solution was not found in output.")
        print("\nActual output:")
        print(output)
        raise SystemExit(1)

    print("Sudoku smoke test passed.")

if __name__ == "__main__":
    main()
