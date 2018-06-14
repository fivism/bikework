# takes client key and connects to oslobyskkel to grab JSON feed and
# writes out a CSV with chosen fields

import pandas as pd
import json
import sys

if len(sys.argv) < 3:
    sys.exit('Usage: %s client-key output-file' % sys.argv[0])

API_KEY = sys.argv[1]
OUTPUT_NAME = sys.argv[2]
HEADERS_LINE = "id,name,name2,lock_count,lat,long\n"

# TODO - input is from the actual feed not a copy
jdata = pd.read_json("stations.json")

with open(OUTPUT_NAME, 'w') as outfile:
    outfile.write(HEADERS_LINE)

## append the rest
with open(OUTPUT_NAME, 'a') as outfile:
    for station in jdata['stations']: 
        line_list =     [str(station['id']), 
                        station['title'], 
                        station['subtitle'], 
                        str(station['number_of_locks']), 
                        str(station['center']['latitude']), 
                        str(station['center']['longitude'])]
        out_line = ",".join(line_list)
        out_line += '\n'
        outfile.write(out_line)


