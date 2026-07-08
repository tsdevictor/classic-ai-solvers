import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "crosswords" / "crossword_generator.py"
DICTIONARY = ROOT / "crosswords" / "examples" / "tiny_dictionary.txt"

VALID_SOLUTIONS = {
    "caborewed",
    "cowarebed",
}

def main():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(DICTIONARY), "3x3", "0"],
        capture_output=True,
        text=True,
        check=True,
    )

    output = result.stdout

    if not any(solution in output for solution in VALID_SOLUTIONS):
        print("Crossword smoke test failed.")
        print("Expected one of these solution strings:")
        for solution in sorted(VALID_SOLUTIONS):
            print(f"- {solution}")
        print("\nActual output:")
        print(output)
        raise SystemExit(1)

    print("Crossword smoke test passed.")

if __name__ == "__main__":
    main()
