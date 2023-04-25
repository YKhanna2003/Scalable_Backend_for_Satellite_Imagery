# Algorithms_On_Satellite_Imagery
Algorithm Application on Satellite Imagery, demonstrating Data Analysis and Algorithm fine-tuning

Deforestation Detector based on the coordinates entered.

NOTE: To get the proper bounding box coordinates,

1. Refer to the website: https://nominatim.openstreetmap.org/ui/search.html
2. Search the Name of the Region you wish to observer.
3. Select from the several options provided below the search bar.
4. Click on show map bounds on top right of the map to get the bouding box coordinates.
5. Copy the viewbox coordinates and input it in the main.py algorithm.
6. You have to run the parallel.py file here to get the divided imagery

![alt text](https://github.com/YKhanna2003/Algorithms_On_Satellite_Imagery/blob/main/Parallel_Processing_Aerial/images/image1.png?raw=true)

eg. for observing region around BITS Goa, you will find the following info:

map center: 15.39093,73.87794 view on osm.org
map zoom: 15
viewbox: 73.85366,15.39878,73.90224,15.38306
last click: undefined
mouse position: 15.39737,73.88954

Copy the data given as 73.85366,15.39878,73.90224,15.38306 for this location.

## Run Instructions
Simply open a Terminal at the project directory, run, for example:

    # Example for near BITS Goa Campus
    python3 main.py 73.77285 15.42234 73.96717 15.35945

Author: Yash Khanna

NOTE: During running any algorithm in the mentioned Repo, if you face error having keywork "HTTPS Connection" in it, try to re-run the algorithm, the error is generated due to the API failing due to weak internet connection.
