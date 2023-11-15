from numbers import Number

from ros_database.filepath import SURFOBS_RAW_PATH, SURFOBS_CLEAN_PATH
from ros_database.processing.surface import read_mesonet_raw_file
from scripts.clean_asos_data import get_raw_station_filepaths


def check_fields(df):
   for col in df.columns:
      if col not in ['station', 'wxcodes']:
         assert check_all_numeric(df[col]), f"Unexpected data type in {col}"
#      if col in ['station', 'wxcodes']:
#         assert check_all_string(df[col]), f"Unexpected data type in {col}"


def check_all_numeric(s):
   return s.map(lambda x: isinstance(x, Number)).all()


def check_all_string(s):
   return s.map(lambda x: isinstance(x, str)).all()

   
#stations = [p.stem.split('.')[0] for p in SURFOBS_CLEAN_PATH.glob("*.csv")]
stations = []

for fp in get_raw_station_filepaths(stations, SURFOBS_RAW_PATH, True):
   print(fp)
   df = read_mesonet_raw_file(fp)
   try:
      check_fields(df)
   except AssertionError as err:
      print(f"  FAILED!")
