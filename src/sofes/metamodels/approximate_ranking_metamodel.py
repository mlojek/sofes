"""
Approximate ranking metamodel based on lmm-CMA-ES.
"""


class ApproximateRankingMetamodel:
    """Approximate ranking metamodel based on lmm-CMA-ES"""

    def __init__(self, input_size: int, popsize: int) -> None:
        self.input_size = input_size
        self.popsize = popsize

        self.n_init = input_size
        self.n_step = max(1, input_size // 10)

        self.train_set = []

        self.objective_function = None
        self.surrogate_function = None



    def placeholder1(self) -> None:
        """placeholder"""

    def placeholder2(self) -> None:
        """placeholder"""
