"""
Benchmarking CMA-ES algorithm on CEC 2017
"""

# pylint: disable=import-error

from cec2017.functions import all_functions
from run_cmaes_on_cec import run_cmaes_on_cec
from tqdm import tqdm

from sofes.data_classes import ExperimentMetadata, ExperimentResults

MAX_FES = 1e6
BOUNDS = [-100, 100]
SIGMA0 = 10
DIMS = [10]
POPSIZE_PER_DIM = 4
TOLERANCE = 1e-8
NUM_RUNS = 5


if __name__ == "__main__":
    functions = [
        (f"cec2017_f{i+1}", func, (i + 1) * 100) for i, func in enumerate(all_functions)
    ]

    metadata = ExperimentMetadata(
        "cmaes",
        {"sigme0": SIGMA0, "popsize_per_dim": 4},
        "",
        {"dummy": 42},
        "cec2017",
        "",
        "",
    )
    results = ExperimentResults(metadata)

    for name, function, target in functions[:5]:
        for dimension in DIMS:
            print(f"{name} dim {dimension}")
            maxes = [
                run_cmaes_on_cec(
                    function,
                    dimension,
                    POPSIZE_PER_DIM * dimension,
                    MAX_FES * dimension,
                    BOUNDS,
                    TOLERANCE,
                    target,
                    SIGMA0,
                )
                for _ in tqdm(range(NUM_RUNS))
            ]

            results.add_data(name, dimension, maxes)

    print(results.print_stats())
    results.save_to_json("cmaes_vanilla_cec2017.json")
    results.save_stats("cmaes_vanilla_cec2017.csv")
    results.plot_ecdf_curve(dim=10, savepath="cmaes_vanilla_cec2017_ecdf_10.png")
    results.plt_box_plot(savepath="cmaes_vanilla_cec2017_box.png")
