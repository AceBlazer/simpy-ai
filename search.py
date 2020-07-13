# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
import argparse
import cv2
import os
import base64
import numpy as np
from firestorage import getImage




def run(query, customer_name, project_name, index, result_path = None):
	# initialize the image descriptor
	cd = ColorDescriptor((8, 12, 3))

	# load the query image and describe it
	query = cv2.imread(str(query))
	features = cd.describe(query)

	# perform the search
	searcher = Searcher(str(index))
	results = searcher.search(features)

	paths = []
	# loop over the results
	if results:
		for (score, resultID) in results:
			sim = {}
			#sim["image"] = str(resultID)
			#return link from firestore with id
			sim["image"] = getImage("dataset/"+customer_name+"/"+project_name+"/"+os.path.basename(resultID))
			sim["score"] = score
			paths.append(sim)
        
	return paths