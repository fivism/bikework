class Trip_obj(object):
    start_time  = 0     # null initialized time value?
    end_time    = 0     # 
    start_st    = 0     # start station ID
    end_st      = 0     # end station ID
    total_time  = 0
    percent_done = 0.0
   

    # we check by minute and initialize any that started this minute 
    def __init__(self, start_time, end_time, start_st, end_st):
        self.start_time = start_time
        self.end_time   = end_time
        self.start_st   = start_st
        self.end_st     = end st
    
    # we check who is alive and accessible in the alive list
    # and update accordingly
    def __update__(self):
        # TODO pull in new time tuple from outside or feed in?
        percent_done = new_percent_done
        
         
