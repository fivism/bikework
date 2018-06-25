#!/bin/bash 

# call python 
python3 controller.py may1.csv

# call imagemagick on the set of PNGs
convert -delay 7 -loop 0 -verbose img/*.png animated.gif

