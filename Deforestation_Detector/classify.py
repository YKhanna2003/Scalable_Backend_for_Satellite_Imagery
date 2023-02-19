import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from Knn import Knn
from img.data import x,y

if len(sys.argv) < 2:
	print("Correct Usage:- "+sys.argv[0]+" image-path")
	exit()
pixel=0
knn = Knn(7)
knn.fit(x,y)
img = mpimg.imread(sys.argv[1])
for j in range(int(img.shape[0]/50)+1):
	for i in range(int(img.shape[1]/50)+1):
		h,b = np.histogram(img[j*50:(j*50)+50,i*50:(i*50)+50])
		#if we find forest cover
		if (knn.predict(h)==1):
			pixel=pixel+1
plt.imshow(img)
plt.show()
print(pixel)
