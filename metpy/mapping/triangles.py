# Copyright (c) 2008-2015 MetPy Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import math

from scipy.spatial import cKDTree

def dist_2(x0, y0, x1, y1):
    '''Returns the squared distance between two points.

    This is faster than calculating distance but should
    only be used with comparable ratios.

    Parameters
    ----------
    x0: float
        Starting x coordinate
    y0: float
        Starting y coordinate
    x1: float
        Ending x coordinate
    y1: float
        Ending y coordinate

    Returns
    --------
    d2: float
        squared distance

    See Also
    --------
    distance
    '''

    d0 = x1 - x0
    d1 = y1 - y0
    return d0 * d0 + d1 * d1


def distance(p0, p1):
    '''Returns the distance between two points.

    Parameters
    ----------
    p0: (X,Y) ndarray
        Starting coordinate
    p1: (X,Y) ndarray
        Ending coordinate

    Returns
    --------
    d: float
        distance

    See Also
    --------
    dist_2
    '''

    return math.sqrt(dist_2(p0[0], p0[1], p1[0], p1[1]))


def circumcircle_radius_2(pt0, pt1, pt2):
    '''Calculates and returns the squared radius of a
    given triangle's circumcircle.

    This is faster than calculating radius but should
    only be used with comparable ratios.

    Parameters
    ----------
    pt0: (x, y)
        Starting vertex of triangle
    pt1: (x, y)
        Second vertex of triangle
    pt2: (x, y)
        Final vertex of a triangle

    Returns
    --------
    r: float
        circumcircle radius

    See Also
    --------
    circumcenter
    '''

    a = distance(pt0, pt1)
    b = distance(pt1, pt2)
    c = distance(pt2, pt0)

    s = (a+b+c) * 0.5

    prod = s * (s-a) * (s-b) * (s-c)
    prod2 = a * b * c

    radius = prod2 * prod2 / (16*prod)

    return radius

def circumcircle_radius(pt0, pt1, pt2):
    '''Calculates and returns the radius of a given
    triangle's circumcircle.

    Parameters
    ----------
    pt0: (x, y)
        Starting vertex of triangle
    pt1: (x, y)
        Second vertex of triangle
    pt2: (x, y)
        Final vertex of a triangle

    Returns
    --------
    r: float
        circumcircle radius

    See Also
    --------
    circumcenter
    '''

    a = distance(pt0, pt1)
    b = distance(pt1, pt2)
    c = distance(pt2, pt0)

    s = (a+b+c) * 0.5

    prod = s * (s-a) * (s-b) * (s-c)
    prod2 = a* b * c

    radius = prod2 / (4*math.sqrt(prod))

    return radius


def circumcenter(pt0, pt1, pt2):
    '''Calculates and returns the circumcenter of
    a circumcircle generated by a given triangle.
    All three points must be unique or a division
    by zero error will be raised.

    Parameters
    ----------
    pt0: (x, y)
        Starting vertex of triangle
    pt1: (x, y)
        Second vertex of triangle
    pt2: (x, y)
        Final vertex of a triangle

    Returns
    --------
    cc: (x, y)
        circumcenter coordinates

    See Also
    --------
    circumcenter
    '''

    a_x = pt0[0]
    a_y = pt0[1]
    b_x = pt1[0]
    b_y = pt1[1]
    c_x = pt2[0]
    c_y = pt2[1]

    bc_y_diff = b_y - c_y
    ca_y_diff = c_y - a_y
    ab_y_diff = a_y - b_y
    cb_x_diff = c_x - b_x
    ac_x_diff = a_x - c_x
    ba_x_diff = b_x - a_x

    d_div = (a_x*bc_y_diff + b_x*ca_y_diff + c_x*ab_y_diff)

    if d_div == 0:
        raise ZeroDivisionError

    d_inv = 0.5 / (a_x*bc_y_diff + b_x*ca_y_diff + c_x*ab_y_diff)

    a_mag = a_x*a_x + a_y*a_y
    b_mag = b_x*b_x + b_y*b_y
    c_mag = c_x*c_x + c_y*c_y

    cx = (a_mag*bc_y_diff + b_mag*ca_y_diff + c_mag*ab_y_diff) * d_inv
    cy = (a_mag*cb_x_diff + b_mag*ac_x_diff + c_mag*ba_x_diff) * d_inv

    return cx, cy


def find_natural_neighbors(tri, grid_points):
    '''Returns the natural neighbor triangles for
    each given grid cell determined by the proper-
    ties of the given delaunay triangulation.

    A triangle is a natural neighbor of a grid cell
    if that triangles circumcenter is within the
    circumradius of the grid cell center.

    Parameters
    ----------
    tri: Object
        A Delaunay Triangulation
    cur_tri: int
        Simplex code for Delaunay Triangulation lookup of
        a given triangle that contains 'position'.
    position: (x, y)
        Coordinates used to calculate distances to
        simplexes in 'tri'.

    Returns
    --------
    nn: (N, ) array
        List of simplex codes for natural neighbor
        triangles in 'tri'.
    '''

    tree = cKDTree(grid_points)

    in_triangulation = tri.find_simplex(tree.data) >= 0

    triangle_info = dict()
	
    members = dict((key, []) for key in range(len(tree.data)))

    for i in range(len(tri.simplices)):

        ps = tri.points[tri.simplices[i]]

        cc = circumcenter(*ps)
        r = circumcircle_radius(*ps)

        triangle_info[i] = {'cc': cc, 'r': r}

        qualifiers = tree.query_ball_point(cc, r)

        for qualifier in qualifiers:
            if in_triangulation[qualifier]:
                members[qualifier].append(i)

    return members, triangle_info


def find_local_boundary(tri, triangles):
    '''Finds and returns the outside edges of a collection
    of natural neighbor triangles.  There is no guarantee
    that this boundary is convex, so ConvexHull is not
    sufficient in some situations.

    Parameters
    ----------
    tri: Object
        A Delaunay Triangulation
    triangles: (N, ) array
        list of
    position: (x, y)
        Coordinates used to calculate distances to
        simplexes in 'tri'.

    Returns
    --------
    nn: (N, ) ndarray
        List of simplex codes for natural neighbor
        triangles in 'tri'.
    '''

    edges = []

    for triangle in triangles:

        for i in range(3):

            pt1 = tri.simplices[triangle][i]
            pt2 = tri.simplices[triangle][(i + 1) % 3]

            if (pt1, pt2) in edges:
                edges.remove((pt1, pt2))

            elif (pt2, pt1) in edges:
                edges.remove((pt2, pt1))

            else:
                edges.append((pt1, pt2))

    return edges
