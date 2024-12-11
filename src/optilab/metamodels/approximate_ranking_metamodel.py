"""
Approximate ranking metamodel based on lmm-CMA-ES.
"""

from typing import List, Tuple

from optilab.functions import ObjectiveFunction
from optilab.functions.surrogate import SurrogateObjectiveFunction


def rank_items(
    items: List[Tuple[List[float], float]]
) -> List[Tuple[List[float], float]]:
    """
    Given a list of x, y values, rank them in ascending order based on the y value.

    :param items: list of pairs of x, y values. y must be float.
    :return: the same list but sorted
    """
    return list(sorted(items, key=lambda x: x[1]))


class ApproximateRankingMetamodel:
    """Approximate ranking metamodel based on lmm-CMA-ES"""

    def __init__(
        self,
        input_size: int,
        popsize: int,
        objective_function: ObjectiveFunction,
        surrogate_function: SurrogateObjectiveFunction,
    ) -> None:
        """
        Class constructor.

        :param input_size: the number of input points to be evaluated (lambda).
        :param popsize: the size of CMA-ES population and number of points returned (mu).
        :param objective_function: the objective function that's being optimized.
        :param surrogate_function: surrogate objective function used to estimate
        the optimized function
        """
        self.input_size = input_size
        self.popsize = popsize

        self.n_init = input_size
        self.n_step = max(1, input_size // 10)

        self.train_set = []

        self.objective_function = objective_function
        self.surrogate_function = surrogate_function

    def _update_n(self, num_iters: int) -> None:
        """
        Updates n_init and n_step values base on the number of algorithm iterations.

        :param num_iters: the number of iterations done by the algorithm.
        """
        if num_iters > 2:
            self.n_init = min(self.n_init + self.n_step, self.input_size - self.n_step)
        elif num_iters < 2:
            self.n_init = max(self.n_step, self.n_init - self.n_step)

    def __call__(self, xs: List[List[float]]) -> List[Tuple[List[float], float]]:
        """
        Approximates the values of provided points with surrogate objective function.

        :param xs: list of points to be evaluated.
        :return: list of x, y value pairs where x is the point from xs and y is the estimated
        function value.
        """
        return [(x, self.surrogate_function(x)) for x in xs]

    def evaluate(self, xs: List[List[float]]) -> List[Tuple[List[float], float]]:
        """
        Evaluate provided point with the objective function and append results to the training
        set and retrain the surrogate function on new training data.

        :param xs: list of point to be evaluated with the objective function.
        :return: list of x, y values, where x are values provided in xs argument and ys are
        objective function values in these points.
        """
        result = [(x, self.objective_function(x)) for x in xs]
        self.train_set.extend(result)
        self.surrogate_function.train(self.train_set)
        return result

    def get_log(self) -> List[float]:
        """
        Returns the function values that were acquired from evaluation with the optimized
        function. This can also be treated as getting the results log of the optimization.

        :return: list of y values acquired from optimized function evaluation.
        """
        return [y for _, y in self.train_set]

    def adapt(self, xs: List[List[float]]) -> None:
        """
        Perform another loop of the optimization on new data.

        :param xs: solution candidates generated by optimizer.
        :raises ValueError: when number of provided points mismatches the expected input size.
        """
        if not len(xs) == self.input_size:
            raise ValueError(
                f"The number of provided points is different than expected."
                f"Expected {self.input_size}, got {len(xs)}."
            )

        if len(self.train_set) < self.input_size:
            self.evaluate(xs)
            return

        # 1 approximate
        items = self(xs)

        # 2 rank
        items_ranked = rank_items(items)
        items_mu_ranked = items_ranked[: self.popsize]

        # 3 evaluate and add to train set
        items_ranked[: self.n_init] = self.evaluate(
            [x for x, _ in items_ranked[: self.n_init]]
        )

        num_iter = 0
        for _ in range((self.input_size - self.n_init) // self.n_step):
            num_iter += 1
            # 6 retrain and approximate
            new_items = self(xs)

            # 7 rank
            new_items_ranked = rank_items(new_items)
            new_items_mu_ranked = new_items_ranked[: self.popsize]

            # 8 if rank change
            if [l[0] == r[0] for l, r in zip(new_items_mu_ranked, items_mu_ranked)]:
                break

            counter = 0
            to_eval = []
            for x in xs:
                for tmp_x, _ in self.train_set:
                    if not x == tmp_x:
                        counter += 1
                        to_eval.append(x)
                        break
                if counter >= self.n_step:
                    break
            items_mu_ranked = new_items_mu_ranked
            self.evaluate(to_eval)

        self._update_n(num_iter)
