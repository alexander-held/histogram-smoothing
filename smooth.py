import matplotlib.pyplot as plt
import numpy as np

import histogram_smoothing


def print_results(hist):
    for h in hist:
        print(f"{h:.4f}", end="   ")
    print()


if __name__ == "__main__":
    plt.style.use("fivethirtyeight")
    # fmt: off
    hist = [
        7.82272339, 20.79126453, 55.58607231, 80.9790969,
        61.72924992, 48.02962419, 55.53139849, 38.1122083,
        37.5203016, 24.89442078, 33.42130301, 34.15961964,
        11.99455817, 90.5479646, 18.71481196, 88.95821081,
    ]
    ref = np.asarray([
        7.822723, 26.247831, 51.234443, 68.039891,
        66.855977, 55.680763, 45.094336, 38.695053,
        36.060684, 34.446053, 33.421303, 33.421303,
        33.605882, 47.674688, 75.258563, 88.958211
    ])
    # fmt: on
    nbins = len(hist)
    print("original array:")
    print_results(hist)
    hist_smooth = histogram_smoothing.SmoothArray(hist)
    print("\nsmooth array:")
    print_results(hist_smooth)

    # compare to reference taken from ROOT
    print("diff > 1e4:", [xi for xi in (hist_smooth - ref) if abs(xi) > 1e-4])
    assert np.allclose(hist_smooth, ref)

    bin_centers = np.arange(nbins)
    plt.bar(
        bin_centers,
        height=hist,
        label="orig",
        fill=True,
        color="C2",
        edgecolor="C2",
        linewidth=2,
        width=1,
    )
    plt.bar(
        bin_centers,
        height=hist_smooth,
        label="smooth",
        fill=False,
        edgecolor="C1",
        linewidth=2,
        width=1.0,
    )
    plt.legend()
    plt.savefig("hist.pdf")
