#!/bin/bash 

# call python 
python3 controller.py may1.csv

# call imagemagick on the set of PNGs
convert -delay 7 -loop 0 -verbose img/*.png animated.gif

# further into h264 mp4 
# ffmpeg -i animated.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" video.mp4
