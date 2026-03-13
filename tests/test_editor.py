from __future__ import annotations

import unittest

from vector_editor.editor import VectorEditor
from vector_editor.models import Circle
from vector_editor.models import Point
from vector_editor.models import Segment
from vector_editor.models import Square
from vector_editor.models import format_shape


class VectorEditorTests(unittest.TestCase):
    def test_create_point_assigns_id_and_coordinates(self) -> None:
        editor = VectorEditor()

        shape = editor.create_point(1.0, 2.5)

        self.assertIsInstance(shape, Point)
        self.assertEqual(shape.id, 1)
        self.assertEqual(shape.x, 1.0)
        self.assertEqual(shape.y, 2.5)

    def test_create_segment_assigns_id_and_coordinates(self) -> None:
        editor = VectorEditor()

        shape = editor.create_segment(0.0, 1.0, 2.0, 3.0)

        self.assertIsInstance(shape, Segment)
        self.assertEqual(shape.id, 1)
        self.assertEqual((shape.x1, shape.y1, shape.x2, shape.y2), (0.0, 1.0, 2.0, 3.0))

    def test_create_circle_assigns_id_and_radius(self) -> None:
        editor = VectorEditor()

        shape = editor.create_circle(3.0, 4.0, 5.0)

        self.assertIsInstance(shape, Circle)
        self.assertEqual(shape.id, 1)
        self.assertEqual((shape.cx, shape.cy, shape.radius), (3.0, 4.0, 5.0))

    def test_create_square_assigns_id_and_side(self) -> None:
        editor = VectorEditor()

        shape = editor.create_square(7.0, 8.0, 2.0)

        self.assertIsInstance(shape, Square)
        self.assertEqual(shape.id, 1)
        self.assertEqual((shape.x, shape.y, shape.side), (7.0, 8.0, 2.0))

    def test_ids_increment_in_creation_order(self) -> None:
        editor = VectorEditor()

        shapes = [
            editor.create_point(1.0, 2.0),
            editor.create_segment(0.0, 0.0, 5.0, 5.0),
            editor.create_circle(3.0, 4.0, 10.0),
            editor.create_square(7.0, 8.0, 2.0),
        ]

        self.assertEqual([shape.id for shape in shapes], [1, 2, 3, 4])

    def test_delete_existing_shape_returns_true_and_removes_it(self) -> None:
        editor = VectorEditor()
        editor.create_point(1.0, 2.0)
        editor.create_circle(3.0, 4.0, 5.0)

        deleted = editor.delete_shape(1)

        self.assertTrue(deleted)
        self.assertEqual([shape.id for shape in editor.list_shapes()], [2])

    def test_delete_missing_shape_returns_false(self) -> None:
        editor = VectorEditor()
        editor.create_point(1.0, 2.0)

        deleted = editor.delete_shape(99)

        self.assertFalse(deleted)
        self.assertEqual([shape.id for shape in editor.list_shapes()], [1])

    def test_list_shapes_returns_empty_list_when_editor_is_empty(self) -> None:
        editor = VectorEditor()

        self.assertEqual(editor.list_shapes(), [])

    def test_list_shapes_returns_shapes_in_creation_order(self) -> None:
        editor = VectorEditor()
        editor.create_point(1.0, 2.0)
        editor.create_square(7.0, 8.0, 2.0)

        listed_shapes = editor.list_shapes()

        self.assertEqual(
            [format_shape(shape) for shape in listed_shapes],
            ["[1] point x=1 y=2", "[2] square x=7 y=8 side=2"],
        )

    def test_create_circle_rejects_non_positive_radius(self) -> None:
        editor = VectorEditor()

        with self.assertRaisesRegex(ValueError, "radius must be greater than 0"):
            editor.create_circle(0.0, 0.0, 0.0)

        with self.assertRaisesRegex(ValueError, "radius must be greater than 0"):
            editor.create_circle(0.0, 0.0, -1.0)

    def test_create_square_rejects_non_positive_side(self) -> None:
        editor = VectorEditor()

        with self.assertRaisesRegex(ValueError, "side must be greater than 0"):
            editor.create_square(0.0, 0.0, 0.0)

        with self.assertRaisesRegex(ValueError, "side must be greater than 0"):
            editor.create_square(0.0, 0.0, -1.0)


if __name__ == "__main__":
    unittest.main()
