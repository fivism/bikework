"""
Controller reads through cleaned trip references and generates the
minute-by-minute renderings of all trips in progress
"""
import matplotlib.pyplot as plt
import matplotlib.cm
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
import pandas as pd
import sys
import csv
from dateutil import parser
import dateutil.relativedelta as tdelta
import copy
import time     # just used for function benchmarking
from trip_obj import Trip

if len(sys.argv) < 2:
    sys.exit('Usage: %s trip_csv_file' % sys.argv[0])

TRIP_FILE = sys.argv[1]

"""
DEBUG SETTINGS
"""
SHOW_BAD_TRIPS = True
DEBUG_MODE = False
error_trips = []  # bad trip quarantine
SHOW_LONG_TRIPS = True  # TODO show trips longer than 45 min

"""
BASEMAP CONSTANTS FOR OSLO BYSYKKEL
(DublinCore format)
"""
M_CENTER_LAT, M_CENTER_LON = 59.922056, 10.736092
W_LIM, S_LIM, E_LIM, N_LIM = 10.649384, 59.886967, 10.818299, 59.955795

if DEBUG_MODE:
    print("DEBUG MODE")


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
    m.drawrivers(linewidth=0.5, linestyle='solid', color='k',
                 antialiased=1, ax=None, zorder=None)

    # m.readshapefile('street_redux/street_redux', oslo_roads, drawbounds=True, zorder=100,
    #                 linewidth=0.5, color='k', antialiased=1, ax=None, default_encoding='utf-8')


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

        # mins of trip elapsed
        x = tdelta.relativedelta(target_time, trip.start_time)
        xmins = x.minutes
        if x.hours > 0:
            xmins += x.hours * 60

        if (xmins == nmins):    # prevent index erroring
            xmins -= 1

        # consider pushing this out
        if DEBUG_MODE:
            print("\nN (total) points: " + str(nmins))
            print("n: " + str(n))
            print("XDelta: " + str(xmins))
            print("x: " + str(x))

        pt_tuples = m.gcpoints(
            startpt[0], startpt[1], endpt[0], endpt[1], nmins)
        return (pt_tuples[0][xmins], pt_tuples[1][xmins])

    for trip in trips:
        if (trip.start_st in sta_dict) and (trip.end_st in sta_dict):
            # Check that start and end exist in our station reference
            # if not, discard
            startpt = (float(sta_dict[trip.start_st][4]),
                       float(sta_dict[trip.start_st][3]))
            endpt = (float(sta_dict[trip.end_st][4]),
                     float(sta_dict[trip.end_st][3]))
            m.drawgreatcircle(float(startpt[0]), float(startpt[1]),
                              float(endpt[0]), float(endpt[1]),
                              linewidth=1.5, color='pink')
            try:
                current_pos = calc_pos(trip, startpt, endpt)
            except ZeroDivisionError as e:
                if DEBUG_MODE:
                    print("Got ZeroDE on Trip:", str(trip))
                error_trips.append(trip)
                continue
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
# *AND drops counting maybe by exporting the affected trips in the loop!
# add drops reporting

# Make the official basemap which we'll recopy for every new frame
# but not render from scratch
oslo_roads = ""
m = Basemap(resolution='c',
            projection='merc',
            lat_0=59.922, lon_0=10.736,
            llcrnrlon=W_LIM, llcrnrlat=S_LIM, urcrnrlon=E_LIM, urcrnrlat=N_LIM)


counter = 0
for hour in range(10, 11):
    for minute in range(0, 10):
        # Start timing for benchmarking
        start_time = time.time()

        # Plot prep
        fig, ax = plt.subplots(figsize=(20, 20))

        # NAIVE: Copy the pre-rendered tmp_m object
        tmp_m = copy.copy(m)
        # color in basemap
        plot_base(tmp_m)

        # plot stations as fixed, scaled points on basemap obj
        plot_stations(station_dict, tmp_m)
        time_string = "2018-05-01 " + \
            "{:0>2d}".format(hour) + ":" + \
            "{:0>2d}".format(minute) + ":00 +0200"
        test_time = parser.parse(time_string)
        results = find_trips(TRIP_FILE, test_time)

        if DEBUG_MODE:
            if len(results) > 0:
                print("Results: ", len(results))
                for trip in results:
                    print(trip)
            else:
                print("No trips found")

        plot_paths(station_dict, tmp_m, results, test_time)
        plt.title(time_string)
        plt.savefig("img/" + "{:0>4d}".format(counter) +
                    ".png", bbox_inches='tight')
        plt.clf()   # Clear figure

        counter += 1
        print("---Processed minute %s in %2.3f seconds ---" %
              (time_string, (time.time() - start_time)))


# Print out exception'd trips from quarantine
# Assume these are mostly trips less than one minute in duration
if SHOW_BAD_TRIPS:
    print("\nThe following trips generated ZeroDivisionError exceptions:")
    for trip in error_trips:
        print(trip)
