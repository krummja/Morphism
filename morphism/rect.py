from __future__ import annotations
from typing import *

from numbers import Real
import numpy as np
from numpy.lib.index_tricks import IndexExpression

from .shape import Shape
from .direction import Direction
from .point import Point
from .size import Size
from .span import Span


class Rect(Shape):
    """Representation of a Rectangle."""

    def __new__(cls, origin: Point, size: Size):
        cls.origin = origin
        cls.size = size
        return super().__new__(cls, (origin, size))

    def __getnewargs__(self):
        return self.origin, self.size

    def __init__(self, origin: Point, size: Size) -> None:
        self.origin = origin
        self.size = size

    def __contains__(self, other: object) -> bool:
        """Check if this Rect _properly_ contains a target Rect or Point."""
        if isinstance(other, Rect):
            return (self.top < other.top and
                    self.bottom > other.bottom and
                    self.left < other.left and
                    self.right > other.right)

        elif isinstance(other, Point):
            return (self.left <= other.x <= self.right and
                    self.top <= other.y <= self.bottom)

        else:
            return False

    def __repr__(self):
        return 'Rect({!r}, {!r})'.format(self.origin, self.size)

    @classmethod
    def from_edges(cls, *, top: Real, bottom: Real, left: Real, right: Real) -> Rect:
        """
        Create a new Rect object by defining the values of its four edges.
        """
        return Rect(Point(left, top), Size(right - left + 1, bottom - top + 1))

    @classmethod
    def from_spans(cls, *, vertical: Span, horizontal: Span) -> Rect:
        """
        Create a new Rect object by defining its vertical and horizontal dimensions
        as Span objects.
        """
        return cls.from_edges(top=vertical.start.y, bottom=vertical.end.y,
                              left=horizontal.start.x, right=horizontal.end.x)

    @classmethod
    def centered_at(cls, size: Size, center: Point) -> Rect:
        """
        Create a new Rect object by defining its dimensions as a Size object
        and its centerpoint as a Point object.
        """
        left = center.x - size.width // 2
        top = center.y - int(size.height) // 2
        return Rect(Point(left, top), size)

    def with_origin(self, new_origin: Point) -> Rect:
        """A copy of this rect with the given origin."""
        return Rect(new_origin, self.size)

    def with_size(self, new_size: Size) -> Rect:
        """A copy of this rect with the given size."""
        return Rect(self.origin, new_size)

    @property
    def top(self) -> Real:
        return self.origin.y

    @property
    def bottom(self) -> Real:
        return self.origin.y + self.size.height

    @property
    def left(self) -> Real:
        return self.origin.x

    @property
    def right(self) -> Real:
        return self.origin.x + self.size.width

    @property
    def width(self) -> int:
        return int(self.size.width)

    @width.setter
    def width(self, new_value):
        self.size = Size(new_value, self.height)

    @property
    def height(self) -> int:
        return int(self.size.height)

    @height.setter
    def height(self, new_value):
        self.size = Size(self.width, new_value)

    @property
    def x(self):
        """Forwarded from ``self.origin.x``"""
        return self.origin.x

    @x.setter
    def x(self, new_value):
        self.origin = Point(new_value, self.y)

    @property
    def y(self):
        """Forwarded from ``self.origin.y``"""
        return self.origin.y

    @y.setter
    def y(self, new_value):
        self.origin = Point(self.x, new_value)

    @property  # no setter; it's not clear if it would change origin or size
    def x2(self):
        """Max X value of this rect. Read-only."""
        return self.origin.x + self.size.width - 1

    @property  # no setter; it's not clear if it would change origin or sizey
    def y2(self):
        """Max Y value of this rect. Read-only."""
        return self.origin.y + self.size.height - 1

    @property
    def area(self) -> int:
        """Getter for the area property of this Rect's Size definition."""
        return int(self.size.area)

    @property
    def floored(self):
        return Rect(self.origin.floored, self.size.floored)

    @property
    def inner(self) -> IndexExpression:
        """Get a NumPy IndexExpression for the inner portion of the Rect."""
        return np.s_[(self.left+1):(self.right-1), (self.top+1):(self.bottom-1)]

    @property
    def outer(self) -> IndexExpression:
        """Get a NumPy IndexExpression for the inner portion + the border
        of the Rect.
        """
        return np.s_[self.left:self.right, self.top:self.bottom]

    @property
    def indices(self) -> IndexExpression:
        """Get a NumPy IndexExpression for this Rect."""
        return np.s_[self.top:self.bottom, self.left:self.right]

    @property
    def vertical_span(self) -> Span:
        """Return a Span for this Rect's vertical axis, from the origin."""
        return Span(Point(self.left, self.top), Point(self.left, self.bottom))

    @property
    def horizontal_span(self) -> Span:
        """Return a Span for this Rect's horizontal axis, from the origin."""
        return Span(Point(self.left, self.top), Point(self.right, self.top))

    @property
    def center(self) -> Point:
        """Get the center of this Rect as a Point object."""
        return self.relative_point(0.5, 0.5)

    @property
    def points_top(self):
        """Iterator of all points along the top edge of this rect"""
        start = self.origin.x + 1
        end = self.origin.x + self.size.width - 1
        for x in range(start, end):
            yield Point(x, self.origin.y)

    @property
    def points_bottom(self):
        """Iterator of all points along the bottom edge of this rect"""
        start = self.origin.x + 1
        end = self.origin.x + self.size.width - 1
        for x in range(start, end):
            yield Point(x, int(self.origin.y + self.size.height - 1))

    @property
    def points_left(self):
        """Iterator of all points along the left edge of this rect"""
        start = self.origin.y + 1
        end = int(self.origin.y + self.size.height - 1)
        for y in range(start, end):
            yield Point(self.origin.x, y)

    @property
    def points_right(self):
        """Iterator of all points along the right edge of this rect"""
        start = self.origin.y + 1
        end = int(self.origin.y + self.size.height - 1)
        for y in range(start, end):
            yield Point(self.origin.x + self.size.width - 1, y)

    @property
    def points_corners(self):
        """Iterator of all four points in this rect's corners"""
        yield self.origin
        yield self.point_top_right
        yield self.point_bottom_right
        yield self.point_bottom_left

    @property
    def point_top_right(self):
        """Point at the top right corner of this rect"""
        return Point(self.origin.x + self.size.width - 1, self.origin.y)

    @property
    def point_bottom_left(self):
        """Point at the bottom left corner of this rect"""
        return Point(self.origin.x, int(self.origin.y + self.size.height - 1))

    @property
    def point_bottom_right(self):
        """Point at the bottom right corner of this rect"""
        return self.origin + self.size - Point(1, 1)

    def distance_to(self, other: Rect) -> float:
        """Return an approximate distance from this rect to another."""
        x, y = self.center
        other_x, other_y = other.center
        return abs(other_x - x) + abs(other_y - y)

    def relative_point(self, relative_width: float, relative_height: float) -> Point:
        """Find a point x% across the width and y% across the height. The
        arguments should be floats between 0 and 1.
        For example, `relative_point(0, 0)` returns the top left, and
        `relative_point(0.5, 0.5)` returns the center.
        """
        assert 0 <= relative_width <= 1
        assert 0 <= relative_height <= 1
        return Point(self.left + int((self.width - 1) * relative_width + 0.5),
                     self.top + int((self.height - 1) * relative_height + 0.5))

    # Directional Interactions

    def edge_length(self, edge: Direction) -> Real:
        """Use a Direction to get the length of the relevant edge."""
        if edge is Direction.up or edge is Direction.down:
            return self.width
        if edge is Direction.left or edge is Direction.right:
            return self.height
        raise ValueError("Expected an orthogonal Direction.")

    def edge_span(self, edge: Direction) -> Span:
        """Use a Direction to get a Span that starts and ends at
        opposite edges and crosses the centerpoint of this Rect."""
        if edge is Direction.up or edge is Direction.down:
            return self.horizontal_span
        if edge is Direction.left or edge is Direction.right:
            return self.vertical_span
        raise ValueError("Expected an orthogonal Direction.")

    def edge_point(self, edge: Direction, parallel: int, orthogonal: int) -> Point:
        """Return a point, relative to a particular edge.
        `parallel` is the absolute coordinate parallel to the given edge. For
        example, if `edge` is `Direction.top`, then `parallel` is the
        x-coordinate.
        `orthogonal` is the RELATIVE offset from the given edge, towards the
        interior of the rectangle. So for `Direction.top`, the y-coordinate is
        `self.top + orthogonal`.
        """
        if edge is Direction.up:
            return Point(parallel, self.top + orthogonal)
        elif edge is Direction.down:
            return Point(parallel, self.bottom - orthogonal)
        elif edge is Direction.left:
            return Point(parallel, self.left + parallel)
        elif edge is Direction.right:
            return Point(parallel, self.right - parallel)
        raise ValueError("Expected an orthogonal direction.")

    def replace(self, *,
            top: Optional[int] = None,
            bottom: Optional[int] = None,
            left: Optional[int] = None,
            right: Optional[int] = None
        ) -> Rect:
        """Get a new Rect derived from this one, optionally defined in terms
        of edge values. Providing values ot this method pass them as arguments
        to `Rect.from_edges()` constructor.

        Leave a parameter unfilled to get the current Rect's value for that
        parameter, or provide an integer to override.
        """
        if top is None:
            top = self.top
        if bottom is None:
            bottom = self.bottom
        if left is None:
            left = self.left
        if right is None:
            right = self.right
        return type(self).from_edges(top=top, bottom=bottom, left=left, right=right)

    def shift(self, *,
            top: int = 0,
            bottom: int = 0,
            left: int = 0,
            right: int = 0
        ) -> Rect:
        """Get a new Rect derived from this one, defined as offsets from the
        current Rect's values. The values provided for this method's parameters
        are passed to `Rect.from_edges()` constructor."""
        return type(self).from_edges(
            top=self.top + top,
            bottom=self.bottom + bottom,
            left=self.left + left,
            right=self.right + right,
            )

    def shrink(self, amount: int) -> Rect:
        """Get a new Rect derived from this one, defined as an integer offset
        applied to all sides."""
        new_left = self.left + amount
        new_right = self.right - amount
        if new_left > new_right:
            new_left = new_right = (self.left + self.right) // 2

        new_top = self.top + amount
        new_bottom = self.bottom - amount
        if new_top > new_bottom:
            new_top = new_bottom = (self.top + self.bottom) // 2

        return type(self).from_edges(
            top=new_top, bottom=new_bottom,
            left=new_left, right=new_right,
            )

    def iter_border(self) -> Generator[Point, None, None]:
        """Return Points for every x,y in the border of the Rect as well as
        a Direction object encoding the side of the given edge.

        Returns diagonal Directions for the corners of the Rect."""
        for x in range(self.left + 1, int(self.right)):
            yield Point(x, self.top), Direction.up
            yield Point(x, self.bottom), Direction.down
        for y in range(self.top + 1, int(self.bottom)):
            yield Point(self.left, y), Direction.left
            yield Point(self.right, y), Direction.right

        yield Point(self.left, self.top), Direction.up_left
        yield Point(self.right, self.top), Direction.up_right
        yield Point(self.left, self.bottom), Direction.down_left
        yield Point(self.right, self.bottom), Direction.down_right

    def iter_points(self) -> Generator:
        for x in range(int(self.left), self.right + 1):
            for y in range(int(self.top), self.bottom + 1):
                yield Point(x, y)

    def range_width(self):
        """Iterate over every x-coordinate within the width of the Rect."""
        return range(int(self.left), self.right + 1)

    def range_height(self):
        """Iterate over every y-coordinate within the height of the Rect."""
        return range(int(self.top), self.bottom + 1)

    def intersects(self, other: Rect) -> bool:
        """Returns True if this Rect overlaps with another at any point."""
        return (
            self.top <= other.bottom and
            self.bottom >= other.top and
            self.left <= other.right and
            self.right >= other.left
            )
