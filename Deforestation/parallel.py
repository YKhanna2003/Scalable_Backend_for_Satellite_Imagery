import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from Knn import Knn
from img.data import x,y
import sys
import math
import io
import operator
import numpy as np
import urllib.request
from TileSystem import *
from PIL import Image
TILE_SIZE = 256 			# number of pixels per tile per edge

def getURL(quadkey):
	license_key = "AgHer_2TL4WIP75stUJosD2217kPbu_GVYKKE27fKr0PiEdaxdRr5mWq8fmPIk8N"
	return "http://h0.ortho.tiles.virtualearth.net/tiles/h%s.jpeg?g=131&key=%s" % (quadkey, license_key)


def getImageFromQuadkey(quadkey):
	with urllib.request.urlopen(getURL(quadkey)) as response:
		img = Image.open(io.BytesIO(response.read()))
	return img


def getLowestLevel(lat1, lon1, lat2, lon2):
	for i in range(23, 0, -1):
		tx1, ty1 = latLongToTileXY(lat1, lon1, i)
		tx2, ty2 = latLongToTileXY(lat2, lon2, i)
		if tx1 > tx2:
			tx1, tx2 = tx2, tx1
		if ty1 > ty2:
			ty1, ty2 = ty2, ty1

		# The lowest acceptable level is the level where the bounding box is within only one same tile.
		if (tx2 - tx1 <= 1) and (ty2 - ty1 <= 1):
			print("The lowest acceptable level is: ")
			print(i)
			return i
	print("Error: Improper bounding box.")
	


def nullImage(img):
	flag = (img == Image.open('null.jpeg'))
	return flag


def findBestLevel(lat1, lon1, lat2, lon2, minlevel):
	# set UPPER_SIZE as the size limit of the desired image, in case it is too large to open efficiently.
	UPPER_SIZE = 1 << 12 		# 4096 pixels
	l = 23

	# select the level, iterated from the finest one to the lowest acceptable one
	while l >= minlevel:
		# print ("Check quality in level: ")
		# print (l)
		flag = True
		tx1, ty1 = latLongToTileXY(lat1, lon1, l)
		tx2, ty2 = latLongToTileXY(lat2, lon2, l)
		if tx1 > tx2:
			tx1, tx2 = tx2, tx1
		if ty1 > ty2:
			ty1, ty2 = ty2, ty1
		
		# filter out the "overfine" levels in case of too big images
		if (tx2 - tx1) * TILE_SIZE > UPPER_SIZE:
			l = l - 1
			continue

		# filter out the level as long as where exists even one null image
		for x in range(tx1, tx2+1):
			for y in range(ty1, ty2+1):
				curr_quadkey = tileXYToQuadKey(x, y, l)
				curr_image = getImageFromQuadkey(curr_quadkey)
				if nullImage(curr_image):
					flag = False
					# print("can't find tile:")
					# print("(%d, %d)" % (x,y))
					# print("at the level:")
					# print(l)
					break
			if flag == False:
				break

		if flag == True:
			break
		l = l - 1

	if flag == True:
		print("Found the Image at level: %d" % l)
		return l, tx1, ty1, tx2, ty2
	else:
		print("Error: No acceptable level. Please re-select the bounding box.")

def predictdeforestation(img):
	pixel=0
	knn = Knn(7)
	knn.fit(x,y)
	for j in range(int(img.shape[0]/50)+1):
		for i in range(int(img.shape[1]/50)+1):
			h,b = np.histogram(img[j*50:(j*50)+50,i*50:(i*50)+50])
			if ( knn.predict(h) != 1 ):
				img[j*50:(j*50)+50,i*50:(i*50)+50,1] = 0
				pixel=pixel+1
	plt.imshow(img)
	plt.show()
	print(pixel)

def maintwo(lon1,lat1,lon2,lat2,j,i):
    minlevel = getLowestLevel(lat1, lon1, lat2, lon2)

    l,tx1, ty1, tx2, ty2 = findBestLevel(lat1, lon1, lat2, lon2, minlevel)
    ## generte image
    width = (tx2 - tx1 + 1) * TILE_SIZE
    height = (ty2 - ty1 + 1) * TILE_SIZE
    image = Image.new('RGB', (width, height))

    for x in range(tx1, tx2+1):
        for y in range(ty1, ty2+1):
            curr_quadkey = tileXYToQuadKey(x, y, l)
            # query and paste every tile image orderly
            curr_image = getImageFromQuadkey(curr_quadkey)
            start_x = (x - tx1) * TILE_SIZE 
            start_y = (y - ty1) * TILE_SIZE
            end_x = start_x + TILE_SIZE
            end_y = start_y + TILE_SIZE
            image.paste(curr_image, (int(start_x), int(start_y), int(end_x), int(end_y)))

    print("Image successfully generated.")
    ## crop the image
    px1, py1 = latLongToPixelXY(lat1, lon1, l) 		# px1, py1 is the global pixel coordinates of the upper left point
    base_x = tx1 * TILE_SIZE 						# base_x, base_y is the global pixel coordinates of the upper left pixel in the upper left tile
    base_y = ty1 * TILE_SIZE
    d_x1 = px1 - base_x 							# d_x1, d_y1 is the displacement coodinates of the upper left point relative to the base pixel
    d_y1 = py1 - base_y

    px2, py2 = latLongToPixelXY(lat2, lon2, l)
    d_x2 = px2 - base_x
    d_y2 = py2 - base_y

    output = image.crop((d_x1, d_y1, d_x2, d_y2))
    print("Image successfully cropped.")
    predictdeforestation(output)
	output.save('./output/'+str(j)+str(i)+" "+str(lon1) + " " + str(lat1)+ " " + str(lon2)+ " " + str(lat2)+".jpg")


def main():
    lon1 = float(sys.argv[1])
    lat1 = float(sys.argv[2])
    lon2 = float(sys.argv[3])
    lat2 = float(sys.argv[4])
    majorlondiff=lon2-lon1
    majorlatdiff=lat1-lat2
    londiff=0.00607
    latdiff=0.00197
    londivisor=int(majorlondiff/londiff)
    latdivisor=int(majorlatdiff/latdiff)
    for j in range(latdivisor):
        for i in range(londivisor):
            maintwo(lon1+((i)*londiff),lat1-((j)*latdiff),lon1+((i+1)*londiff),lat1-((j+1)*latdiff),j,i)

if __name__ == '__main__':
	main()
