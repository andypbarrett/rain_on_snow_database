"""Contains data for quality control"""

expected_cleaned_dtypes = {
    'station': 'object',
    'relh': 'float64',
    'drct': 'float64',
    'p01i': 'float64',
    'alti': 'float64',
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


expected_range = {
    'relh': {'min': 0., 'max': 100.},
    'drct': {'min': 0., 'max': 360.},
    'p01i': {'min': 0., 'max': 100.},
    'alti': {'min': -100, 'max': 100},
    'mslp': {'min': 900., 'max': 1090.},
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


expected_values = {
    'UP': [True, False, np.nan],
    'RA': [True, False, np.nan],
    'FZRA': [True, False, np.nan],
    'SOLID': [True, False, np.nan],
}
