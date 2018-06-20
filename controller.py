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
import pandas as pd
import sys
import csv

# if len(sys.argv) < 3:
#     sys.exit('Usage: %s trip_csv_file output' % sys.argv[0])

# TRIP_FILE = sys.argv[1]
# OUTPUT_NAME = sys.argv[2]

# trip_df = pandas.read_csv(TRIP_FILE)

fig, ax = plt.subplots(figsize=(10, 20))

# center 59.922056, 10.736092
# for now using DublinCore bounding box of Oslo with limits:
# westlimit=10.649384; southlimit=59.886967; eastlimit=10.818299; northlimit=59.955795


def plot_base(m):
    m.drawmapboundary(fill_color='#46bcec')
    m.fillcontinents(color='#f2f2f2', lake_color='#46bcec')
    m.drawcoastlines()


def read_stations(filename):
    """
    This should eventually call stationExtractor for newest list
    Returns dict of station IDs linked to relevant data bits so that 
    we skip row matching
    """
    with open(filename, mode='r') as infile:
        infile_noheader = infile.readlines()[1:]
        reader = csv.reader(infile_noheader)
        out_dict = {rows[0]: rows[1:6] for rows in reader}
        return out_dict
    # station_dict = pd.read_csv(filename)


def plot_stations(sta_dict, m):
    """
    Plots stations on basemap given dict which includes lat/longs
    (lat: dict[4], long: dict[5])
    """
    for st in sta_dict:
        x, y = float(sta_dict[st][4]), float(sta_dict[st][3])
        size = (float(sta_dict[st][2]) / 13.0) ** 2 + 1
        m.plot(x, y, marker='o',
               markersize=size, color='#cccccc', alpha=0.9, latlon=True)


def plot_paths(sta_dict, m, starts, ends):
    """
    Void func that for now, takes in sets of lats and longs and draws these routes
    """
    for trip in range(0, len(starts)):
        stx, sty = sta_dict[starts[trip]][4], sta_dict[starts[trip]][3]
        endx, endy = sta_dict[ends[trip]][4], sta_dict[ends[trip]][3]
        m.drawgreatcircle(float(stx), float(sty),
                          float(endx), float(endy),
                          linewidth=1.5, color='pink')


def plot_trips(sta_dict, trips, starts, ends):
    """
    Func takes station_dictionary
    List of active trips
    """
    for trip in range(0, len(starts)):
        stx, sty = sta_dict[starts[trip]][4], sta_dict[starts[trip]][3]
        endx, endy = sta_dict[ends[trip]][4], sta_dict[ends[trip]][3]
        m.drawgreatcircle(float(stx), float(sty),
                          float(endx), float(endy),
                          linewidth=1.5, color='pink')


# Initialize 'm' basemap obj
m = Basemap(resolution='c',
            projection='merc',
            lat_0=59.922, lon_0=10.736,
            llcrnrlon=10.65, llcrnrlat=59.887, urcrnrlon=10.8183, urcrnrlat=59.9558)

# color in basemap
plot_base(m)

# read stations into a hashed dict because we will be referring to them v often
station_dict = read_stations("test.csv")

# plot stations as fixed, scaled points on basemap obj
plot_stations(station_dict, m)

# draw mini trips list
starts = ['229', '232', '226', '394', '201']
ends = ['262', '419', '342', '402', '201']
plot_paths(station_dict, m, starts, ends)

# generate plot title
plt.title('bysykkel')

# plt.gcpoints() -- calculate n points where n is # of minutes of trip

# OFFSETS ARE INTERESTING HERE
# test line perhaps x and y are gyldige trips
# plt.quiver(x[points], y[points],
#            u10[points], v10[points], speed[points],
#            cmap=plt.cm.autumn)


# plt.savefig('out.png')

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
