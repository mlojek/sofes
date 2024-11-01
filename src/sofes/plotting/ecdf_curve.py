"""
Plotting and calculating ECDF curves.
"""

# pylint: disable=too-many-locals

import math
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np

from .convergence_curve import convergence_curve


def _ecdf_thresholding(
    log: List[float],
    thresholds: List[float],
    n_dimensions: int,
    extend_to_len: int = None,
) -> Tuple[List[float], List[float]]:
    """
    Perform thresholding of a log with a given list of thresholds.
    The resulting y is the number of thresholds achieved by the log items.

    :param log: error log of a optimization function
    :param thresholds: ecdf value thresholds
    :n_dimensions: number of optimized function dimensions
    :return: x and y values for the curve
    """
    y = [np.sum(thresholds >= item) / len(thresholds) for item in log]

    if extend_to_len:
        if extend_to_len < len(y):
            raise ValueError(
                "extend_to_len parameter is lower than lenght of the provided log"
            )
        while len(y) < extend_to_len:
            y.append(y[-1])

    x = [(i + 1) / n_dimensions for i in range(len(y))]

    return x, y


def ecdf_curve(
    data: Dict[str, List[List[float]]],
    n_dimensions: int = 1,
    n_thresholds: int = 100,
    allowed_error: float = 1e-8,
) -> Dict[str, Tuple[List[float], List[float]]]:
    """
    Calculate ecdf curves.

    :param data: dictionary containing list of value logs indexed by method name.
    :param n_dimensions: dimensionality of the solved problem
    :param n_thresholds: number of ecdf thresholds
    :param allowed_error: tolerable error value. This value will be used as the last threshold.
    :return: dictionary indexed with method name and containing x and y values of the curve.
    """
    processed_logs = {}
    log_lengths = {}
    all_last_items = []

    for method, logs in data.items():
        processed_logs[method] = []
        max_len = 0
        for log in logs:
            new_log = convergence_curve(log)
            max_len = max(max_len, len(new_log))
            processed_log = [math.log10(v) for v in new_log]
            processed_logs[method].append(processed_log)
            all_last_items.append(processed_log[-1])
            log_lengths[method] = max_len

    low_value = math.log10(allowed_error)
    high_value = max(all_last_items)

    thresholds = np.linspace(low_value, high_value, n_thresholds + 1)[1:]

    ecdf_data = {}
    for method, logs in processed_logs.items():
        ecdf_ys = []
        ecdf_x = []

        for log in logs:
            x, y = _ecdf_thresholding(
                log, thresholds, n_dimensions, log_lengths[method]
            )
            ecdf_x = x
            ecdf_ys.append(y)

        ecdf_avg = np.mean(ecdf_ys, axis=0)
        ecdf_data[method] = (ecdf_x, ecdf_avg)

    return ecdf_data


def plot_ecdf_curves(
    data: Dict[str, List[List[float]]],
    n_dimensions: int = 1,
    n_thresholds: int = 100,
    allowed_error: float = 1e-8,
    savepath: str = None,
) -> None:
    """
    Calculate and plot ecdf curves.

    :param data: dictionary containing list of value logs indexed by method name.
    :param n_dimensions: dimensionality of the solved problem
    :param n_thresholds: number of ecdf thresholds
    :param allowed_error: tolerable error value. This value will be used as the last threshold.
    :param savepath: optional, path to save the plot
    """
    plt.clf()

    ecdf_data = ecdf_curve(data, n_dimensions, n_thresholds, allowed_error)

    for method, (x, y) in ecdf_data.items():
        plt.plot(x, y, label=method)

    plt.xlabel("Number of function evaluations divided by the number of dimensions.")
    plt.xscale("log")
    plt.ylabel("ECDF point pairs")
    plt.title("ECDF Curves")

    plt.legend()
    plt.grid(True)

    if savepath:
        plt.savefig(savepath)

    plt.show()
