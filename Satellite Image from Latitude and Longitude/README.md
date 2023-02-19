# Satellite-Image-Retrieval
## Problem: 
BING Maps API is used to download Satellite Imagery based on specific Bounding Boxes, latitude and longitude of which is asked from the user.

-**Input:** Upper Left (Lon1,Lat1), Bottom Right (Lon2,Lat2)
-**Output:** Aerial Imagery based on the above bounding box.

NOTE: To get the proper bounding box coordinates, 
1. Refer to the website: https://nominatim.openstreetmap.org/ui/search.html
2. Search the Name of the Region you wish to observe.
3. Select from the several options provided below the search bar.
4. Click on show map bounds on top right of the map to get the bounding box coordinates.
5. Copy the viewbox coordinates and input it in the main.py algorithm.

![alt text](https://github.com/YKhanna2003/Algorithms_On_Satellite_Imagery/blob/main/Satellite%20Image%20from%20Latitude%20and%20Longitude/images/image1.png?raw=true)

eg. for observing BITS Goa, you will find the following info:

Map center: 15.39093,73.87794 view on osm.org
Map zoom: 15
Viewbox: 73.85366,15.39878,73.90224,15.38306
Last click: undefined
Mouse position: 15.39737,73.88954

Copy the data given as 73.85366,15.39878,73.90224,15.38306 for this location.

## Run Instructions
Simply open a Terminal at the project directory, run, for example:

    # Example for BITS Goa Campus
    python3 main.py
    
    Enter four comma-separated float values [Upper Left (Lon1,Lat1), Bottom Right (Lon2,Lat2)]:- 73.85366,15.39878,73.90224,15.38306

The output desired image is then saved in output folder as '73.85366-15.39878 to 73.90224-15.38306.jpg'.

## Required Environment
Python 3.8.10 (can test on later versions)
Pillow (Installation below)

Note:
1. Installation of PIL:  
		$ pip install Pillow
2. Make sure the 'null.jpeg' file is in the current running directory. It will be used to check if the image obatined from the BING server is different from null image, if it is equal to null then there will be no entry on BING's server.

Output

![alt text](https://github.com/YKhanna2003/Algorithms_On_Satellite_Imagery/blob/main/Satellite%20Image%20from%20Latitude%20and%20Longitude/images/image2.jpg?raw=true)

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
