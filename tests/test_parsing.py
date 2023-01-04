# Tests parsing datasets
import numpy as np
import pandas as pd

from ros_database.processing.surface import parse_iowa_mesonet_file, parse_precip

"""
TODO:
- Finish creating test data
   a. one with nan and only zero precip
   b. one with object type and T values
- add setting p01i with all zero to nan
- test converting T to 0.2 inches
"""

index = pd.to_datetime(['2015-11-01 01:53:00',
                        '2015-11-01 02:53:00',
                        '2015-11-01 03:33:00',
                        '2015-11-01 03:53:00',
                        '2015-11-01 04:05:00'])
    
df_with_trace = pd.DataFrame(
    {'station': ['BBXY', 'BBXY', 'BBXY', 'BBXY', 'BBXY'],
     'tmpf': [np.nan, '', -40, 0., 32],
     'dwpf': [np.nan, '', -40, 0., 32],
     'relh': [np.nan, '', 0., 45., 100.],
     'drct': [np.nan, '', 0., 359, 90],
     'sknt': [np.nan, '', 0., 1., 5.],
     'p01i': [np.nan, '', 'T', '0.03', '0.05'],
     'alti': [np.nan, '', 24., 30., 7.],
     'mslp': [np.nan, '', 1013., 1005., 900.],
     'wxcodes': ['', 'RA', 'FZRA', 'SN', 'RASN'],
    }, index=index
)

df_with_trace_expected = pd.DataFrame(
    {'station': ['BBXY', 'BBXY', 'BBXY', 'BBXY', 'BBXY'],
     'tmpf': [np.nan, np.nan, -40, 0., 32],
     'dwpf': [np.nan, np.nan, -40, 0., 32],
     'relh': [np.nan, np.nan, 0., 45., 100.],
     'drct': [np.nan, np.nan, 0., 359, 90],
     'sknt': [np.nan, np.nan, 0., 1., 5.],
     'p01i': [np.nan, np.nan, 0.007874, 0.03, 0.05],
     'alti': [np.nan, np.nan, 24., 30., 7.],
     'mslp': [np.nan, np.nan, 1013., 1005., 900.],
     'wxcodes': ['', 'RA', 'FZRA', 'SN', 'RASN'],
    }, index=index
)

df_zero_precip = pd.DataFrame(
    {'station': ['BBXY', 'BBXY', 'BBXY', 'BBXY', 'BBXY'],
     'tmpf': [np.nan, '', -40, 0., 32],
     'dwpf': [np.nan, '', -40, 0., 32],
     'relh': [np.nan, '', 0., 45., 100.],
     'drct': [np.nan, '', 0., 359, 90],
     'sknt': [np.nan, '', 0., 1., 5.],
     'p01i': [np.nan, '', 0., 0., 0.],
     'alti': [np.nan, '', 24., 30., 7.],
     'mslp': [np.nan, '', 1013., 1005., 900.],
     'wxcodes': ['', 'RA', 'FZRA', 'SN', 'RASN'],
    }, index=index
)

df_zero_precip_expected = pd.DataFrame(
    {'station': ['BBXY', 'BBXY', 'BBXY', 'BBXY', 'BBXY'],
     'tmpf': [np.nan, np.nan, -40, 0., 32],
     'dwpf': [np.nan, np.nan, -40, 0., 32],
     'relh': [np.nan, np.nan, 0., 45., 100.],
     'drct': [np.nan, np.nan, 0., 359, 90],
     'sknt': [np.nan, np.nan, 0., 1., 5.],
     'p01i': [np.nan, np.nan, np.nan, np.nan, np.nan],
     'alti': [np.nan, np.nan, 24., 30., 7.],
     'mslp': [np.nan, np.nan, 1013., 1005., 900.],
     'wxcodes': ['', 'RA', 'FZRA', 'SN', 'RASN'],
    }, index=index
)

df_good = pd.DataFrame(
    {'station': ['BBXY', 'BBXY', 'BBXY', 'BBXY', 'BBXY'],
     'tmpf': [np.nan, '', -40, 0., 32],
     'dwpf': [np.nan, '', -40, 0., 32],
     'relh': [np.nan, '', 0., 45., 100.],
     'drct': [np.nan, '', 0., 359, 90],
     'sknt': [np.nan, '', 0., 1., 5.],
     'p01i': [np.nan, '', 0., 0.03, 0.05],
     'alti': [np.nan, '', 24., 30., 7.],
     'mslp': [np.nan, '', 1013., 1005., 900.],
     'wxcodes': ['', 'RA', 'FZRA', 'SN', 'RASN'],
    }, index=index
)

df_good_expected = pd.DataFrame(
    {'station': ['BBXY', 'BBXY', 'BBXY', 'BBXY', 'BBXY'],
     'tmpf': [np.nan, np.nan, -40, 0., 32],
     'dwpf': [np.nan, np.nan, -40, 0., 32],
     'relh': [np.nan, np.nan, 0., 45., 100.],
     'drct': [np.nan, np.nan, 0., 359, 90],
     'sknt': [np.nan, np.nan, 0., 1., 5.],
     'p01i': [np.nan, np.nan, 0., 0.03, 0.05],
     'alti': [np.nan, np.nan, 24., 30., 7.],
     'mslp': [np.nan, np.nan, 1013., 1005., 900.],
     'wxcodes': ['', 'RA', 'FZRA', 'SN', 'RASN'],
    }, index=index
)

def test_parse_precip_dtype():
    """Checks that parse precip returns float64"""
    assert parse_precip(df_with_trace["p01i"]).dtype == "float64", f"df_with_trace precip not returned as float64, returns {parse_precip(df_with_trace['p01i']).dtype} instead"
    assert parse_precip(df_zero_precip["p01i"]).dtype == "float64", f"df_with_trace precip not returned as float64, returns {parse_precip(df_zero_precip['p01i']).dtype} instead"
    assert parse_precip(df_good["p01i"]).dtype == "float64", f"df_with_trace precip not returned as float64, returns {parse_precip(df_good['p01i']).dtype} instead"


def test_parse_precip_trace():
    """Tests that parse_precip returns expected response

    Add round(6) so match is found to 6 sf"""
    assert parse_precip(df_with_trace["p01i"]).round(6).equals(df_with_trace_expected["p01i"].round(6)), f"Expected {df_with_trace_expected['p01i'].values}, got {parse_precip(df_with_trace['p01i'])}"
    
    
def main():
    test_parse_precip_dtype()
