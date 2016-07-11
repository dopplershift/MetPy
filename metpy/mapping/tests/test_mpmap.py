# Copyright (c) 2008-2015 MetPy Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

from datetime import datetime
import numpy as np

from metpy.mapping.mpmap import MetpyMap

from numpy.testing import assert_array_almost_equal


def test_add():

    options = {"data_file": "C:/Documents/Stuff.txt",
               "data_type": "txt",
               "variable_to_plot": "air_temperature"}

    gmap = MetpyMap(options)

    gmap.add(["a", "b"], [1, 2])

    truth_keys = np.array(["a", "b", "data_file", "data_type", "variable_to_plot"])

    truth_values = np.array([1, 2, "C:/Documents/Stuff.txt", "txt", "air_temperature"])

    sorted_keys = sorted(gmap.params.keys())
    sorted_truth_values = [gmap.params[p] for p in sorted_keys]

    assert (all(truth_keys == sorted_keys))
    assert (all(truth_values == sorted_truth_values))


def test_remove():

    options = {"data_file": "C:/Documents/Stuff.txt",
               "data_type": "txt",
               "variable_to_plot": "air_temperature",
               "datetime": datetime.now()}

    gmap = MetpyMap(options)

    gmap.remove(["datetime"])

    truth_keys = np.array(["data_file", "data_type", "variable_to_plot"])

    truth_values = np.array(["C:/Documents/Stuff.txt", "txt", "air_temperature"])

    sorted_keys = sorted(gmap.params.keys())
    sorted_truth_values = [gmap.params[p] for p in sorted_keys]

    assert (all(truth_keys == sorted_keys))
    assert (all(truth_values == sorted_truth_values))


def test_update():

    options = {"data_file": "C:/Documents/Stuff.txt",
               "data_type": "txt",
               "variable_to_plot": "air_temperature"}

    gmap = MetpyMap(options)

    gmap.update(["data_file"], ["C:/Documents/different_stuff.txt"])

    truth_keys = np.array(["data_file", "data_type", "variable_to_plot"])

    truth_values = np.array(["C:/Documents/different_stuff.txt", "txt", "air_temperature"])

    sorted_keys = sorted(gmap.params.keys())
    sorted_truth_values = [gmap.params[p] for p in sorted_keys]

    assert (all(truth_keys == sorted_keys))
    assert (all(truth_values == sorted_truth_values))
