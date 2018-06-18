"""
Controller reads through cleaned trip references and generates the
minute-by-minute renderings of all trips in progress
"""

import trip_obj
import pandas
import sys

if len(sys.argv) < 3:
    sys.exit('Usage: %s trip_csv_file output' % sys.argv[0])

TRIP_FILE = sys.argv[1]
OUTPUT_NAME = sys.argv[2]

trip_df = pandas.read_csv(TRIP_FILE)


def generate_objs(trips_data):
    """
    Given a trips dataframe, generate minute by minute renders
    """
