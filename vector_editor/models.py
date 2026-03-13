from __future__ import annotations

from dataclasses import dataclass


def format_number(value: float) -> str:
    # Keep console output compact: `1.0` becomes `1`, while fractional values stay readable.
    if value.is_integer():
        return str(int(value))
    return format(value, "g")


@dataclass(frozen=True, slots=True)
class Point:
    id: int
    x: float
    y: float


@dataclass(frozen=True, slots=True)
class Segment:
    id: int
    x1: float
    y1: float
    x2: float
    y2: float


@dataclass(frozen=True, slots=True)
class Circle:
    id: int
    cx: float
    cy: float
    radius: float


@dataclass(frozen=True, slots=True)
class Square:
    id: int
    x: float
    y: float
    side: float


type Shape = Point | Segment | Circle | Square


def shape_name(shape: Shape) -> str:
    if isinstance(shape, Point):
        return "point"
    if isinstance(shape, Segment):
        return "segment"
    if isinstance(shape, Circle):
        return "circle"
    return "square"


def format_shape(shape: Shape) -> str:
    # Centralized formatting keeps `list` output consistent for every caller.
    if isinstance(shape, Point):
        return (
            f"[{shape.id}] point x={format_number(shape.x)} "
            f"y={format_number(shape.y)}"
        )
    if isinstance(shape, Segment):
        return (
            f"[{shape.id}] segment x1={format_number(shape.x1)} "
            f"y1={format_number(shape.y1)} x2={format_number(shape.x2)} "
            f"y2={format_number(shape.y2)}"
        )
    if isinstance(shape, Circle):
        return (
            f"[{shape.id}] circle cx={format_number(shape.cx)} "
            f"cy={format_number(shape.cy)} r={format_number(shape.radius)}"
        )
    return (
        f"[{shape.id}] square x={format_number(shape.x)} "
        f"y={format_number(shape.y)} side={format_number(shape.side)}"
    )
