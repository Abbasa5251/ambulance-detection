from tensorflow.keras.models import load_model
from imutils.video import FileVideoStream, FPS
import time
import cv2
import librosa
import numpy as np
from django.conf import settings
from warnings import filterwarnings as w; w('ignore')

def Detector(video_file_path):
	model_file_path = str(settings.BASE_DIR) + "\\ambulance_detection\\model.h5"
	model = load_model(model_file_path)

	def preprocess(frame):
		'''
		Returns: Frame is resized to model's configuration, scaled and converted to a batch
		'''
		frame = cv2.resize(frame, (224,224), interpolation = cv2.INTER_AREA)
		frame = frame/255.0
		frame = np.expand_dims(frame, 0)
		return frame

	vs = FileVideoStream(video_file_path).start()
	time.sleep(1.0)
	
	fourcc = cv2.VideoWriter_fourcc(*'avc1')

	fps = FPS().start()

	classes = ['NON-EMERGENCY', 'EMERGENCY']
	i = 0
	
	while vs.more():
		frm = vs.read()
		if frm is None:
			break
		frame = preprocess(frm)
		prediction = model.predict(frame)

		text = classes[not(np.argmax(prediction))]

		cv2.putText(frm, text, (90,200), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0,221,254), 4)
		
		if i==0:
			w, h = frm.shape[:2]
			video = cv2.VideoWriter(video_file_path[:-5]+"_new"+".mp4", fourcc, 59.84, (h, w))
			i += 1
		video.write(frm)
		fps.update()

	fps.stop()
	video.release()
	cv2.destroyAllWindows()
	vs.stop()
	return video_file_path[:-5]+"_new"+".mp4"

def AudioDetector(audiofile):
	import noisereduce as nr

	model = load_model(str(settings.BASE_DIR) + '\\ambulance_detection\\siren_classification.hdf5')

	def predict(filename):
		audio, sample_rate = librosa.load(filename, res_type='kaiser_fast')
		audio = nr.reduce_noise(y=audio, sr=sample_rate)
		mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
		mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
		mfccs_scaled_features=mfccs_scaled_features.reshape(1,-1)
		predicted_prob=model.predict(mfccs_scaled_features)
		
		if predicted_prob[0,1] >= 0.5:
			return "It's a SIREN \U0001f6a8", str(predicted_prob[0,1]*100)[:5]
		else:
			return "It's just Noise \U0001f4e2", str((1-predicted_prob[0,1])*100)[:5]

	result, score = predict(audiofile)
	return result, score, audiofile