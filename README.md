# bikework
collection of oslo bysykkel munging utilities and visualization tools

Currently, this generates visualizations with 60-second resolution, interpolating rider movements
between Oslo Bysykkel bikeracks.
![sample image](img/2.png)
 
# TODO
- [x] scrape coords out of station status feed
- [x] trip objects succesfully created from trip data
- [x] 1080 minute-collections per day generated
- [x] automate merging of usage data + latlongs
- [x] render trip vectors
- [x] animation workflow
- [ ] collect one day of station data to try and mash together
- [ ] evaluate translation to mplleaflet to speed up processing
- [ ] look into deal.gl
