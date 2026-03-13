from __future__ import annotations

from .models import Circle
from .models import Point
from .models import Segment
from .models import Shape
from .models import Square


class VectorEditor:
    def __init__(self) -> None:
        # Shapes are stored in insertion order so `list` reflects creation order.
        self._shapes: list[Shape] = []
        self._next_id = 1

    def create_point(self, x: float, y: float) -> Point:
        shape = Point(id=self._next_shape_id(), x=x, y=y)
        self._shapes.append(shape)
        return shape

    def create_segment(self, x1: float, y1: float, x2: float, y2: float) -> Segment:
        shape = Segment(id=self._next_shape_id(), x1=x1, y1=y1, x2=x2, y2=y2)
        self._shapes.append(shape)
        return shape

    def create_circle(self, cx: float, cy: float, radius: float) -> Circle:
        if radius <= 0:
            raise ValueError("radius must be greater than 0")

        shape = Circle(id=self._next_shape_id(), cx=cx, cy=cy, radius=radius)
        self._shapes.append(shape)
        return shape

    def create_square(self, x: float, y: float, side: float) -> Square:
        if side <= 0:
            raise ValueError("side must be greater than 0")

        shape = Square(id=self._next_shape_id(), x=x, y=y, side=side)
        self._shapes.append(shape)
        return shape

    def delete_shape(self, shape_id: int) -> bool:
        for index, shape in enumerate(self._shapes):
            if shape.id == shape_id:
                del self._shapes[index]
                return True
        return False

    def list_shapes(self) -> list[Shape]:
        # Return a copy so callers cannot mutate the editor state from the outside.
        return list(self._shapes)

    def _next_shape_id(self) -> int:
        # IDs are monotonically increasing and never reused within one session.
        shape_id = self._next_id
        self._next_id += 1
        return shape_id
