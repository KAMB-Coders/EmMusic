import cv2
from keras.preprocessing import image
import warnings
from PIL import Image
warnings.filterwarnings("ignore") 
#from keras.preprocessing.image import load_img, img_to_array 
from keras.models import  load_model
import matplotlib.pyplot as plt
import numpy as np
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .spotifyfunction import getTrackURL
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
import os
@csrf_exempt
def detectEmotion(req):	
	# load model
	model = load_model("KambMusic/best_model.h5")
	face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
	img = req.FILES['image']
	fs = FileSystemStorage()
	filename = fs.save((img.name).replace(" ",""), img)
	fileurl = fs.url(filename)
	# test_img = img.open('rb')
	# test_img = Image.fromarray(np.array(img))

	# print("Type of face image", type(test_img))
	test_img = cv2.imread(fileurl[1:]) #cv2.imread(face_image)
	# print("Type of face image", test_img)
	gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)
	faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)
	if(len(faces_detected)>0):
		x, y, w, h = faces_detected[0]
		roi_gray = gray_img[y:y + w, x:x + h]
		# cropping region of interest i.e. face area from  image
		roi_gray = cv2.resize(roi_gray, (224, 224))
		img_pixels = np.array(roi_gray)
		img_pixels = np.expand_dims(img_pixels, axis=0)
		img_pixels = img_pixels/255
		
		predictions = model.predict(img_pixels)
		
		# find max indexed array
		max_index = np.argmax(predictions[0])
		emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
		predicted_emotion = emotions[max_index]
		print("Predicted emotion: ", predicted_emotion)
		if os.path.exists(fileurl[1:]):
			os.remove(fileurl[1:])
		return getTrackURL(predicted_emotion)
	if os.path.exists(fileurl[1:]):
		os.remove(fileurl[1:])
	return JsonResponse({"emotion":'No face detected'})