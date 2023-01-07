"""Contains data for quality control"""

# Expected data types for columns in cleaned data files 
expected_cleaned_dtypes = {
    'station': 'object',
    'relh': 'float64',
    'drct': 'float64',
    'p01i': 'float64',
    'psurf': 'float64',
    'mslp': 'float64',
    't2m': 'float64',
    'd2m': 'float64',
    'wspd': 'float64',
    'UP': 'object',
    'RA': 'object',
    'FZRA': 'object',
    'SOLID': 'object',
    'uwnd': 'float64',
    'vwnd': 'float64',
}

# Expected range of values for each variable.  These are used to
# screen out "obviously" wrong values.  Expected values are determined from
# logical ranges in the case of relative humidity and direction, and
# climatological values otherwise.  Note: relative humidity is allowed to
# be slightly supersaturated.
expected_range = {
    'relh': {'min': 0., 'max': 105.},
    'drct': {'min': 0., 'max': 360.},
    'p01i': {'min': 0., 'max': 100.},
    'alti': {'min': -100, 'max': 100},
    'mslp': {'min': 900., 'max': 1090.},
    'psurf': {'min': 600., 'max': 1090.},
    't2m': {'min': -60., 'max': 50.},
    'd2m': {'min': -60., 'max': 50.},
    'wspd': {'min': 0., 'max': 100.},   # Based on Mt Washington record 231 mph
    'UP': {'min': False, 'max': True},
    'RA': {'min': False, 'max': True},
    'FZRA': {'min': False, 'max': True},
    'SOLID': {'min': False, 'max': True},
    'uwnd': {'min': -100, 'max': 100.},
    'vwnd': {'min': -100, 'max': 100.},
}

# Replacement values when values outside of limits
# Only for values greater than relh limits
# np.nan otherwise
replacement_values = {
    'relh_above': 100.,
}
    
expected_values = {
    'UP': [True, False, np.nan],
    'RA': [True, False, np.nan],
    'FZRA': [True, False, np.nan],
    'SOLID': [True, False, np.nan],
}
