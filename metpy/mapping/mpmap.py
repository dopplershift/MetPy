# Copyright (c) 2008-2015 MetPy Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import warnings
import copy

import cartopy

import numpy as np
import matplotlib.pyplot as plt

from metpy.cbook import get_test_data
from metpy.plots import StationPlot
from metpy.calc import get_wind_components
from metpy.units import units

from siphon.catalog import TDSCatalog
from siphon.ncss import NCSS
from datetime import datetime

class MetpyMap(object):

    def __init__(self, options):

        if 'data_location' not in options:
            raise ValueError("You must specify 'data_location'")

        if 'data_type' not in options:

            if "http" in options['data_location']:
                options['data_type'] = "web"

            else:
                data_type = options['data_location'].split('.')[-1]
                options['data_type'] = data_type
                message = ("data_type not specified, will assume " + str(data_type) +
                           " based on filename.")

            warnings.warn(message)

        self.optional_params = ["title", "process_area", "map_params", "datetime",
                                "projection_options"]

        self.required_params = ["data_file", "data_type"]

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

    def draw_map(self, view):

        bbox = self.params['map_params']['bbox']

        view.set_extent([bbox['west'], bbox['east'], bbox['south'], bbox['north']])

        features = self.params['map_params']['features']

        if "states" in features:
            features.remove("states")
            view.add_feature(cartopy.feature.NaturalEarthFeature(
                category='cultural',
                name='admin_1_states_provinces_lakes',
                scale='50m',
                facecolor='none'))
        if "ocean" in features:
            features.remove("ocean")
            view.add_feature(cartopy.feature.OCEAN)
        if "coastlines" in features:
            features.remove("coastlines")
            view.add_feature(cartopy.feature.COASTLINE)
        if "countries" in features:
            features.remove("countries")
            view.add_feature(cartopy.feature.BORDERS, linestyle=':')

        if len(features) > 0:
            message = "Did not recognize the following features: "
            for f in features:
                message += str(f) + " "
            warnings.warn(message)

        return view


class StationMap(MetpyMap):

    def __init__(self, options):

        opts = copy.deepcopy(options)

        satellite_fill = None
        radar_fill = None

        if 'radar_fill' in opts:
            radar_fill = opts.pop('radar_fill')

        if 'satellite_fill' in opts:
            satellite_fill = opts.pop('satellite_fill')

        MetpyMap.__init__(self, opts)

        self.optional_params.append('radar_fill')
        self.optional_params.append('satellite_fill')

        if satellite_fill is not None:
            self.params['satellite_fill'] = satellite_fill

        if radar_fill is not None:
            self.params['radar_fill'] = satellite_fill

        if self.params['data_type'] == 'txt':
            self.data = self.load_text()

    def load_text(self):

        f = get_test_data(self.params['data_file'])

        all_data = np.loadtxt(f, skiprows=1, delimiter=',',
                              usecols=(1, 2, 3, 4, 5, 6, 7, 17, 18, 19),
                              dtype=np.dtype([('stid', '3S'), ('lat', 'f'), ('lon', 'f'),
                                              ('slp', 'f'), ('air_temperature', 'f'),
                                              ('cloud_fraction', 'f'), ('dewpoint', 'f'),
                                              ('weather', '16S'),
                                              ('wind_dir', 'f'), ('wind_speed', 'f')]))

        all_stids = [s.decode('ascii') for s in all_data['stid']]

        whitelist = ['OKC', 'ICT', 'GLD', 'MEM', 'BOS', 'MIA', 'MOB', 'ABQ', 'PHX', 'TTF',
                     'ORD', 'BIL', 'BIS', 'CPR', 'LAX', 'ATL', 'MSP', 'SLC', 'DFW', 'NYC', 'PHL',
                     'PIT', 'IND', 'OLY', 'SYR', 'LEX', 'CHS', 'TLH', 'HOU', 'GJT', 'LBB', 'LSV',
                     'GRB', 'CLT', 'LNK', 'DSM', 'BOI', 'FSD', 'RAP', 'RIC', 'JAN', 'HSV', 'CRW',
                     'SAT', 'BUY', '0CO', 'ZPC', 'VIH']

        # Loop over all the whitelisted sites, grab the first data, and concatenate them
        return np.concatenate([all_data[all_stids.index(site)].reshape(1, ) for site in whitelist])

    def draw_map(self, view):

        from_proj = self.params['projection_options']['from_proj']

        view = MetpyMap.draw_map(self, view)

        x = self.data['lon']
        y = self.data['lat']

        u, v = get_wind_components((self.data['wind_speed'] * units('m/s')).to('knots'),
                                    self.data['wind_dir'] * units.degree)

        stationplot = StationPlot(view, x, y, transform=from_proj,
                                  fontsize=12)

        stationplot.plot_parameter('NW', self.data['air_temperature'], color='red')
        stationplot.plot_parameter('SW', self.data['dewpoint'], color='darkgreen')

        stationplot.plot_parameter('NE', self.data['slp'],
                                   formatter=lambda sp: format(10 * sp, '.0f')[-3:])

        stationplot.plot_barb(u, v)

        return view


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

        MetpyMap.__init__(self, opts)

        self.lons, self.lats,  self.field = self.load_data()

    def load_data(self):

        gefs = TDSCatalog("http://thredds.ucar.edu/thredds/catalog/grib/NCEP/GEFS/Global_1p0deg_Ensemble"
                          "/members/catalog.html?dataset=grib/NCEP/GEFS/Global_1p0deg_Ensemble/members/Best")

        best_ds = list(gefs.datasets.values())[0]
        ncss = NCSS(best_ds.access_urls['NetcdfSubset'])

        query = ncss.query()

        bbox = self.params['bbox']
        query.lonlat_box(north=bbox['north'], south=bbox['south'], east=bbox['east'], west=bbox['west']).time(
            datetime.utcnow())
        query.accept('netcdf4')
        query.variables(self.params['variable'])

        data = ncss.get_data(query)
        print(list(data.variables))

        data = data.variables[self.params['variable']]

        # Time variables can be renamed in GRIB collections. Best to just pull it out of the
        # coordinates attribute on temperature
        time_name = temp_var.coordinates.split()[1]

        time_var = data.variables[time_name]
        lats = data.variables['lat']
        lons = data.variables['lon']

        return lons, lats, data

    def draw_map(self, view):

        view = MetpyMap.draw_map(self, view)

        if 'variable' not in self.options:
            raise ValueError("Must specify variable name.")