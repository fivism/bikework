"""
Controller reads through cleaned trip references and generates the
minute-by-minute renderings of all trips in progress
"""
import time
import matplotlib.pyplot as plt
import matplotlib.cm
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
#import trip_obj
import pandas
import sys

# if len(sys.argv) < 3:
#     sys.exit('Usage: %s trip_csv_file output' % sys.argv[0])

# TRIP_FILE = sys.argv[1]
# OUTPUT_NAME = sys.argv[2]

# trip_df = pandas.read_csv(TRIP_FILE)

fig, ax = plt.subplots(figsize=(10, 20))

# center 59.922056, 10.736092
# for now using DublinCore bounding box of Oslo with limits:
# westlimit=10.649384; southlimit=59.886967; eastlimit=10.818299; northlimit=59.955795
m = Basemap(resolution='i',
            projection='merc',
            lat_0=59.922, lon_0=10.736,
            llcrnrlon=10.65, llcrnrlat=59.887, urcrnrlon=10.8183, urcrnrlat=59.9558)
m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='#f2f2f2')
m.drawcoastlines()
plt.title('oslo med veldig få polygon')

plt.show()
# def generate_objs(trips_data):
#     """
#     Given a trips dataframe, generate minute by minute renders
#     """

# def output_file(filename):
#     # write headers
#     with open(OUTPUT_NAME, 'w') as outfile:
#     outfile.write(HEADERS_LINE)

#     # append the rest
#     with open(OUTPUT_NAME, 'a') as outfile:
#         for station in jdata['stations']:
#             line_list = [str(station['id']),
#                          station['title'],
#                          station['subtitle'],
#                          str(station['number_of_locks']),
#                          str(station['center']['latitude']),
#                          str(station['center']['longitude'])]
#             out_line = ",".join(line_list)
#             out_line += '\n'
#             outfile.write(out_line)
