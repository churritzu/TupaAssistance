import speech_recognition as sr
import webbrowser, os, playsound, random
from gtts import gTTS
from time import ctime, sleep

class TupaAssistance:
	def __init__(self):
		self.r = sr.Recognizer()
		self.r.energy_threshold = 4000
		
		self.mic = sr.Microphone()
		
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
		print("TUPA: "+ texto+"\n")
		os.remove(audio)

	def listen(self, prompt = "¿Hola en que te puedo ayudar?"):
		with self.mic as source:
			voice_data = ""
			self.r.adjust_for_ambient_noise(source, 5)
			self.r.dynamic_energy_threshold = True 

			print(prompt)
			
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
		
		if 'buscar' in data:
			prompt = "¿Qué quieres buscar?"
			self.habla(prompt)
			search = self.listen(prompt=prompt)
			url = "https://www.google.com/search?q="+ str(search)
			webbrowser.get().open(url)
			self.habla("Aqui es lo que encontre respecto a "+ str(search)+"\n")

		if 'traducir' in data:
			prompt = "¿Qué quieres traducir?"
			self.habla(prompt)
			search = self.listen(prompt=prompt)
			url = "https://translate.google.com/?hl=es#view=home&op=translate&sl=es&tl=en&text="+ str(search)
			webbrowser.get().open(url)
			self.habla("Aqui esta la traduccion de "+ str(search)+"\n")

		if 'localizar' in data:
			prompt = "¿Qué quieres localizar?"
			self.habla(prompt)
			search = self.listen(prompt=prompt)
			url = "https://www.google.com.mx/maps/search/"+ str(search+"\n")
			# url = "https://www.google.com/maps/place/"+ str(search+"\n")
			webbrowser.get().open(url)
			self.habla("Aqui estan las "+ str(search))
		
		if 'descansar' in data:
			self.habla("Nos vemos.")
			playsound.playsound("audio/sheep.mp3")
			exit(0)

if __name__ == "__main__":
	TupaAssistance()
