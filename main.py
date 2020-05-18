# pip install speechrecognition
# pip install wheel
# pip install wave
# pip install pyaudio
# pip install playsound
# pip install gTTS
# pip install pyObjC # Mac Only
# ----------------------------------------------
# pip install pipwin (if problems with pyaudio)
# pipwin install pyaudio
# ----------------------------------------------
import speech_recognition as sr
import webbrowser, os, playsound, random
from gtts import gTTS
from time import ctime, sleep

class TupaAssistance:
	def __init__(self):
		self.r = sr.Recognizer()
		self.r.energy_threshold = 400
		
		self.mic = sr.Microphone(1)
		
		sleep(1)
		while True:
			self.respuesta(self.listen())

	def listAudioHardware(self):
		for index, name in enumerate(sr.Microphone.list_microphone_names()):
				print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

	def habla(self, texto):
		tts = gTTS(text=texto, lang="es")
		fName = random.randint(1,1000)
		audio = "audio-"+str(fName)+".mp3"
		tts.save(audio)
		playsound.playsound(audio)
		print("TUPA: "+ texto)
		os.remove(audio)

	def listen(self, prompt = "¿Hola en que te puedo ayudar?"):
		with self.mic as source:
			voice_data = ""
			
			print('\033[93m'+"\nSe esta calibrando el microfono...\n"+'\033[0m')
			self.r.adjust_for_ambient_noise(source, 5)
			self.r.dynamic_energy_threshold = True 

			print('\033[95m' + prompt + '\033[0m')
			
			try:
				audio = self.r.listen(source)
				voice_data = self.r.recognize_google(audio, language="es-MX")
				return voice_data
			except sr.UnknownValueError:
				self.habla("No te entendi ni papa!")
			except sr.RequestError:
				self.habla("Ups, no hay servicio")

	def respuesta(self, audio_data):
		data = str(audio_data).lower()
		print("=> "+ data)

		if 'cómo te llamas' in data:
			self.habla("Mi nombre es Tupa, Tupa la Obeja")

		if 'qué día es hoy' in data:
			self.habla(str(ctime()))
		
		if 'busca' in data:
			prompt = "¿Qué quieres buscar?"
			self.habla(prompt)
			search = self.listen(prompt=prompt)
			url = "https://www.google.com/search?q="+ str(search)
			webbrowser.get().open(url)
			self.habla("Aqui es lo que encontre respecto a "+ str(search))

		if 'traduce' in data:
			prompt = "¿Qué quieres traducir?"
			self.habla(prompt)
			search = self.listen(prompt=prompt)
			url = "https://translate.google.com/?hl=es#view=home&op=translate&sl=es&tl=en&text="+ str(search)
			webbrowser.get().open(url)
			self.habla("Aqui esta la traduccion de "+ str(search))

		if 'localiza' in data:
			prompt = "¿Qué quieres localizar?"
			self.habla(prompt)
			search = self.listen(prompt=prompt)
			url = "https://www.google.com/maps/place/"+ str(search)
			webbrowser.get().open(url)
			self.habla("Aqui estan las "+ str(search))
		
		if 'descansa' in data:
			self.habla("Nos vemos.")
			playsound.playsound("audio/sheep.mp3")
			exit(0)

if __name__ == "__main__":
	TupaAssistance()
