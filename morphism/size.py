from __future__ import annotations
from math import floor
from typing import Type


class Size(tuple):
    """Base class for defining a 2D area.

    Supports floor division.
    """

    def __new__(cls: Type[Size], width: int = 0, height: float = 0) -> Size:
        return super().__new__(cls, (width, height))

    def __floordiv__(self, n) -> Size:
        if not isinstance(n, (int, float)):
            return NotImplemented
        return Size(self[0] // n, self[1] // n)

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def floored(self):
        """A copy of this rect with the :py:attr:`Point.floored` origin/size
        copies"""
        return Size(floor(self.width), floor(self.height))

    @property
    def height(self) -> float:
        return self[1]

    @property
    def width(self) -> int:
        return self[0]
