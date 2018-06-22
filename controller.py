"""
Controller reads through cleaned trip references and generates the
minute-by-minute renderings of all trips in progress
"""
# import time
import matplotlib.pyplot as plt
import matplotlib.cm
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from trip_obj import Trip
import pandas as pd
import sys
import csv
from dateutil import parser
import dateutil.relativedelta as tdelta

# if len(sys.argv) < 3:
#     sys.exit('Usage: %s trip_csv_file output' % sys.argv[0])

# OUTPUT_NAME = sys.argv[2]

# trip_df = pandas.read_csv(TRIP_FILE)
# center 59.922056, 10.736092
# for now using DublinCore bounding box of Oslo with limits:
# westlimit=10.649384; southlimit=59.886967; eastlimit=10.818299; northlimit=59.955795


def find_trips(filename, target_time):
    """
    Iterates through trip data CSV files for trips that are alive at
    target_time. Returns list of initialized *trip_objs*
    """
    trip_list = []

    def init_trip(csv_line):
        """
        Void function that dissects trip line and
        fully initializes a new trip_obj
        and returns the obj
        """
        new_trip = Trip(parser.parse(csv_line[1]),
                        parser.parse(csv_line[3]),
                        csv_line[0],
                        csv_line[2])
        return new_trip

    with open(filename, mode='r') as infile:
        infile_noheader = infile.readlines()[1:]
        reader = csv.reader(infile_noheader)
        for row in reader:
            if (target_time < parser.parse(row[1])):
                # search time is before this entry
                break
            elif (target_time < parser.parse(row[3]) and
                  (target_time > parser.parse(row[1]))):
                trip_list.append(init_trip(row))

    return trip_list


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


def plot_base(m):
    m.drawmapboundary(fill_color='#46bcec')
    m.fillcontinents(color='#f2f2f2', lake_color='#46bcec')
    m.drawcoastlines()


def plot_stations(sta_dict, m):
    """
    Plots stations on basemap given dict which includes lat/longs
    (lat: dict[4], long: dict[5])
    """
    for st in sta_dict:
        x, y = float(sta_dict[st][4]), float(sta_dict[st][3])
        size = (float(sta_dict[st][2]) / 13.0) ** 2 + 4
        m.plot(x, y, marker='o',
               markersize=size, color='#cccccc', alpha=0.9, latlon=True)


def plot_paths(sta_dict, m, trips, target_time):
    """
    Examines trip start and stop stations and generates
    straight line paths + 
    interpolated position given target_time
    """
    def calc_pos(trip, startpt, endpt):
        """
        Takes trip object + start and end (x, y) tuples 
        and generates n-minutes of points 
        and returns the "current" point
        """
        n = tdelta.relativedelta(
            trip.end_time, trip.start_time)  # total trip time in mins
        nmins = n.minutes
        if n.days > 0:
            n.hours = n.days * 24       # late deliveries
        if n.hours > 0:
            nmins += n.hours * 60       # also late deliveries
        print("NPoints: " + str(nmins))
        print("n: " + str(n))

        # mins of trip elapsed
        x = tdelta.relativedelta(target_time, trip.start_time)
        xmins = x.minutes
        if x.hours > 0:
            xmins += x.hours * 60
        print("XDelta: " + str(xmins))
        print("x: " + str(x))

        if (xmins == nmins):    # prevent index erroring
            xmins -= 1

        pt_tuples = m.gcpoints(
            startpt[0], startpt[1], endpt[0], endpt[1], nmins)
        # print(pt_tuples)
        return (pt_tuples[0][xmins], pt_tuples[1][xmins])

    for trip in trips:
        if (trip.start_st in sta_dict) and (trip.end_st in sta_dict):
            startpt = (float(sta_dict[trip.start_st][4]),
                       float(sta_dict[trip.start_st][3]))
            endpt = (float(sta_dict[trip.end_st][4]),
                     float(sta_dict[trip.end_st][3]))
            m.drawgreatcircle(float(startpt[0]), float(startpt[1]),
                              float(endpt[0]), float(endpt[1]),
                              linewidth=1.5, color='pink')

            current_pos = calc_pos(trip, startpt, endpt)
            m.plot(current_pos[0], current_pos[1], marker='o',
                   markersize=5, color='#000000')
        else:
            continue

    return None


def plot_path(sta_dict, m, starts, ends):
    """
    Void func that for now, takes in sets of lats and longs and draws these routes
    """
    for trip in range(0, len(starts)):
        stx, sty = sta_dict[starts[trip]][4], sta_dict[starts[trip]][3]
        endx, endy = sta_dict[ends[trip]][4], sta_dict[ends[trip]][3]
        m.drawgreatcircle(float(stx), float(sty),
                          float(endx), float(endy),
                          linewidth=1.5, color='pink')


# read stations into a hashed dict because we will be referring to them v often
station_dict = read_stations("test.csv")

# MAIN
# Get rid of this and fix incrementing
# add divide by zero exception
# *AND drops counting maybe by exporting the affected trips in the loop!
for minute in range(0, 10):
    # Plot prep
    fig, ax = plt.subplots(figsize=(20, 20))
    # Initialize 'm' basemap obj
    m = Basemap(resolution='l',
                projection='merc', i
                lat_0=59.922, lon_0=10.736,
                llcrnrlon=10.65, llcrnrlat=59.887, urcrnrlon=10.8183, urcrnrlat=59.9558)

    # color in basemap
    plot_base(m)

    # plot stations as fixed, scaled points on basemap obj
    plot_stations(station_dict, m)
    time_string = "2018-05-01 09:" + str(minute) + ":00 +0200"
    test_time = parser.parse(time_string)
    results = find_trips("may1.csv", test_time)
    if len(results) > 0:
        print("Results: ", len(results))
        for trip in results:
            print(trip)
    else:
        print("No trips found")
    plot_paths(station_dict, m, results, test_time)
    plt.title(time_string)
    plt.savefig("img/" + str(minute) + ".png", bbox_inches='tight')
    plt.clf()   # Clear figure

# Animation workflow sample
# counter = 0                                         # Frame counter

# for t in t_space:
#     y = f(x, t)
#     lines[0].set_ydata(y)
#     plt.legend(['t=%4.2f' % t])                     # t changes every frame; update
#     plt.draw()
#     plt.savefig('tmp_%03d.png' % counter)
#     counter += 1
# $ convert -delay 7 -loop 0 *.png animated.gif       # ImageMagick CLI - with shorter delay than spec
