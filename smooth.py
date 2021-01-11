# import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("fivethirtyeight")


def print_results(xx):
    for i in range(len(xx)):
        print(xx[i], end="   ")
    print()


def root_median(n, w):
    # https://root.cern.ch/root/html524/TMath.html#TMath:Median
    # first parameter is array size (only take first n entries)
    w_sorted = sorted(w[0:n])
    if n % 2 == 0:
        raise NotImplementedError
    else:
        k = int((n + 1) / 2) - 1
    return w_sorted[k]


def SmoothArray(nbins, xx):
    if nbins < 3:
        print("need at least three points for smoothing")
        return

    hh = [0, 0, 0, 0, 0, 0]  # edges?

    yy = [None for _ in range(nbins)]
    zz = xx.copy()
    rr = [None for _ in range(nbins)]

    for _ in range(2):  # run median algorithm twice
        # do running median 3,5,3
        for kk in range(3):
            yy = zz.copy()  # zz is a copy of input, but then changes
            medianType = 3 if kk != 1 else 5
            ifirst = 1 if kk != 1 else 2
            ilast = nbins - 1 if kk != 1 else nbins - 2
            # do central elements first in (ifirst, ilast) range
            for ii in range(ifirst, ilast):
                assert ii - ifirst >= 0
                for jj in range(medianType):
                    hh[jj] = yy[ii - ifirst + jj]
                zz[ii] = root_median(medianType, hh)

            if kk == 0:  # first median 3
                # first bin
                hh[0] = zz[1]
                hh[1] = zz[0]
                hh[2] = 3 * zz[1] - 2 * zz[2]
                zz[0] = root_median(3, hh)
                # last bin
                hh[0] = zz[nbins - 2]
                hh[1] = zz[nbins - 1]
                hh[2] = 3 * zz[nbins - 2] - 2 * zz[nbins - 3]
                zz[nbins - 1] = root_median(3, hh)

            if kk == 1:  # median 5
                for ii in range(3):
                    hh[ii] = yy[ii]
                zz[1] = root_median(3, hh)
                # last two points
                for ii in range(3):
                    hh[ii] = yy[nbins - 3 + ii]
                zz[nbins - 2] = root_median(3, hh)

        print("end of median step")
        print("zz:", end=" ")
        print_results(zz)
        print("hh:", end=" ")
        print_results(hh)
        return zz


if __name__ == "__main__":
    nbins = 5
    xx = [10, 12, 16, 13, 16]
    nbins = 16
    xx = [
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
        18.71481196,
        88.95821081,
    ]
    print_results(xx)
    zz = SmoothArray(nbins, xx)

    bin_centers = np.arange(nbins)
    plt.bar(
        bin_centers,
        height=xx,
        label="orig",
        fill=True,
        color="C2",
        edgecolor="C2",
        linewidth=2,
        width=1,
    )
    plt.bar(
        bin_centers,
        height=zz,
        label="smooth",
        fill=False,
        edgecolor="C1",
        linewidth=2,
        width=1.0,
    )
    plt.legend()
    plt.savefig("hist.pdf")
