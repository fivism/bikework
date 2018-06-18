import dateutil.relativedelta as tdelta
from datetime import datetime, timezone


class Trip_obj(object):
    # consider keyID for these objects
    start_time = 0     # null initialized time value?
    end_time = 0     #
    start_st = 0     # start station ID
    end_st = 0     # end station ID
    minutes_total = 0     # time delta between start and end time in mins
    minutes_done = 0    # total minutes elapsed
    percent_done = 0.0   # current percentage of trip complete (for drawing)
    # this will be zero at creation time

    # we check by minute and initialize any that started this minute
    def __init__(self, start_time, end_time, start_st, end_st):
        self.start_time = start_time
        self.end_time = end_time
        self.start_st = start_st
        self.end_st = end_st
        self.minutes_total = tdelta.relativedelta(end_time, start_time)

    def __update__():
        """
        Ticks the progress of the trip forward one minute
        """
        minutes_done += 1
        percent_done = minutes_done / float(minutes_total)

    def __str__():
        """
        toString available for debugging
        """
        print()
