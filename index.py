# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from firestorage import uploadRetrievedImages, uploadIndexes
import argparse
import glob
import cv2
import os
import time



def indexNow(customer_name, project_name, index):
	dataset = os.path.join("dataset", customer_name, project_name)
	# initialize the color descriptor
	cd = ColorDescriptor((8, 12, 3))

	# open the output index file for writing
	output = open(str(index), "w")
	# use glob to grab the image paths and loop over them



	#TODO: all img extentions
	for imagePath in glob.glob(str(dataset) + "/*/*.jpg"):
		# extract the image ID (i.e. the unique filename) from the image
		# path and load the image itself
		imageID = imagePath[imagePath.rfind("/") + 1:]
		image = cv2.imread(imagePath)

		# describe the image
		features = cd.describe(image)

		# write the features to file
		features = [str(f) for f in features]
		output.write("%s,%s\n" % (imageID, ",".join(features)))


	for imagePath in glob.glob(str(dataset) + "/*/*.jpeg"):
    	# extract the image ID (i.e. the unique filename) from the image
		# path and load the image itself
		imageID = imagePath[imagePath.rfind("/") + 1:]
		image = cv2.imread(imagePath)

		# describe the image
		features = cd.describe(image)

		# write the features to file
		features = [str(f) for f in features]
		output.write("%s,%s\n" % (imageID, ",".join(features)))


	for imagePath in glob.glob(str(dataset) + "/*/*.png"):
    	# extract the image ID (i.e. the unique filename) from the image
		# path and load the image itself
		imageID = imagePath[imagePath.rfind("/") + 1:]
		image = cv2.imread(imagePath)

		# describe the image
		features = cd.describe(image)

		# write the features to file
		features = [str(f) for f in features]
		output.write("%s,%s\n" % (imageID, ",".join(features)))

	print("=========> started uploading into firebase")
	start_time = time.time()
	#upload all retrieved images to firestorage
	uploadRetrievedImages(customer_name, project_name)

	#TODO: upload indexes
	uploadIndexes(customer_name, project_name)
	print("=========> firebase upload time taken: %s" %(time.time() - start_time))

	# close the index file
	output.close()