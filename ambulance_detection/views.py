from django.shortcuts import render
from .forms import AmbulanceDetectionForm
from django.conf import settings
from .detector import Detector, AudioDetector
import mimetypes
mimetypes.init()

def home(request):
	form = AmbulanceDetectionForm(request.POST, request.FILES) 
	if request.method == 'POST':	
		if len(request.FILES) == 0:
			return render(request,'ambulance_detection/ambulance_detection.html', {'form' : form, 'isclicked':True, 'error_name':'Files NOT found'})
		
		elif request.POST.get('audio', False):
			post = form.save(commit=False)
			post.save()
			audioURL = settings.MEDIA_URL + form.instance.ambulance_detection_audio.name
			audiopath = settings.MEDIA_ROOT_URL + audioURL
			form.save()
			result, score, audioURL = AudioDetector(audiopath)
			return render(request, 'ambulance_detection/ambulance_detection.html', {'form': form, 'post': post, 'audioURL': audioURL, 'isclicked':True, 'isaudio':True, 'audio_result':result, 'score':score, 'error_name':'Audio Uploaded Successfully !'})

		else :
			post = form.save(commit=False)
			post.save()
			videoURL = settings.MEDIA_URL + form.instance.ambulance_detection_video.name
			mimestart = mimetypes.guess_type(settings.MEDIA_ROOT_URL + videoURL)[0]
			if mimestart != None:
				mimestart = mimestart.split('/')[0]
				videopath = settings.MEDIA_ROOT_URL + videoURL
				if mimestart == "image":
					Detector(videopath)
				else:
					form.save()
					path=str(settings.MEDIA_ROOT_URL) + videoURL
					path=str(settings.BASE_DIR) + path[1:len(path)]
					videoURL = Detector(videopath)
					return render(request, 'ambulance_detection/ambulance_detection.html', {'form': form, 'post': post, 'videoURL': videoURL, 'isclicked':True, 'error_name':'Video Uploaded Successfully !'})
			return render(request,'ambulance_detection/ambulance_detection.html', {'form' : form, 'post':post, 'videoURL': videoURL, 'isclicked':True, 'error_name':'Video Uploaded Successfully !'})

	else:
		form = AmbulanceDetectionForm()
	return render(request,'ambulance_detection/ambulance_detection.html', {'form' : form, 'iserror':False})  

	