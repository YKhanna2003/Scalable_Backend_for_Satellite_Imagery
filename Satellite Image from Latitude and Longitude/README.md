# Satellite-Image-Retrieval
## Problem: 
BING Maps API is used to download Satellite Imagery based on specific Bounding Boxes, latitude and longitude of which is asked from the user.

-**Input:** Upper Left (Lon1,Lat1), Bottom Right (Lon2,Lat2)
-**Output:** Aerial Imagery based on the above bounding box.

NOTE: To get the proper bounding box coordinates, 
1. Refer to the website: https://nominatim.openstreetmap.org/ui/search.html
2. Search the Name of the Region you wish to observer.
3. Select from the several options provided below the search bar.
4. Click on show map bounds on top right of the map to get the bouding box coordinates.
5. Copy the viewbox coordinates and input it in the main.py algorithm.
eg. for observing BITS Goa, you will find the following info:

map center: 15.39093,73.87794 view on osm.org
map zoom: 15
viewbox: 73.85366,15.39878,73.90224,15.38306
last click: undefined
mouse position: 15.39737,73.88954

Copy the data given as 73.85366,15.39878,73.90224,15.38306 for this location.

## Run Instructions
Simply open a Terminal at the project directory, run, for example:

    # Example for BITS Goa Campus
    Enter four comma-separated float values [Upper Left (Lon1,Lat1), Bottom Right (Lon2,Lat2)]:- 73.85366,15.39878,73.90224,15.38306

The output desired image is then saved in output folder as '73.85366-15.39878 to 73.90224-15.38306.jpg'.

## Required Environment
Python 3.8.10 (can test on later versions)
Pillow (Installation below)

Note:
1. Installation of PIL:  
		$ pip install Pillow
2. Make sure the 'null.jpeg' file is in the current running directory.

## Algorithm Introduction
1. Determine the lowest acceptable level by all bounding box area within one tile.
2. Determine the final best level by filtering out from fine to coarse iteratively.
3. Query each tile image and paste.
      1) Convert lat/lon to pixel coordinates.
      2) Convert pixel coordinates to tile coordinates.
      3) Query tile image from Bing Server.
4. Refine and crop the generated image by pixel granularity.

## Reference
	https://msdn.microsoft.com/en-us/library/bb259689.aspx
