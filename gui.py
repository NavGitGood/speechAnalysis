import tkinter as tk
import requests
import emoji
from PIL import Image, ImageTk

HEIGHT = 1000
WIDTH = 1000

def format_response(weather):
	try:
		name = weather['name']
		desc = weather['weather'][0]['description']
		temp = weather['main']['temp']

		final_str = 'City: %s \nConditions: %s \nTemperature (°F): %s' % (name, desc, temp)
	except:
		final_str = 'There was a problem retrieving that information'

	return final_str

def get_weather(city):
	weather_key = 'a4aa5e3d83ffefaba8c00284de6ef7c3'
	url = 'https://api.openweathermap.org/data/2.5/weather'
	params = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
	response = requests.get(url, params=params)
	weather = response.json()

	label['text'] = format_response(weather)

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image = tk.PhotoImage(file='landscape.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text="Get Weather", font=40, command=lambda: get_weather(entry.get()))
button.place(relx=0.7, relheight=1, relwidth=0.3)

lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.75, anchor='n')

# print(lower_frame.winfo_height())
# print(lower_frame.winfo_width())

img_height = int(lower_frame.winfo_height()*0.1)
img_width = int(lower_frame.winfo_width()*0.1)
photo = ImageTk.PhotoImage(Image.open('WPVG_icon_2016.png').resize((62,58)))

# photo = tk.PhotoImage(file="WPVG_icon_2016.png")

label = tk.Label(lower_frame, image=photo)
label.place(relx=0.0, rely=0.0, relwidth=0.1, relheight=0.1)

print(label.winfo_reqheight())
print(label.winfo_reqwidth())

label1 = tk.Label(lower_frame, image=photo)
label1.place(relx=0.0, rely=0.2, relwidth=0.1, relheight=0.1)
label2 = tk.Label(lower_frame, image=photo)
label2.place(relx=0.0, rely=0.4, relwidth=0.1, relheight=0.1)

root.mainloop()

def append_transcript(transcript):
    label['text'] = label.cget('text') + '\n' + transcript
