# import numpy as np

# def calculate_psi(expected, actual, bins):
#     """
#     expected: baseline values
#     actual: live batch values
#     bins: number of bins
#     """
#     expected_counts, bin_edges = np.histogram(expected, bins=bins)
#     actual_counts, _ = np.histogram(actual, bins=bin_edges)

#     expected_perc = expected_counts / len(expected)
#     actual_perc = actual_counts / len(actual)

#     # Avoid division by zero
#     expected_perc = np.where(expected_perc == 0, 1e-6, expected_perc)
#     actual_perc = np.where(actual_perc == 0, 1e-6, actual_perc)

#     psi = np.sum((actual_perc - expected_perc) * np.log(actual_perc / expected_perc))
#     return float(psi)

import numpy as np

def calculate_psi(expected, actual, buckets=10):
    """
    PSI using percentile-based bins (industry standard)
    """
    # Define bins using baseline percentiles
    breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))

    expected_counts = np.histogram(expected, bins=breakpoints)[0]
    actual_counts = np.histogram(actual, bins=breakpoints)[0]

    expected_perc = expected_counts / len(expected)
    actual_perc = actual_counts / len(actual)

    # Avoid division by zero
    expected_perc = np.where(expected_perc == 0, 1e-6, expected_perc)
    actual_perc = np.where(actual_perc == 0, 1e-6, actual_perc)

    psi = np.sum((actual_perc - expected_perc) * np.log(actual_perc / expected_perc))
    return float(psi)