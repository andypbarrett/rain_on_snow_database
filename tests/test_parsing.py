# Tests parsing datasets
import numpy as np
import pandas as pd

from ros_database.processing.surface import (parse_iowa_mesonet_file,
                                             parse_precip,
                                             parse_all_zero_precip,
                                             knots2mps,
                                             u_wind, v_wind,
                                             altitude_to_pressure)
from ros_database.processing.cleaning import range_check, range_check_relh


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
     'wspd': [np.nan, np.nan, 0.00, 0.51, 2.57],
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
     'wspd': [np.nan, np.nan, 0.00, 0.51, 2.57],
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
     'wspd': [np.nan, np.nan, 0.00, 0.51, 2.57],
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


def test_altitude_conversion():
    """Tests conversion of altitude to barometric pressure"""
    expected_arr = [np.nan, np.nan, 812.7, 1015.9, 237.1]
    parse_arr = altitude_to_pressure(df_with_trace["alti"]).round(1).values
    assert (parse_arr == expected_arr).any(), f"Expected {expected_arr}, got {parse_arr}"

    
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


def test_windspeed_conversion(atol=0.01):
    """Checks wind speed conversion with round-off"""
    df = df_good
    expected = df_good_expected.wspd.values
    result = knots2mps(df.sknt).values
    print(expected)
    print(result)
    np.testing.assert_allclose(result, expected, atol, equal_nan=True,
                               err_msg=f"Expected {expected}, got {result}")    


def test_expected_range_relh():
    """Test for relh range check"""
    parse = pd.DataFrame({'relh': [np.nan, -7., 0., 50., 100., 105., 200.]})
    expected = pd.DataFrame({'relh': [np.nan, np.nan, 0., 50., 100., 105., 100.]})
    range_check_relh(parse)
    assert expected.equals(parse), f"Expected {expected['relh'].values}, got {parse['relh'].values}"


def test_expected_range_drct():
    """Test for relh range check"""
    parse = pd.DataFrame({'drct': [np.nan, -7., 0., 180., 360., 361.]})
    expected = pd.DataFrame({'drct': [np.nan, np.nan, 0., 180., 360., np.nan]})
    range_check(parse, 'drct')
    assert expected.equals(parse), f"Expected {expected['drct'].values}, got {parse['drct'].values}"


def test_expected_range_p01i():
    """Test for relh range check"""
    parse = pd.DataFrame({'p01i': [np.nan, -7., 0., 50., 100., 500.]})
    expected = pd.DataFrame({'p01i': [np.nan, np.nan, 0., 50., 100., np.nan]})
    range_check(parse, 'p01i')
    assert expected.equals(parse), f"Expected {expected['p01i'].values}, got {parse['p01i'].values}"


def test_expected_range_mslp():
    """Test for relh range check"""
    parse = pd.DataFrame({'mslp': [np.nan, -7., 500., 900., 1013., 1090., 2000.]})
    expected = pd.DataFrame({'mslp': [np.nan, np.nan, np.nan, 900., 1013., 1090., np.nan]})
    range_check(parse, 'mslp')
    assert expected.equals(parse), f"Expected {expected['mslp'].values}, got {parse['mslp'].values}"


def test_expected_range_psurf():
    """Test for relh range check"""
    parse = pd.DataFrame({'psurf': [np.nan, -7., 500., 850., 1013., 1090., 2000.]})
    expected = pd.DataFrame({'psurf': [np.nan, np.nan, np.nan, 850., 1013., 1090., np.nan]})
    range_check(parse, 'psurf')
    assert expected.equals(parse), f"Expected {expected['psurf'].values}, got {parse['psurf'].values}"


def test_expected_range_t2m():
    """Test for relh range check"""
    parse = pd.DataFrame({'t2m': [np.nan, -100., -70., 0., 20., 50., 70]})
    expected = pd.DataFrame({'t2m': [np.nan, np.nan, -70., 0., 20., 50., np.nan]})
    range_check(parse, 't2m')
    assert expected.equals(parse), f"Expected {expected['t2m'].values}, got {parse['t2m'].values}"


def test_expected_range_d2m():
    """Test for relh range check"""
    parse = pd.DataFrame({'d2m': [np.nan, -100., -70., 0., 20., 50., 70]})
    expected = pd.DataFrame({'d2m': [np.nan, np.nan, -70., 0., 20., 50., np.nan]})
    range_check(parse, 'd2m')
    assert expected.equals(parse), f"Expected {expected['d2m'].values}, got {parse['d2m'].values}"


def test_expected_range_wspd():
    """Test for relh range check"""
    parse = pd.DataFrame({'wspd': [np.nan, -100., 0., 50., 103., 200.]})
    expected = pd.DataFrame({'wspd': [np.nan, np.nan, 0., 50., 103., np.nan]})
    range_check(parse, 'wspd')
    assert expected.equals(parse), f"Expected {expected['wspd'].values}, got {parse['wspd'].values}"


def test_expected_range_uwnd():
    """Test for relh range check"""
    parse = pd.DataFrame({'uwnd': [np.nan, -200., -103., 0., 103., 200.]})
    expected = pd.DataFrame({'uwnd': [np.nan, np.nan, -103., 0., 103., np.nan]})
    range_check(parse, 'uwnd')
    assert expected.equals(parse), f"Expected {expected['uwnd'].values}, got {parse['uwnd'].values}"


def test_expected_range_vwnd():
    """Test for relh range check"""
    parse = pd.DataFrame({'vwnd': [np.nan, -200., -103., 0., 103., 200.]})
    expected = pd.DataFrame({'vwnd': [np.nan, np.nan, -103., 0., 103., np.nan]})
    range_check(parse, 'vwnd')
    assert expected.equals(parse), f"Expected {expected['vwnd'].values}, got {parse['vwnd'].values}"


def test_parse_dataframe_trace():
    """Test correct parsing of df_with_trace"""
    df_parse = parse_iowa_mesonet_file(df_with_trace)
    assert df_parse["t2m"].equals(df_with_trace_expected["t2m"]), "Parsing df_with_trace failed for t2m"
    assert df_parse["d2m"].equals(df_with_trace_expected["d2m"]), "Parsing df_with_trace failed for d2m"
    assert df_parse["p01i"].equals(df_with_trace_expected["p01i"]), "Parsing df_with_trace failed for p01i"
    assert df_parse["UP"].equals(df_with_trace_expected["UP"]), "Parsing df_with_trace failed for UP"
    assert df_parse["RA"].equals(df_with_trace_expected["RA"]), "Parsing df_with_trace failed for RA"
    assert df_parse["FZRA"].equals(df_with_trace_expected["FZRA"]), "Parsing df_with_trace failed for FZRA"
    assert df_parse["SOLID"].equals(df_with_trace_expected["SOLID"]), "Parsing df_with_trace failed for SOLID"
    assert df_parse["wspd"].equals(df_good_expected["wspd"]), "Parsing df_good failed for SOLID"
    
def test_parse_dataframe_zero():
    """Test correct parsing of df_zero_precip"""
    df_parse = parse_iowa_mesonet_file(df_zero_precip)
    assert df_parse["t2m"].equals(df_zero_precip_expected["t2m"]), "Parsing df_zero_precip failed for t2m"
    assert df_parse["d2m"].equals(df_zero_precip_expected["d2m"]), "Parsing df_zero_precip failed for d2m"
    assert df_parse["p01i"].equals(df_zero_precip_expected["p01i"]), "Parsing df_zero_precip failed for p01i"
    assert df_parse["UP"].equals(df_zero_precip_expected["UP"]), "Parsing df_zero_precip failed for UP"
    assert df_parse["RA"].equals(df_zero_precip_expected["RA"]), "Parsing df_zero_precip failed for RA"
    assert df_parse["FZRA"].equals(df_zero_precip_expected["FZRA"]), "Parsing df_zero_precip failed for FZRA"
    assert df_parse["SOLID"].equals(df_zero_precip_expected["SOLID"]), "Parsing df_zero_precip failed for SOLID"
    assert df_parse["wspd"].equals(df_good_expected["wspd"]), "Parsing df_good failed for SOLID"

def test_parse_dataframe_good():
    """Test correct parsing of df_good"""
    df_parse = parse_iowa_mesonet_file(df_good)
    assert df_parse["t2m"].equals(df_good_expected["t2m"]), "Parsing df_good failed for t2m"
    assert df_parse["d2m"].equals(df_good_expected["d2m"]), "Parsing df_good failed for d2m"
    assert df_parse["p01i"].equals(df_good_expected["p01i"]), "Parsing df_good failed for p01i"
    assert df_parse["UP"].equals(df_good_expected["UP"]), "Parsing df_good failed for UP"
    assert df_parse["RA"].equals(df_good_expected["RA"]), "Parsing df_good failed for RA"
    assert df_parse["FZRA"].equals(df_good_expected["FZRA"]), "Parsing df_good failed for FZRA"
    assert df_parse["SOLID"].equals(df_good_expected["SOLID"]), "Parsing df_good failed for SOLID"
    assert df_parse["wspd"].equals(df_good_expected["wspd"]), "Parsing df_good failed for SOLID"


def test_parse_all_zero_precip():
    test_df = pd.Series([np.nan, 0.0, 0.0])
    result = parse_all_zero_precip(test_df)
    assert  np.isnan(result).all(), f"test_parse_all_zero_precip: expected all NaNs, got {result}"

    
def test_parse_not_all_zero_precip():
    test_df = pd.Series([np.nan, 1.0, 0.0])
    result = np.isnan(parse_all_zero_precip(test_df))
    expected = [True, False, False]
    assert  (result == expected).all(), f"test_parse_not_all_zero_precip: expected {expected}, got {result}"
