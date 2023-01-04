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
     'tmpf': [np.nan, np.nan, -40, 0., 32],
     'dwpf': [np.nan, np.nan, -40, 0., 32],
     'relh': [np.nan, np.nan, 0., 45., 100.],
     'drct': [np.nan, np.nan, 0., 359, 90],
     'sknt': [np.nan, np.nan, 0., 1., 5.],
     'p01i': [np.nan, '', 'T', '0.03', '0.05'],
     'alti': [np.nan, np.nan, 24., 30., 7.],
     'mslp': [np.nan, np.nan, 1013., 1005., 900.],
     'wxcodes': ['', 'RA', 'FZRA', 'SN', 'RASN'],
    }, index=index
)

df_with_trace_expected = pd.DataFrame(
    {'station': ['BBXY', 'BBXY', 'BBXY', 'BBXY', 'BBXY'],
     't2m': [np.nan, np.nan, -40.0, -17.8, 0.0],
     'd2m': [np.nan, np.nan, -40.0, -17.8, 0.0],
     'relh': [np.nan, np.nan, 0., 45., 100.],
     'drct': [np.nan, np.nan, 0., 359, 90],
     'sknt': [np.nan, np.nan, 0.00, 0.51, 2.57],
     'p01i': [np.nan, np.nan, 0.2, 0.8, 1.3],
     'alti': [np.nan, np.nan, 24., 30., 7.],
     'mslp': [np.nan, np.nan, 1013., 1005., 900.],
     'UP': [False, False, False, False, False],
     'RA': [False, True, False, False, True],
     'FZRA': [False, False, True, False, False],
     'SOLID': [False, False, False, True, True],
    }, index=index
)

df_zero_precip = pd.DataFrame(
    {'station': ['BBXY', 'BBXY', 'BBXY', 'BBXY', 'BBXY'],
     'tmpf': [np.nan, np.nan, -40, 0., 32],
     'dwpf': [np.nan, np.nan, -40, 0., 32],
     'relh': [np.nan, np.nan, 0., 45., 100.],
     'drct': [np.nan, np.nan, 0., 359, 90],
     'sknt': [np.nan, np.nan, 0., 1., 5.],
     'p01i': [np.nan, '', 0., 0., 0.],
     'alti': [np.nan, np.nan, 24., 30., 7.],
     'mslp': [np.nan, np.nan, 1013., 1005., 900.],
     'wxcodes': ['', 'RA', 'FZRA', 'SN', 'RASN'],
    }, index=index
)

df_zero_precip_expected = pd.DataFrame(
    {'station': ['BBXY', 'BBXY', 'BBXY', 'BBXY', 'BBXY'],
     't2m': [np.nan, np.nan, -40.0, -17.8, 0.0],
     'd2m': [np.nan, np.nan, -40.0, -17.8, 0.0],
     'relh': [np.nan, np.nan, 0., 45., 100.],
     'drct': [np.nan, np.nan, 0., 359, 90],
     'sknt': [np.nan, np.nan, 0.00, 0.51, 2.57],
     'p01i': [np.nan, np.nan, np.nan, np.nan, np.nan],
     'alti': [np.nan, np.nan, 24., 30., 7.],
     'mslp': [np.nan, np.nan, 1013., 1005., 900.],
     'UP': [False, False, False, False, False],
     'RA': [False, True, False, False, True],
     'FZRA': [False, False, True, False, False],
     'SOLID': [False, False, False, True, True],
     'wxcodes': ['', 'RA', 'FZRA', 'SN', 'RASN'],
    }, index=index
)

df_good = pd.DataFrame(
    {'station': ['BBXY', 'BBXY', 'BBXY', 'BBXY', 'BBXY'],
     'tmpf': [np.nan, np.nan, -40, 0., 32],
     'dwpf': [np.nan, np.nan, -40, 0., 32],
     'relh': [np.nan, np.nan, 0., 45., 100.],
     'drct': [np.nan, np.nan, 0., 359, 90],
     'sknt': [np.nan, np.nan, 0., 1., 5.],
     'p01i': [np.nan, '', 0., 0.03, 0.05],
     'alti': [np.nan, np.nan, 24., 30., 7.],
     'mslp': [np.nan, np.nan, 1013., 1005., 900.],
     'wxcodes': ['', 'RA', 'FZRA', 'SN', 'RASN'],
    }, index=index
)

df_good_expected = pd.DataFrame(
    {'station': ['BBXY', 'BBXY', 'BBXY', 'BBXY', 'BBXY'],
     't2m': [np.nan, np.nan, -40.0, -17.8, 0.0],
     'd2m': [np.nan, np.nan, -40.0, -17.8, 0.0],
     'relh': [np.nan, np.nan, 0., 45., 100.],
     'drct': [np.nan, np.nan, 0., 359, 90],
     'sknt': [np.nan, np.nan, 0.00, 0.51, 2.57],
     'p01i': [np.nan, np.nan, 0.0, 0.8, 1.3],
     'alti': [np.nan, np.nan, 24., 30., 7.],
     'mslp': [np.nan, np.nan, 1013., 1005., 900.],
     'UP': [False, False, False, False, False],
     'RA': [False, True, False, False, True],
     'FZRA': [False, False, True, False, False],
     'SOLID': [False, False, False, True, True],
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
    expected_arr = [np.nan, np.nan, 0.007874, 0.03, 0.05]
    parse_arr = parse_precip(df_with_trace["p01i"]).round(6).values
    assert (parse_arr == expected_arr).any(), f"Expected {expected_arr}, got {parse_arr}"


def test_parse_precip_zero():
    """Checks that test dataframe returns the same"""
    expected_arr = [np.nan, np.nan, 0.0, 0.0, 0.0]
    parse_arr = parse_precip(df_zero_precip["p01i"]).round(6).values
    assert (parse_arr == expected_arr).any(), f"Expected {expected_arr}, got {parse_arr}"


def test_parse_dataframe_trace():
    """Test correct parsing of df_with_trace"""
    df_parse = parse_iowa_mesonet_file(df_with_trace)
    assert df_parse["t2m"].equals(df_with_trace_expected["t2m"]), "Parsing df_with_trace failed for t2m"
    assert df_parse["d2m"].equals(df_with_trace_expected["d2m"]), "Parsing df_with_trace failed for d2m"
    assert df_parse["p01i"].equals(df_with_trace_expected["p01i"]), "Parsing df_with_trace failed for p01i"
    assert df_parse["UP"].equals(df_with_trace_expected["UP"]), "Parsing df_with_trace failed for UP"
    assert df_parse["RA"].equals(df_with_trace_expected["RA"]), "Parsing df_with_trace failed for RA"
    assert df_parse["FZRA"].equals(df_with_trace_expected["FZRA"]), "Parsing df_with_trace failed for FZRA"
    assert df_parse["SOLID"].equals(df_with_trace_expected["FZRA"]), "Parsing df_with_trace failed for FZRA"

    
def main():
    test_parse_precip_dtype()
    test_parse_precip_trace()
    test_parse_precip_zero()
    test_parse_precip_dtype()
    test_parse_dataframe_trace()


if __name__ == "__main__":
    main()
