from traitlets.config.application import Application
from traitlets import Float, Unicode, Bool, Any, Dict, default, Instance

import cartopy
import numpy as np

from metpy.plots import StationPlot
from metpy.calc import get_wind_components
from metpy.units import units
from metpy.cbook import get_test_data
from metpy.plots.wx_symbols import sky_cover, current_weather

from cartopy.mpl.geoaxes import GeoAxes


class MetpyMap(Application):

    map_type = Unicode(default_value='',
                       allow_none=False,
                       help='type of map to plot').tag(config=True)

    data = Any(default_value=None,
               allow_none=False,
               help='data to be plotted').tag(config=True)

    file_location = Unicode(default_value="",
                            allow_none=False,
                            help='location of the data file').tag(config=True)

    bbox = Dict(traits={"east": Float(allow_none=False), "west": Float(allow_none=False),
                        "north": Float(allow_none=False), "south": Float(allow_none=False)},
                help='map bounding box in lat/lon coordinates').tag(config=True)

    feature_choices = Dict(trait=Any(),
                           help='Available features to toggle on or off').tag(config=True)

    features = Dict(trait=Bool(),
                    help='Toggle cartopy features to draw').tag(config=True)

    projection_options = Dict(traits={"from_proj": Any(),
                                      "to_proj": Any()},
                              help='projection options').tag(config=True)

    @default('feature_choices')
    def _feature_choices_default(self):
        """Set the default values for available basic cartopy features."""

        avail_features = {
            'OCEANS': cartopy.feature.OCEAN,
            'LAKES': cartopy.feature.LAKES,
            'RIVERS': cartopy.feature.RIVERS,
            'LAND': cartopy.feature.LAND,
            'COASTLINE': cartopy.feature.COASTLINE,
            'BORDERS': cartopy.feature.BORDERS,
            'STATES': cartopy.feature.NaturalEarthFeature(
                category='cultural',
                name='admin_1_states_provinces_lakes',
                scale='50m',
                facecolor='none')
        }

        return avail_features

    @default('features')
    def _features_default(self):
        """Set the all of the default activation toggles to false for all map features."""

        return dict({f: False for f in self.feature_choices.keys()})

    @default('projection_options')
    def _projection_options_default(self):
        """Set the all of the default cartopy projection objects."""

        return dict(from_proj=None, to_proj=None)

    @default('bbox')
    def _bbox_default(self):
        """Set default bounding box to contain the United States."""

        return dict(east=-70, west=-120, north=50, south=25)

    def draw_map(self, view):
        """Most basic map we can make.  With required parameters, draw active features
           within the given bounding box."""

        view.set_extent([self.bbox['west'], self.bbox['east'],
                         self.bbox['south'], self.bbox['north']])

        for key, activated in self.features.items():
            if activated:
                view.add_feature(self.feature_choices[key])

        if self.map_type == 'station':

            self.draw_station_plots(view)

    def load_text(self):
        """Placeholder function to demonstrate traitlets class"""

        f = get_test_data(self.file_location)

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
        self.data = np.concatenate([all_data[all_stids.index(site)].reshape(1, ) for site in whitelist])

    def draw_station_plots(self, view):
        """Another semi-placeholder.  We could get much smarter on what stationplot attributes
           to try to display."""

        from_proj = self.projection_options['from_proj']

        x = self.data['lon']
        y = self.data['lat']

        cloud_frac = (8 * self.data['cloud_fraction']).astype(int)

        stid = [s.decode('ascii') for s in self.data['stid']]

        wx_text = [s.decode('ascii') for s in self.data['weather']]

        wx_codes = {'': 0, 'HZ': 5, 'BR': 10, '-DZ': 51, 'DZ': 53, '+DZ': 55,
                    '-RA': 61, 'RA': 63, '+RA': 65, '-SN': 71, 'SN': 73, '+SN': 75}

        wx = [wx_codes[s.split()[0] if ' ' in s else s] for s in wx_text]

        u, v = get_wind_components((self.data['wind_speed'] * units('m/s')).to('knots'),
                                   self.data['wind_dir'] * units.degree)

        stationplot = StationPlot(view, x, y, transform=from_proj,
                                  fontsize=12)

        stationplot.plot_parameter('NW', self.data['air_temperature'], color='red')
        stationplot.plot_parameter('SW', self.data['dewpoint'], color='darkgreen')

        stationplot.plot_parameter('NE', self.data['slp'],
                                   formatter=lambda sp: format(10 * sp, '.0f')[-3:])

        stationplot.plot_symbol('C', cloud_frac, sky_cover)

        stationplot.plot_symbol('W', wx, current_weather)

        stationplot.plot_barb(u, v)

        stationplot.plot_text((2, 0), stid)