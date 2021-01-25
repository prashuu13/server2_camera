# USAGE
# python recognize_faces_image.py --encodings encodings.pickle

# import the necessary packages
import face_recognition
import argparse
import pickle
import cv2
import os
import time
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
#ap.add_argument("-e", "--encodings", required=True,
#	help="path to serialized db of facial encodings")
#ap.add_argument("-i", "--image", required=False,
# 	help="path to input image")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

cap2 = cv2.VideoCapture('rtsp://admin:Lock@1234@202.134.159.185:10554/streaming/Channels/401')
ret2, frame2 = cap2.read()

# load the known faces and embeddings
#print("[INFO] loading encodings...")
#data = pickle.loads(open(args["encodings"], "rb").read())

# load the input image and convert it from BGR to RGB
# pathImg = r'C:\Users\laptopno202\Desktop\facebb\images'

# def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png')):
#     """
#     Get the latest image file in the given directory
#     """

#     # get filepaths of all files and dirs in the given dir
#     image_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
#     # filter out directories, no-extension, and wrong extension files
#     image_files = [f for f in image_files if '.' in f and \
#         f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

#     if not image_files:
#         raise ValueError("No valid images in %s" % dirpath)

#     return max(image_files, key=os.path.getmtime)

# folder_last_modified_time = os.path.getmtime(pathImg)
# print("Last modification time ", folder_last_modified_time)

# local_time = time.ctime(folder_last_modified_time)
# print("Last modification time(Local time):", local_time)

# image=get_latest_image(pathImg)
# print(type(image))
# print(os.path.basename(image))


# image = cv2.imread(image)
# rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# print(rgb.shape)




# image = cv2.imread(image)
# rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# detect the (x, y)-coordinates of the bounding boxes corresponding
# to each face in the input image, then compute the facial embeddings
# for each face
#print("[INFO] recognizing faces...")
# from camerasync import *
# try:
# 	cap2 = VideoCaptureAsync('rtsp://admin:Lock@1234@202.134.159.185:10554/streaming/Channels/401')
# 	cap2.start()
# 	print('Async')
# except:
# 	cap2 = cv2.VideoCapture('rtsp://admin:Lock@1234@202.134.159.185:10554/streaming/Channels/401')
# 	print('continuous')
def feed(cap,feedname):
	ret, frame = cap.read()
	print(ret)

	boxes = face_recognition.face_locations(frame,
		model=args["detection_method"])
#encodings = face_recognition.face_encodings(rgb, boxes)

# initialize the list of names for each face detected
#names = []

# loop over the facial embeddings
#for encoding in encodings:
	# attempt to match each face in the input image to our known
	# encodings
	# matches = face_recognition.compare_faces(data["encodings"],
	# 	encoding)
	# name = "Unknown"
	#
	# # check to see if we have found a match
	# if True in matches:
	# 	# find the indexes of all matched faces then initialize a
	# 	# dictionary to count the total number of times each face
	# 	# was matched
	# 	matchedIdxs = [i for (i, b) in enumerate(matches) if b]
	# 	counts = {}
	#
	# 	# loop over the matched indexes and maintain a count for
	# 	# each recognized face face
	# 	for i in matchedIdxs:
	# 		name = data["names"][i]
	# 		counts[name] = counts.get(name, 0) + 1
	#
	# 	# determine the recognized face with the largest number of
	# 	# votes (note: in the event of an unlikely tie Python will
	# 	# select first entry in the dictionary)
	# 	name = max(counts, key=counts.get)
	#
	# # update the list of names
	# names.append(name)

# loop over the recognized faces
	for (top, right, bottom, left) in boxes:
		# draw the predicted face name on the image
		cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		#cv2.putText(image,{top,bottom},(left, y), cv2.FONT_HERSHEY_SIMPLEX,
		#	0.75, (0, 255, 0), 2)

# show the output image
#print("The persion identified in the pic" ,name)
	cv2.imshow("Image", frame)
	#print(" The BB cordinates are ", top,right,bottom,left)
	cv2.waitKey(0)
	cap.release()

	cv2.destroyAllWindows()
feed(cap2,'ch-8')
#print("The persion identified in the pic" ,{names})
