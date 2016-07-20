# Copyright (c) 2008-2015 MetPy Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

from libc.math cimport sqrt, fabs
import cython

def _area(pt1, pt2, pt3):

    cdef:
        double x0
        double y0
        double x1
        double y1
        double x2
        double y2

    x0, y0 = pt1
    x1, y1 = pt2
    x2, y2 = pt3

    return c_area(x0, y0, x1, y1, x2, y2)

cdef double c_area(double x0, double y0, double x1, double y1, double x2, double y2):

    cdef double a

    a = (x0 * y1 - x1 * y0) + (x1 * y2 - x2 * y1) + (x2 * y0 - x0 * y2)

    return fabs(a) * 0.5


@cython.cdivision(True)
def _circumcircle_radius(pt1, pt2, pt3):
    cdef:
        double x0
        double y0
        double x1
        double y1
        double x2
        double y2
        double a

    x0, y0 = pt1
    x1, y1 = pt2
    x2, y2 = pt3

    a = _area(pt1, pt2, pt3)

    return c_circumcircle_radius(x0, y0, x1, y1, x2, y2, a)

cdef double c_dist_2(double x0, double y0, double x1, double y1):

    cdef:
        double d0
        double d1

    d0 = x1 - x0
    d1 = y1 - y0

    return d0 * d0 + d1 * d1


cdef double c_circumcircle_radius(double x0, double y0, double x1,
                                  double y1, double x2, double y2,
                                  double area):

    cdef:
        double a
        double b
        double c
        double s
        double prod
        double radius

    radius = -99.00

    if area > 0:

        a = c_dist_2(x0, y0, x1, y1)
        b = c_dist_2(x1, y1, x2, y2)
        c = c_dist_2(x2, y2, x0, y0)

        prod = a * b * c

        radius = sqrt(prod) / (4 * area)

    return radius