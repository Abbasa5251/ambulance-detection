from django.db import models

class AmbulanceDetection(models.Model):
    ambulance_detection_video = models.FileField(upload_to='ambulance_detection/video/', blank=True)
    ambulance_detection_audio = models.FileField(upload_to='ambulance_detection/audio/', blank=True)
    