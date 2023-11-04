# Satellite-Image-Retrieval
## Problem and Solution: 
For having meaningful algorithms run on satellite dataset we need to divide the dataset into small bounding boxes on which the data analysis can be done.
Each Bounding Box is sub-divided into several boxes with two consecutive boxes having the following parameters: 

Latitude Difference:- 0.00197
Longitude Difference:- 0.00607

-**Input:** Upper Left (Lon1,Lat1), Bottom Right (Lon2,Lat2)

-**Output:** Aerial Imagery based on the above bounding box.

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
    python3 parallel.py 73.77285 15.42234 73.96717 15.35945

The output desired image is then saved in output folder as divided into sevaral pieces of latdiff and longdiff.

NOTE: Make sure the 'null.jpeg' file is in the current running directory.

## Algorithm:-
Divide each of the bigger bounding boxes to smaller bounding boxes of a specified Length and Breadth and save the images in the output folder.
