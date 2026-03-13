from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_cli(commands: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "vector_editor"],
        input=commands,
        capture_output=True,
        text=True,
        cwd=ROOT,
        timeout=5,
        check=False,
    )


class VectorEditorCliTests(unittest.TestCase):
    def test_cli_create_list_delete_and_list_again(self) -> None:
        result = run_cli(
            "\n".join(
                [
                    "create point 1 2",
                    "create circle 3 4 5",
                    "list",
                    "delete 1",
                    "list",
                    "exit",
                ]
            )
            + "\n"
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("Created point with id=1", result.stdout)
        self.assertIn("Created circle with id=2", result.stdout)
        self.assertIn("[1] point x=1 y=2", result.stdout)
        self.assertIn("[2] circle cx=3 cy=4 r=5", result.stdout)
        self.assertIn("Deleted shape id=1", result.stdout)
        self.assertIn("> [2] circle cx=3 cy=4 r=5", result.stdout)

    def test_cli_invalid_command_does_not_crash_repl(self) -> None:
        result = run_cli("unknown\nhelp\nexit\n")

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("Invalid command. Type 'help' for usage.", result.stdout)
        self.assertIn("Available commands:", result.stdout)

    def test_cli_invalid_number_format_reports_error(self) -> None:
        result = run_cli("create point one 2\nexit\n")

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("Error: invalid number format. Type 'help' for usage.", result.stdout)

    def test_cli_invalid_argument_count_reports_error(self) -> None:
        result = run_cli("create square 1 2\nexit\n")

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("Invalid command. Type 'help' for usage.", result.stdout)


if __name__ == "__main__":
    unittest.main()
