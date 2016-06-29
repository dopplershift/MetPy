# Copyright (c) 2008-2015 MetPy Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

from metpy.mapping.points import *
from numpy.testing import assert_array_almost_equal


def test_get_points_within_r():

    x = list(range(10))
    y = list(range(10))

    center = [1, 5]

    radius = 5

    matches = get_points_within_r(center, list(zip(x, y)), radius).T

    truth = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]

    assert_array_almost_equal(truth, matches)


def test_get_point_count_within_r():

    x = list(range(10))
    y = list(range(10))

    center1 = [1, 5]
    center2 = [12, 10]

    radius = 5

    count = get_point_count_within_r([center1, center2], list(zip(x, y)), radius)

    truth = np.array([5, 2])

    assert_array_almost_equal(truth, count)


def test_get_boundary_coords():

    x = list(range(10))
    y = list(range(10))

    bbox = get_boundary_coords(x, y)

    east_truth  = 9
    north_truth = 9
    south_truth = 0
    west_truth = 0

    assert_array_almost_equal(north_truth, bbox['north'])
    assert_array_almost_equal(south_truth, bbox['south'])
    assert_array_almost_equal(east_truth, bbox['east'])
    assert_array_almost_equal(west_truth, bbox['west'])

    bbox = get_boundary_coords(x, y, 10)

    north_truth = 19
    south_truth = -10
    east_truth = 19
    west_truth = -10

    assert_array_almost_equal(north_truth, bbox['north'])
    assert_array_almost_equal(south_truth, bbox['south'])
    assert_array_almost_equal(east_truth, bbox['east'])
    assert_array_almost_equal(west_truth, bbox['west'])


def test_get_xy_steps():

    x = list(range(10))
    y = list(range(10))

    bbox = get_boundary_coords(x, y)

    x_steps, y_steps = get_xy_steps(bbox, 3)

    truth_x = 3
    truth_y = 3

    assert x_steps == truth_x
    assert y_steps == truth_y


def test_get_xy_range():

    x = list(range(10))
    y = list(range(10))

    bbox = get_boundary_coords(x, y)

    x_range, y_range = get_xy_range(bbox)

    truth_x = 9
    truth_y = 9

    assert truth_x == x_range
    assert truth_y == y_range


def test_generate_grid():

    x = list(range(10))
    y = list(range(10))

    bbox = get_boundary_coords(x, y)

    gx, gy = generate_grid(3, bbox, ignore_warnings=True)

    truth_x = np.array([[0.0, 4.5, 9.0],
                        [0.0, 4.5, 9.0],
                        [0.0, 4.5, 9.0]])

    truth_y = np.array([[0.0, 0.0, 0.0],
                        [4.5, 4.5, 4.5],
                        [9.0, 9.0, 9.0]])

    assert_array_almost_equal(gx, truth_x)
    assert_array_almost_equal(gy, truth_y)


def test_generate_grid_coords():

    x = list(range(10))
    y = list(range(10))

    bbox = get_boundary_coords(x, y)

    gx, gy = generate_grid(3, bbox, ignore_warnings=True)

    truth = [[0.0, 0.0],
             [4.5, 0.0],
             [9.0, 0.0],
             [0.0, 4.5],
             [4.5, 4.5],
             [9.0, 4.5],
             [0.0, 9.0],
             [4.5, 9.0],
             [9.0, 9.0]]

    pts = generate_grid_coords(gx, gy)

    assert_array_almost_equal(truth, pts)