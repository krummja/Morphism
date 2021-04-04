from __future__ import annotations

import unittest

from morphism import *


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.circ = Circ.from_edges(top=0, left=0, radius=10)
        self.rect = Rect.from_edges(top=0, left=0, right=10, bottom=10)
        self.point = Point(0, 0)
        self.size = Size(10, 1.0)
        self.span = Span(Point(0, 0), Point(0, 10))

    def testCircConstructor(self):
        self.assertTrue(self.circ)
        self.assertTrue(self.rect)
        self.assertTrue(self.point)
        self.assertTrue(self.size)
        self.assertTrue(self.span)


if __name__ == '__main__':
    unittest.main()
