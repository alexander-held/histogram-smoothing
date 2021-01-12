import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

plt.style.use("fivethirtyeight")

y = [
    7.82272339,
    20.79126453,
    55.58607231,
    80.9790969,
    61.72924992,
    48.02962419,
    55.53139849,
    38.1122083,
    37.5203016,
    24.89442078,
    33.42130301,
    34.15961964,
    11.99455817,
    90.5479646,
    58.71481196,
    88.95821081,
]
y_unc = np.ones_like(y) * 5


def smooth_lowess(y, y_unc):
    x = np.arange(len(y))
    rand_x = []
    rand_y = []
    n_points = 50
    for i, yi in enumerate(y):
        # loop over bins, generate random samples for each bin
        rand_y += list(np.random.normal(loc=yi, scale=y_unc[i], size=n_points))
        rand_x += list(np.random.normal(loc=x[i], scale=0.2, size=n_points))

    # https://www.statsmodels.org/stable/generated/statsmodels.nonparametric.smoothers_lowess.lowess.html
    y_smooth_full = sm.nonparametric.lowess(
        rand_y, rand_x, return_sorted=False, frac=0.5, it=3, delta=0.2
    )
    # get median prediction per bin
    y_smooth = []
    for i in range(len(x)):
        y_smooth.append(np.median(y_smooth_full[i * n_points : (i + 1) * n_points]))
    return y_smooth, rand_x, rand_y


y_smooth, rand_x, rand_y = smooth_lowess(y, y_unc)
x = np.arange(len(y))

# plotting
plt.bar(
    x,
    height=y,
    label="orig",
    fill=True,
    color="C2",
    edgecolor="C2",
    linewidth=2,
    width=1,
)
plt.bar(
    x,
    height=y_unc,
    bottom=y - y_unc / 2,
    fill=False,
    edgecolor="gray",
    hatch=3 * "/",
    linewidth=0,
    width=1,
)
plt.bar(
    x,
    height=y_smooth,
    label="smooth",
    fill=False,
    edgecolor="C1",
    linewidth=2,
    width=1,
)
plt.plot(rand_x, rand_y, ".")
plt.legend()
plt.savefig("lowess.pdf")
