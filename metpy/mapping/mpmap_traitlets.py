from traitlets.config.configurable import Configurable
from traitlets import Int, Float, Unicode, Bool, Any


class StationPlot(Configurable):

    file_location = Unicode(allow_none=False, help='location of the data file').tag(config=True)

    west = Float(allow_none=False, help='westernmost edge of map').tag(config=True)

    east = Float(allow_none=False, help='east edge of map').tag(config=True)

    north = Float(allow_none=False, help='north edge of map').tag(config=True)

    south = Float(allow_none=False, help='south edge of map').tag(config=True)

    states = Bool(default_value=False, help='toggle for drawing states').tag(config=True)

    oceans = Bool(default_value=False, help='toggle for drawing oceans').tag(config=True)

    coastlines = Bool(default_value=False, help='toggle for drawing oceans').tag(config=True)

    countries = Bool(default_value=True, help='toggle for drawing countries').tag(config=True)

    from_proj = Any()

