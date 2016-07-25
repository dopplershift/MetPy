import cartopy.crs as ccrs


# Variables

file_location = "station_data.txt"

to_proj = ccrs.AlbersEqualArea(central_longitude=-97.0000, central_latitude=38.0000)
from_proj = ccrs.Geodetic()

north = 45
south = 30
east = -100
west = -120

oceans = True
borders = True
coastline = True
lakes = False
states = True

map_type = 'station'

# Map configuration
# Dict types only take dict assignments..
# cannot assign value to individual keys

c.MetpyMap.file_location = file_location

c.MetpyMap.map_type = map_type

c.MetpyMap.bbox = dict(north=40, south=25, east=-80, west=-100)

c.MetpyMap.projection_options = dict(to_proj=to_proj, from_proj=from_proj)

c.MetpyMap.features = dict(OCEANS=oceans, BORDERS=borders,
                           COASTLINE=coastline, LAKES=lakes, STATES=states)

