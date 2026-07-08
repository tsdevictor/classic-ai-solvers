import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "othello" / "othello_engine.py"

def main():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        check=True,
    )

    output = result.stdout

    expected_snippets = [
        "Possible moves for x: 19, 26, 37, 44",
        "The preferred move is: 37",
    ]

    missing = [snippet for snippet in expected_snippets if snippet not in output]

    if missing:
        print("Othello smoke test failed.")
        print("Missing expected output:")
        for snippet in missing:
            print(f"- {snippet}")
        print("\nActual output:")
        print(output)
        raise SystemExit(1)

    print("Othello smoke test passed.")

if __name__ == "__main__":
    main()
