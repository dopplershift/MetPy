# Copyright (c) 2008-2015 MetPy Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import warnings
import copy


class MetpyMap(object):

    def __init__(self, options):

        if 'data_file' not in options:

            raise ValueError("You must specify 'data_file'")

        if 'variable_to_plot' not in options:

            raise ValueError("You must specify 'variable_to_plot'")

        if 'data_type' not in options:

            data_type = options['data_file'].split('.')[-1]
            options['data_type'] = data_type
            message = ("data_type not specified, will assume " + str(data_type) +
                       " based on filename.")

            warnings.warn(message)

        self.optional_params = ["title", "process_area", "map_params", "datetime",
                                "projection_options"]

        self.required_params = ["data_file", "data_type", "variable_to_plot"]

        self.params = dict()

        for key, item in options.items():
            if key in self.optional_params or key in self.required_params:
                self.params[key] = options[key]
            else:
                raise ValueError("Unrecognized parameter: " + str(key))

    def add(self, parameters, values):

        for key, val in list(zip(parameters, values)):
            if key in self.optional_params or key in self.required_params:
                self.params[key] = val
            else:
                raise ValueError("Unrecognized parameter: " + str(key))

    def remove(self, parameters):

        for key in parameters:
            if key in self.params:
                if key not in self.required_params:
                    self.params.pop(key, None)
                else:
                    raise ValueError("Cannot remove required parameter " + str(key))
            else:
                message = str(key) + " was not found in parameters list."
                warnings.warn(message)

    def update(self, parameters, values):

        for key, val in list(zip(parameters, values)):
            if key in self.params:
                self.params[key] = val
            else:
                message = str(key) + " was not found in parameters list."
                warnings.warn(message)


class StationMap(MetpyMap):

    def __init__(self, options):

        opts = copy.deepcopy(options)

        MetpyMap.__init__(self, opts)

        self.optional_params.append('radar_fill')
        self.optional_params.append('satellite_fill')

        if 'radar_fill' in opts:
            self.params['radar_fill'] = opts['radar_fill']

        if 'satellite_fill' in opts:
            self.params['radar_fill'] = opts['radar_fill']


class SoundingMap(StationMap):

    def __init__(self, options):

        opts = copy.deepcopy(options)

        if 'vertical_levels' not in opts:
            raise ValueError("Must specify vertical level(s) to plot")

        vertical_levels = opts.pop('vertical_levels')
        coord_type = None

        if 'vertical_coord_type' in opts:
            coord_type = opts.pop('vertical_coord_type')

        StationMap.__init__(self, opts)

        self.required_params.append('vertical_levels')
        self.optional_params.append('vertical_coord_type')

        self.params['vertical_levels'] = vertical_levels

        if coord_type is not None:
            self.params['vertical_coord_type'] = coord_type


class GridMap(MetpyMap):

    def __init__(self, options):

        opts = copy.deepcopy(options)

        if 'analysis_parameters' not in options:
            raise ValueError("Must specify analysis options.")

        if 'horizontal_resolution' not in options:
            raise ValueError("Must specify horizontal resolution.")

        analy_params = opts.pop('analysis_parameters')
        horiz_resolution = opts.pop('horizontal_resolution')

        MetpyMap.__init__(self, opts)

        self.required_params.append('analysis_parameters')
        self.required_params.append('horizontal_resolution')

        self.optional_params.append('grid')

        self.params['analysis_parameters'] = analy_params
        self.params['horizontal_resolution'] = horiz_resolution

        if 'grid' in opts:

            self.params['grid'] = opts['grid']
