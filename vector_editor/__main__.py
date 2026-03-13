from __future__ import annotations

import shlex

from .editor import VectorEditor
from .models import format_shape
from .models import shape_name

HELP_TEXT = """Available commands:
  create point <x> <y>
  create segment <x1> <y1> <x2> <y2>
  create circle <cx> <cy> <radius>
  create square <x> <y> <side>
  delete <id>
  list
  help
  exit
  quit"""

USAGE_HINT = "Type 'help' for usage."


class CommandError(ValueError):
    pass


def main() -> int:
    editor = VectorEditor()

    while True:
        try:
            # `input` gives us a simple REPL prompt without extra dependencies.
            raw_command = input("> ")
        except EOFError:
            print()
            return 0
        except KeyboardInterrupt:
            print()
            return 0

        try:
            should_exit, message = execute_command(editor, raw_command)
        except CommandError as error:
            print(f"{error} {USAGE_HINT}")
            continue

        if message is not None:
            print(message)
        if should_exit:
            return 0


def execute_command(editor: VectorEditor, raw_command: str) -> tuple[bool, str | None]:
    if not raw_command.strip():
        return False, None

    try:
        # `shlex` makes quoted input predictable and close to shell-style parsing.
        parts = shlex.split(raw_command)
    except ValueError as error:
        raise CommandError(f"Error: {error}.") from error

    command = parts[0].lower()

    if command in {"exit", "quit"}:
        return True, None
    if command == "help":
        return False, HELP_TEXT
    if command == "list":
        return False, render_shapes(editor)
    if command == "delete":
        return False, handle_delete(editor, parts)
    if command == "create":
        return False, handle_create(editor, parts)

    raise CommandError("Invalid command.")


def handle_delete(editor: VectorEditor, parts: list[str]) -> str:
    if len(parts) != 2:
        raise CommandError("Invalid command.")

    try:
        shape_id = int(parts[1])
    except ValueError as error:
        raise CommandError("Error: invalid id format.") from error

    if editor.delete_shape(shape_id):
        return f"Deleted shape id={shape_id}"
    return f"Shape id={shape_id} not found"


def handle_create(editor: VectorEditor, parts: list[str]) -> str:
    if len(parts) < 2:
        raise CommandError("Invalid command.")

    shape_type = parts[1].lower()
    coordinates = parts[2:]

    # The dispatch table keeps CLI parsing flat and makes adding shapes straightforward.
    handlers: dict[str, tuple[int, callable]] = {
        "point": (2, editor.create_point),
        "segment": (4, editor.create_segment),
        "circle": (3, editor.create_circle),
        "square": (3, editor.create_square),
    }

    if shape_type not in handlers:
        raise CommandError("Invalid command.")

    expected_arg_count, factory = handlers[shape_type]
    if len(coordinates) != expected_arg_count:
        raise CommandError("Invalid command.")

    values = parse_float_values(coordinates)

    try:
        shape = factory(*values)
    except ValueError as error:
        raise CommandError(f"Error: {error}.") from error

    return f"Created {shape_name(shape)} with id={shape.id}"


def parse_float_values(values: list[str]) -> list[float]:
    try:
        return [float(value) for value in values]
    except ValueError as error:
        raise CommandError("Error: invalid number format.") from error


def render_shapes(editor: VectorEditor) -> str:
    shapes = editor.list_shapes()
    if not shapes:
        return "No shapes created."
    return "\n".join(format_shape(shape) for shape in shapes)


if __name__ == "__main__":
    raise SystemExit(main())
