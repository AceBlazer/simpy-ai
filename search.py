# USAGE
# python search.py --index index.csv --query queries/103100.png --result-path .

# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
import argparse
import cv2
import os



def run(query, index, result_path = None):
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
			# load the result image and display it
			#result = cv2.imread(str(os.path.join(result_path, resultID)))
			#cv2.imshow("Result", result)
			#cv2.waitKey(0)
			sim = {}
			sim["image"] = str(resultID)
			sim["score"] = score
			paths.append(sim)

	return paths