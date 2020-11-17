import pandas as pd
import numpy as np


def moving_mean(arr, n=None):
    result = np.cumsum(arr, dtype=float)
    n = n if n is not None else result.shape[0]
    result[n:] = result[n:] - result[:-n]
    return result[n-1: ] / n