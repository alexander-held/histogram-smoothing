import statistics
from typing import List


def SmoothArray(xx: List[float]) -> List[float]:
    """Runs the 353QH algorithm twice and returns smooth version of the input.

    For documentation see these proceedings https://cds.cern.ch/record/186223/ on page
    292. The algorithm runs twice to avoid over-smoothing peaks and valleys. The
    algorithm is not aware of statistical uncertainties per entry in the array. See also
    the ROOT implementation https://root.cern.ch/doc/master/TH1_8cxx_source.html#l06725.

    Args:
        xx (List[float]): array to smooth

    Returns:
        List[float]: smooth version of input
    """
    nbins = len(xx)
    if nbins < 3:
        print("need at least three points for smoothing")
        return xx

    zz = xx.copy()

    for i_353QH in range(2):  # run 353QH twice
        # do running median with window sizes 3, 5, 3
        for kk in range(3):
            yy = zz.copy()  # yy stays constant at each step in the loop
            medianType = 3 if kk != 1 else 5
            ifirst = 1 if kk != 1 else 2
            ilast = nbins - 1 if kk != 1 else nbins - 2
            # do central elements first in (ifirst, ilast) range
            for ii in range(ifirst, ilast):
                zz[ii] = statistics.median(yy[ii - ifirst : ii - ifirst + medianType])

            if kk == 0:  # first median 3
                # first bin, proceedings use y_1 (=yy[0]), while ROOT uses zz[0]
                zz[0] = statistics.median([3 * zz[1] - 2 * zz[2], yy[0], zz[1]])
                # last bin, proceedings use y_n (=yy[-1]), while ROOT uses zz[-1]
                zz[-1] = statistics.median([zz[-2], yy[-1], 3 * zz[-2] - 2 * zz[-3]])

            if kk == 1:  # median 5
                zz[1] = statistics.median(yy[0:3])
                # second to last bin
                zz[-2] = statistics.median(yy[-3:])

        yy = zz.copy()

        # quadratic interpolation for flat segments
        for ii in range(2, nbins - 2):
            if zz[ii - 1] != zz[ii]:
                continue  # not flat
            if zz[ii] != zz[ii + 1]:
                continue  # not flat
            left_larger = zz[ii - 2] - zz[ii]  # two bins left larger by this amount
            right_larger = zz[ii + 2] - zz[ii]  # two bins right larger by this amount
            if left_larger * right_larger <= 0:
                continue  # current position is part of larger scale slope
            jk = 1
            if abs(right_larger) > abs(left_larger):
                jk = -1  # left is more flat than right
            yy[ii] = -0.5 * zz[ii - 2 * jk] + zz[ii] / 0.75 + zz[ii + 2 * jk] / 6
            yy[ii + jk] = 0.5 * (zz[ii + 2 * jk] - zz[ii - 2 * jk]) + zz[ii]

        # running means
        for ii in range(1, nbins - 1):
            zz[ii] = 0.25 * yy[ii - 1] + 0.5 * yy[ii] + 0.25 * yy[ii + 1]
        zz[0] = yy[0]
        zz[-1] = yy[-1]

        if i_353QH == 0:
            # algorithm has been run once
            rr = zz.copy()  # save computed values
            # calculate residuals: (original) - (after 353QH)
            zz = [xx[ii] - zz[ii] for ii in range(0, nbins)]
            # zz is now "rough", while rr is "smooth"

        # "twicing": run 353QH again on "rough" zz and add to "smooth" rr

    xmin = min(xx)
    xx_new = xx.copy()  # histogram after smoothing
    for ii in range(nbins):
        if xmin < 0:
            xx_new[ii] = rr[ii] + zz[ii]
        # result is positive if no negative values are in input
        else:
            xx_new[ii] = max(rr[ii] + zz[ii], 0)
    return xx_new
