"""
The rosenbrock objective function
"""

# pylint: disable=too-few-public-methods

from typing import List

from ..objective_function import ObjectiveFunction


class RosenbrockFunction(ObjectiveFunction):
    """
    Rosenbrock objective function.
    """

    def __init__(self, dim: int):
        """
        Class constructor.

        :param dim: dimensionality of the function.
        """
        super().__init__("rosenbrock", dim)

    def __call__(self, x: List[float]) -> float:
        """
        Evaluate a single point with the objective function.

        :param x: point to be evaluated
        :raises ValueError: if dimensionality of x doesn't match self.dim
        :return: value of the function in the provided point
        """
        super().__call__(x)
        return sum(
            100 * (x_i**2 - x_i_next) ** 2 + (x_i - 1) ** 2
            for x_i, x_i_next in zip(x, x[1:])
        )
