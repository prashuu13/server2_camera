# USAGE
# python social_distance_detector.py --input pedestrians.mp4
# python social_distance_detector.py --input pedestrians.mp4 --output output.avi

# import the necessary packages
from pyimagesearch import social_distancing_config as config
from pyimagesearch.detection import detect_people
from scipy.spatial import distance as dist
import numpy as np
import argparse
import imutils
import cv2
import os
import time
from store_api import *
from imutils import paths
from camerasync import *
try:
	#cap2 = cv2.VideoCapture('rtsp://admin:admin@123@114.79.131.224:554/unicast/c4/s1/live')
	cap2 = VideoCaptureAsync('rtsp://admin:Lock@1234@202.134.159.185:10554/streaming/Channels/401')
	cap2.start()
	print('Async')
except:
	#cap2 = cv2.VideoCapture('rtsp://admin:admin@123@114.79.131.224:554/unicast/c4/s1/live')
	cap2 = cv2.VideoCapture('rtsp://admin:Lock@1234@202.134.159.185:10554/streaming/Channels/301')
	print('continuous')

Detected = True
Violation = False
# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--input", type=str, default="",
# 	help="path to (optional) input video file")
# ap.add_argument("-o", "--output", type=str, default="",
# 	help="path to (optional) output video file")
# ap.add_argument("-d", "--display", type=int, default=1,
# 	help="whether or not output frame should be displayed")
# args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([config.MODEL_PATH, "yolov3.weights"])
configPath = os.path.sep.join([config.MODEL_PATH, "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# check if we are going to use GPU
if config.USE_GPU:
	# set CUDA as the preferable backend and target
	print("[INFO] setting preferable backend and target to CUDA...")
	net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
	net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# initialize the video stream and pointer to output video file
print("[INFO] accessing video stream...")
#vs = cv2.VideoCapture(args["input"] if args["input"] else 0)
writer = None
Detected = False
 
counter = 0
proxy = 500
def feed(cap,feedname):
	ret, frame = cap.read()
	global temp
	global counter,proxy,imgpath,Detected
# loop over the frames from the video stream
	while True:
		# read the next frame from the file
		(grabbed, frame) = cap.read()
		
		image = frame.copy()
		counter += 1 
		
		

		# if the frame was not grabbed, then we have reached the end
		# of the stream
		if not grabbed:
			break

		# resize the frame and then detect people (and only people) in it
		frame = imutils.resize(frame, width=700)
		results = detect_people(frame, net, ln,
			personIdx=LABELS.index("person"))

		# initialize the set of indexes that violate the minimum social
		# distance
		violate = set()
		Violation = False
		# ensure there are *at least* two people detections (required in
		# order to compute our pairwise distance maps)
		if len(results) >= 2:
			# extract all centroids from the results and compute the
			# Euclidean distances between all pairs of the centroids
			centroids = np.array([r[2] for r in results])
			D = dist.cdist(centroids, centroids, metric="euclidean")

			# loop over the upper triangular of the distance matrix
			for i in range(0, D.shape[0]):
				for j in range(i + 1, D.shape[1]):
					# check to see if the distance between any two
					# centroid pairs is less than the configured number
					# of pixels
					if D[i, j] < config.MIN_DISTANCE:
						# update our violation set with the indexes of
						# the centroid pairs
						violate.add(i)
						violate.add(j)
						Violation = True

		# loop over the results
		for (i, (prob, bbox, centroid)) in enumerate(results):
			# extract the bounding box and centroid coordinates, then
			# initialize the color of the annotation
			(startX, startY, endX, endY) = bbox
			(cX, cY) = centroid
			color = (0, 255, 0)

			# if the index pair exists within the violation set, then
			# update the color
			if i in violate:
				color = (0, 0, 255)

			# draw (1) a bounding box around the person and (2) the
			# centroid coordinates of the person,
			cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
			cv2.circle(frame, (cX, cY), 5, color, 1)

		# draw the total number of social distancing violations on the
		# output frame
		text = "Social Distancing Violations: {}".format(len(violate))
		cv2.putText(frame, text, (10, frame.shape[0] - 25),
			cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)
		
		
		date_string = time.strftime("%Y-%m-%d-%H-%M")
		
		
		if Violation == True and Detected == False:
			print(Detected)
			imgpath = 'output/img-'+ date_string +'.png'
			cv2.imwrite(imgpath ,image)
			print("The file is saved to ",imgpath)
			#cv2.imwrite('output/img-'+ date_string +'.png' ,frame)
			
			#ret = social_store_image_bucket(str(10),'E',imgpath,6)

			Detected = True
			Violation = False
			proxy = counter + 100
			print(counter)
			print(proxy)
		if counter == proxy:
			Detected = False

		 
		#path = 'output'
		#imgpath = sorted(list(paths.list_images(path)))

		#for imgpath in imagePaths:
			#print(imgpath)
		#ret = social_store_image_bucket(str(8),'E',imgpath,4)

		# check to see if the output frame should be displayed to our
		# screen
		#if args["display"] > 0:
			# show the output frame
		#cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

			# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

		# if an output video file path has been supplied and the video
		# writer has not been initialized, do so now
		# if args["output"] != "" and writer is None:
		# 	# initialize our video writer
		# 	fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		# 	writer = cv2.VideoWriter(args["output"], fourcc, 25,
		# 		(frame.shape[1], frame.shape[0]), True)

		# # if the video writer is not None, write the frame to the output
		# # video file
		# if writer is not None:
		# 	writer.write(frame)

feed(cap2,'ch-8')
