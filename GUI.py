import customtkinter
import time as t
import tensorflow as tf
from PIL import Image
import cv2
from funcions import get_examen, mark_circles, respostes_marcades
import copy


def seleccionar_plantilla(): # Mirar que hi hagi algun examen visible i mirar que a cada linia hi ha una sola resposta marcada
	global resposta_seleccionada, respostes_plantilla
	global img_plantilla, amplada

	if not resposta_seleccionada: # S'ha clicat per seleccionar la plantilla
		resposta_seleccionada = True
		#bot_select_resposta.configure(text="Deseleccionar")
		bot_select_resposta.configure(text="Unselect")

		img_plantilla = get_examen(cam_video)

		if type(img_plantilla) != int: # Si s'ha detectat un examen

			img_plantilla, respostes_plantilla = marcar_respostes(img_plantilla, 60)

			img_plantilla = processar_imatge_per_CTK(img_plantilla, amplada)


	else:
		resposta_seleccionada = False
		#bot_select_resposta.configure(text="Seleccionar resposta")
		bot_select_resposta.configure(text="Select answer")


def marcar_respostes(img, num_preguntes):
	# INPUT: imatge (procesada amb la funció get_examen()) i el numero de preguntes que hi ha
	# OUTPUT: imatge donada com a input amb un quadrat indicant cada resposta detectada com a marcada. També llista de booleans dient si cada resposta està marcada o no

	size = 48

	model = tf.keras.models.load_model("xarxa_neuronal")
	result = list(mark_circles(img, num_preguntes))

	respostes = respostes_marcades(model, img, result, 48)

	for n in range(len(respostes)):
		i = result[n]

		if not respostes[n]: # Si el model retorna 0, és a dir que és resposta marcada
			size = 40
			cv2.rectangle(img, (int(i[0]-size/2), int(i[1]-size/2)), (int(i[0]+size/2), int(i[1]+size/2)), (0,255,0), 2)

	return img, respostes

def processar_imatge_per_CTK(img, ampl): # Passa d'imatge normal (per exemple cv2) a una versio compatible amb CTKinter. Necessita de input una imatge i la amplada de la finestra
	mides = img.shape

	img = Image.fromarray(img)
	img = customtkinter.CTkImage(img, size=(ampl, mides[0]/mides[1]*ampl))

	return img

def contar_respostes_correctes(resp_exam, foto_examen): # La foto del examen ha de ser ja processada amb la funcio get_exam() i també tenir les respostes correctes i incorrectes marcades

	resp_plant = respostes_plantilla

	coordenades = list(mark_circles(foto_examen, 60))

	if len(list(resp_plant)) != len(list(resp_exam)) or len(list(resp_plant)) != len(list(coordenades)) or len(list(resp_exam))%3 != 0:
		print("ERROR")
		return

	num_correctes = 0
	num_incorrectes = 0
	num_no_contestades = 0
	num_altres = 0

	img_final = foto_examen

	for i in range(int(len(resp_plant)/3)):
		correctes = 0
		incorrectes = 0

		marcades = 0

		for j in range(3):
			if resp_plant[i*3+j] == resp_exam[i*3+j]:
				correctes += 1
			elif resp_plant[i*3+j] != resp_exam[i*3+j]:
				incorrectes += 1

			if resp_exam[i*3+j] == 0:
				marcades += 1


		x0 = coordenades[i*3][0]
		y0 = coordenades[i*3][1]

		x1 = coordenades[i*3+1][0]
		y1 = coordenades[i*3+1][1]

		x2 = coordenades[i*3+2][0]
		y2 = coordenades[i*3+2][1]

		size = 40

		if marcades > 1:
			num_altres += 1
			img_final = cv2.rectangle(img_final, (int(x0-size/2), int(y0-size/2)), (int(x2+size/2), int(y2+size/2)), (0,0,255), 2)

		elif marcades == 0:
			num_no_contestades += 1
			img_final = cv2.rectangle(img_final, (int(x0-size/2), int(y0-size/2)), (int(x2+size/2), int(y2+size/2)), (255,150,100), 2)

		elif correctes == 3:
			num_correctes += 1
			for j in range(3):
				if resp_exam[i*3+j] == 0 and j == 0: # Si la resposta sha detectat com a marcada
					img_final = cv2.rectangle(img_final, (int(x0-size/2), int(y0-size/2)), (int(x0+size/2), int(y0+size/2)), (0,255,0), 2)

				if resp_exam[i*3+j] == 0 and j == 1: # Si la resposta sha detectat com a marcada
					img_final = cv2.rectangle(img_final, (int(x1-size/2), int(y1-size/2)), (int(x1+size/2), int(y1+size/2)), (0,255,0), 2)

				if resp_exam[i*3+j] == 0 and j == 2: # Si la resposta sha detectat com a marcada
					img_final = cv2.rectangle(img_final, (int(x2-size/2), int(y2-size/2)), (int(x2+size/2), int(y2+size/2)), (0,255,0), 2)

		else:
			num_incorrectes += 1
			for j in range(3):

				if True:
					pass

				elif resp_plant[i*3+j] == 0 and j == 0: # Si la resposta sha detectat com a marcada
					img_final = cv2.rectangle(img_final, (int(x0-size/2), int(y0-size/2)), (int(x0+size/2), int(y0+size/2)), (0,255,0), 2)

				elif resp_plant[i*3+j] == 0 and j == 1: # Si la resposta sha detectat com a marcada
					img_final = cv2.rectangle(img_final, (int(x1-size/2), int(y1-size/2)), (int(x1+size/2), int(y1+size/2)), (0,255,0), 2)

				elif resp_plant[i*3+j] == 0 and j == 2: # Si la resposta sha detectat com a marcada
					img_final = cv2.rectangle(img_final, (int(x2-size/2), int(y2-size/2)), (int(x2+size/2), int(y2+size/2)), (0,255,0), 2)


				if resp_exam[i*3+j] == 0 and j == 0: # Si la resposta sha detectat com a marcada
					img_final = cv2.rectangle(img_final, (int(x0-size/2), int(y0-size/2)), (int(x0+size/2), int(y0+size/2)), (255,0,0), 2)

				if resp_exam[i*3+j] == 0 and j == 1: # Si la resposta sha detectat com a marcada
					img_final = cv2.rectangle(img_final, (int(x1-size/2), int(y1-size/2)), (int(x1+size/2), int(y1+size/2)), (255,0,0), 2)

				if resp_exam[i*3+j] == 0 and j == 2: # Si la resposta sha detectat com a marcada
					img_final = cv2.rectangle(img_final, (int(x2-size/2), int(y2-size/2)), (int(x2+size/2), int(y2+size/2)), (255,0,0), 2)


	return [num_correctes, num_incorrectes, num_no_contestades, num_altres, img_final]





def corregir_examen(): # Mirar que hi hagi alguna plantilla seleccionada i algun examen visible
	global corregint_examen, img_corregit, respostes_plantilla, amplada, cam_video, text_respostes

	if not corregint_examen and resposta_seleccionada: # Corregim el examen
		corregint_examen = True
		#bot_corregir.configure(text="Seguent examen")
		bot_corregir.configure(text="Next exam")



		model = tf.keras.models.load_model("xarxa_neuronal")

		img_corregit = get_examen(cam_video)

		if type(img_corregit) == int:
			corregint_examen = False
			return

		result = list(mark_circles(img_corregit, 60))

		respostes = respostes_marcades(model, img_corregit, result, 48)

		size = 40

		for n in range(len(respostes)):
			i = result[n]

			if not respostes[n]: # Si el model retorna 0, és a dir que és resposta marcada
				break
				img_corregit = cv2.rectangle(img_corregit, (int(i[0]-size/2), int(i[1]-size/2)), (int(i[0]+size/2), int(i[1]+size/2)), (255,0,0), 2)


		for n in range(len(respostes_plantilla)):
			i = result[n]

			if not respostes_plantilla[n]: # Si el model retorna 0, és a dir que és resposta marcada
				break
				img_corregit = cv2.rectangle(img_corregit, (int(i[0]-size/2), int(i[1]-size/2)), (int(i[0]+size/2), int(i[1]+size/2)), (0,255,0), 2)

		a,b,c,d,img_corregit = contar_respostes_correctes(respostes, img_corregit)
		img_corregit = processar_imatge_per_CTK(img_corregit, amplada)

		#text = "Correctes: "
		text = "Correct: "

		text += str(a)

		#text += "\nIncorrectes: "
		text += "\nIncorrect: "

		text += str(b)

		#text += "\nNo contestades: "
		text += "\nNot answered: "

		text += str(c)

		#text += "\nAltres: "
		text += "\nOther: "

		text += str(d)

		print(text)

		text_respostes.configure(text=text)


	else: # Preparem per mirar el seguent examen
		corregint_examen = False
		#bot_corregir.configure(text="Corregir examen")
		bot_corregir.configure(text="Grade exam")
		text_respostes.configure(text="")



def update_video():
	global cam_video, amplada, img_corregit, corregint_examen

	ret, cam_video = cap.read()
	cam_video = cv2.cvtColor(cam_video, cv2.COLOR_RGB2BGR)

	if not ret: # Si hi ha hagut un error en la lectura del video
		app.after(100, update_video)
		return

	amplada = (app.winfo_width()-120)/3

	video_frame = processar_imatge_per_CTK(cam_video, amplada)

	mides = cam_video.shape

	if amplada <= 0 or mides[0]/mides[1]*amplada <= 0: # Si la imatge del video es massa petita (mida 0)
		app.after(100, update_video)
		return

	# Primer video (sempre s'actualitza)

	img_cam_feed.configure(image=video_frame)

	# Segon video

	if not resposta_seleccionada: # Si no s'ha clicat el boto per seleccionar la resposta
		img_resposta.configure(image=video_frame)

	elif type(img_plantilla) != int: # Si s'ha clicat el boto per seleccionar la resposta
		img_resposta.configure(image=img_plantilla)

		# Pot ser que ningun dels ifs siguin True, aixo passa quan s'ha clicat el boto per seleccionar la resposta pero no ha pogut detectar cap examen


	# Tercer video
	
	if resposta_seleccionada and not corregint_examen:
		aux = get_examen(cam_video)

		if type(aux) != int: # Si es detecta un examen

			aux = processar_imatge_per_CTK(aux, amplada)
			img_examen.configure(image=aux)

		else:
			img_examen.configure(image=video_frame)

	elif resposta_seleccionada and corregint_examen:
		img_examen.configure(image=img_corregit)

	else:
		img_examen.configure(image=video_frame)
		corregint_examen = False


	# Final de la funció
	
	app.after(100, update_video)


# variables globals dels estats possibles

resposta_seleccionada = False
corregint_examen = False

img_plantilla = []
img_corregit = []

respostes_plantilla = [] # llista de booleans amb 0 si la resposta esta marcada i 1 si es creu que no ho està

amplada = 0

cap = cv2.VideoCapture(0)
ret, cam_video = cap.read()
aux = []


# Comença l'iniciació de la app

app = customtkinter.CTk()
app.title("corrector")
app.geometry("1080x720")

# Botons

#bot_corregir = customtkinter.CTkButton(app, text="Corregir examen", command=corregir_examen)
bot_corregir = customtkinter.CTkButton(app, text="Grade exam", command=corregir_examen)
bot_corregir.grid(row=1, column=2, padx=20, pady=20)

#bot_select_resposta = customtkinter.CTkButton(app, text="Seleccionar resposta", command=seleccionar_plantilla)
bot_select_resposta = customtkinter.CTkButton(app, text="Select answer", command=seleccionar_plantilla)
bot_select_resposta.grid(row=1, column=1, padx=20, pady=20)


# Videos

amplada = (1080-120)/3

video_frame = processar_imatge_per_CTK(cam_video, amplada)

img_cam_feed = customtkinter.CTkLabel(app, image=video_frame, text="")
img_cam_feed.grid(column=0, row = 0, padx=20, pady=20)

img_resposta = customtkinter.CTkLabel(app, image=video_frame, text="")
img_resposta.grid(column=1, row = 0, padx=20, pady=20)

img_examen = customtkinter.CTkLabel(app, image=video_frame, text="")
img_examen.grid(column=2, row = 0, padx=20, pady=20)

# Labels

text_respostes = customtkinter.CTkLabel(app, text="")
text_respostes.grid(column = 0, row = 1, padx = 20, pady = 20)

# Final de l'inicialització

app.after(100, update_video)
app.mainloop()