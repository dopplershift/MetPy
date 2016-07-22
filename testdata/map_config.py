
c = 


@default('feature_choices')
def _feature_choices_default(self):
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
    return dict({f: False for f in self.feature_choices.keys()})


@default('projection_options')
def _projection_options_default(self):
    return dict(from_proj=None, to_proj=None)


@default('bbox')
def _bbox_default(self):
    return dict(east=-70, west=-120, north=50, south=25)