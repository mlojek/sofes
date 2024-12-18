"""
Cumulative squared sums function.
"""

# pylint: disable=too-few-public-methods

from ...data_classes import Point
from ..objective_function import ObjectiveFunction


class CumulativeSquaredSums(ObjectiveFunction):
    """
    Cumulative squared sums function.
    """

    def __init__(self, dim: int):
        """
        Class constructor.

        Args:
            dim (int): Dimensionality of the function.
        """
        super().__init__("cumulative_squared_sums", dim)

    def __call__(self, point: Point) -> Point:
        """
        Evaluate a single point with the objective function.

        Args:
            point (Point): Point to evaluate.

        Raises:
            ValueError: If dimensionality of x doesn't match self.dim.

        Returns:
            Point: Evaluated point.
        """
        super().__call__(point)
        return Point(
            x=point.x,
            y=sum(sum(point.x[:i]) ** 2 for i in range(point.dim())),
            is_evaluated=True,
        )
