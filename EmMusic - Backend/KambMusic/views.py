from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .faceDetection import detectEmotion
# from .spotifyfunction import getTrackURL
from django.views.decorators.csrf import csrf_exempt, csrf_protect


# Create your views here.
def index(request):
	return HttpResponse("Hello")

@csrf_exempt
def getTrack(request):
	#print(request)
	if request.method == 'GET':
		return HttpResponse("Invalid request method")
	img = request.FILES['image'].file.read()
	print("Type  of:  ",type(img))
	return detectEmotion(request)#"KambMusic/images.jpg")
	#track_url = getTrackURL(emotion)
	# return JsonResponse({"emotion":emotion})
	#if request.method == 'POST':
	#	request.FILES['image']