# forms.py
from django import forms
from .models import AmbulanceDetection

class AmbulanceDetectionForm(forms.ModelForm):
	class Meta:
		model = AmbulanceDetection
		fields = ['ambulance_detection_video', 'ambulance_detection_audio']
