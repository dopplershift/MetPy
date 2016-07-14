from libc.math cimport sqrt
import numpy as np


def _circumcenter(pt1, pt2, pt3):

    x0, y0 = pt1
    x1, y1 = pt2
    x2, y2 = pt3

    return c_circumcenter(x0, y0, x1, y1, x2, y2)


cdef c_circumcenter(double x0, double y0, double x1, double y1, double x2, double y2):

    cdef:
        double bc_y_diff = y1 - y2
        double ca_y_diff = y2 - y0
        double ab_y_diff = y0 - y1
        double d_inv = 0.5 / (x0 * bc_y_diff + x1 * ca_y_diff + x2 * ab_y_diff)
        double a_mag = x0 * x0 + y0 * y0
        double b_mag = x1 * x1 + y1 * y1
        double c_mag = x2 * x2 + y2 * y2
        double cx
        double cy

    cx = (a_mag * bc_y_diff + b_mag * ca_y_diff + c_mag * ab_y_diff) * d_inv
    cy = (a_mag * (x2 - x1) + b_mag * (x0 - x2) + c_mag * (x1 - x0)) * d_inv

    return cx, cy


def _dist_2(double x0, double y0, double x1, double y1):

    return c_dist_2(x0, y0, x1, y1)


cdef double c_dist_2(double x0, double y0, double x1, double y1):

    cdef:
        double d0
        double d1

    d0 = x1 - x0
    d1 = y1 - y0

    return d0 * d0 + d1 * d1


cdef double _distance(double x0, double y0, double x1, double y1):

    return sqrt(c_dist_2(x0, y0, x1, y1))


def _circumcircle_radius(pt1, pt2, pt3):

    x0, y0 = pt1
    x1, y1 = pt2
    x2, y2 = pt3

    return c_circumcircle_radius(x0, y0, x1, y1, x2, y2)


cdef double c_circumcircle_radius(double x0, double y0, double x1, double y1, double x2, double y2):

    cdef:
        double a = _distance(x0, y0, x1, y1)
        double b = _distance(x1, y1, x2, y2)
        double c = _distance(x2, y2, x0, y0)
        double s = (a + b + c) * 0.5
        double prod = s*(a+b-s)*(a+c-s)*(b+c-s)
        double prod2 = a*b*c
        double radius = prod2 * prod2 / (16*prod)

    return radius
