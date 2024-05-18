import os
from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from PIL import Image, ImageTk
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API")

if not API_KEY:
    raise ValueError("API ключ не знайдений. Переконайтесь, що файл .env містить рядок API=ваш_API_ключ")

root = Tk()
root.title("Weather App for Татусько")
root.geometry("890x470+300+200")
root.configure(bg="#57adff")
root.resizable(False, False)

def getWeather():
    city = textfield.get()

    # Geolocation
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        location = geolocator.geocode(city)
        if not location:
            messagebox.showerror("Error", "City not found")
            return
    except Exception as e:
        messagebox.showerror("Error", f"Geocoding error: {e}")
        return
    
    obj = TimezoneFinder()
    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
    
    timezone.config(text=result)
    long_lat.config(text=f"{round(location.latitude, 4)}°N, {round(location.longitude, 4)}°E")

    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock.config(text=current_time)
    
    # Weather API request
    BASE_URL = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": API_KEY,
        "q": f"{location.latitude},{location.longitude}",
        "days": 7,
        "aqi": "no",
        "alerts": "no"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        messagebox.showerror("Error", f"HTTP error: {err}")
        return
    except Exception as err:
        messagebox.showerror("Error", f"Error: {err}")
        return

    data = response.json()

    # Current weather
    current = data['current']
    temp = current['temp_c']
    humidity = current['humidity']
    pressure = current['pressure_mb']
    wind = current['wind_kph']
    description = current['condition']['text']

    t.config(text=f"{temp} °C")
    h.config(text=f"{humidity} %")
    p.config(text=f"{pressure} гПа")
    w.config(text=f"{wind} км/год")
    d.config(text=description)
    
    # Forecast for 7 days
    forecast = data['forecast']['forecastday']
    for i, frame in enumerate(frames):
        day = forecast[i + 1]
        day_name = datetime.strptime(day['date'], '%Y-%m-%d').strftime("%A")
        day_temp = day['day']['avgtemp_c']
        night_temp = day['day']['mintemp_c']
        icon = day['day']['condition']['icon']

        # Update labels and images
        frames[i]['day_label'].config(text=day_name)
        frames[i]['temp_label'].config(text=f"Day: {day_temp}°C\nNight: {night_temp}°C")

        img = Image.open(requests.get(f"http:{icon}", stream=True).raw)
        resized_image = img.resize((50, 50))
        photo = ImageTk.PhotoImage(resized_image)
        frames[i]['icon_label'].config(image=photo)
        frames[i]['icon_label'].image = photo

# Icon
image_icon = PhotoImage(file="images/logo.png")
root.iconphoto(False, image_icon)

Round_box = PhotoImage(file="images/Rounded Rectangle 1.png")
Label(root, image=Round_box, bg="#57adff").place(x=30, y=110)

# Labels
label1 = Label(root, text="Температура", font=('Times New Roman', 11), fg="white", bg="#203243")
label1.place(x=50, y=120)

label2 = Label(root, text="Вологість", font=('Times New Roman', 11), fg="white", bg="#203243")
label2.place(x=50, y=140)

label3 = Label(root, text="Тиск", font=('Times New Roman', 11), fg="white", bg="#203243")
label3.place(x=50, y=160)

label4 = Label(root, text="Швидкість вітру", font=('Times New Roman', 11), fg="white", bg="#203243")
label4.place(x=50, y=180)

label5 = Label(root, text="Опис", font=('Times New Roman', 11), fg="white", bg="#203243")
label5.place(x=50, y=200)

# Search box
Search_image = PhotoImage(file="Images/Rounded Rectangle 3.png")
myimage = Label(image=Search_image, bg="#57adff")
myimage.place(x=270, y=120)

weat_image = PhotoImage(file="images/Layer 7.png")
weatherimage = Label(root, image=weat_image, bg="#203243")
weatherimage.place(x=290, y=127)

textfield = tk.Entry(root, justify='center', width=15, font=('poppins', 25, 'bold'), bg="#203243", border=0, fg="white")
textfield.place(x=370, y=130)
textfield.focus()

Search_icon = PhotoImage(file="images/Layer 6.png")
myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#203243", command=getWeather)
myimage_icon.place(x=645, y=125)

# Bottom box
frame = Frame(root, width=900, height=180, bg="#212120")
frame.pack(side=BOTTOM)

# Bottom boxes
firstbox = PhotoImage(file="images/Rounded Rectangle 2.png")
secondbox = PhotoImage(file="images/Rounded Rectangle 2 copy.png")

Label(frame, image=firstbox, bg="#212120").place(x=30, y=20)
Label(frame, image=secondbox, bg="#212120").place(x=300, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=400, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=500, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=600, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=700, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=800, y=30)

# Clock
clock = Label(root, font=("Times New Roman", 30, 'bold'), fg="white", bg="#57adff")
clock.place(x=30, y=20)

# Timezone
timezone = Label(root, font=("Times New Roman", 20), fg="white", bg="#57adff")
timezone.place(x=700, y=20)

long_lat = Label(root, font=("Times New Roman", 10), fg="white", bg="#57adff")
long_lat.place(x=700, y=50)

# Current weather info
t = Label(root, font=("Times New Roman", 11), fg="white", bg="#203243")
t.place(x=150, y=120)
h = Label(root, font=("Times New Roman", 11), fg="white", bg="#203243")
h.place(x=150, y=140)
p = Label(root, font=("Times New Roman", 11), fg="white", bg="#203243")
p.place(x=150, y=160)
w = Label(root, font=("Times New Roman", 11), fg="white", bg="#203243")
w.place(x=150, y=180)
d = Label(root, font=("Times New Roman", 11), fg="white", bg="#203243")
d.place(x=150, y=200)

# Define forecast frames
frames = [
    {"frame": Frame(root, width=230, height=132, bg="#282829"), "day_label": None, "icon_label": None, "temp_label": None},
    {"frame": Frame(root, width=70, height=115, bg="#282829"), "day_label": None, "icon_label": None, "temp_label": None},
    {"frame": Frame(root, width=70, height=115, bg="#282829"), "day_label": None, "icon_label": None, "temp_label": None},
    {"frame": Frame(root, width=70, height=115, bg="#282829"), "day_label": None, "icon_label": None, "temp_label": None},
    {"frame": Frame(root, width=70, height=115, bg="#282829"), "day_label": None, "icon_label": None, "temp_label": None},
    {"frame": Frame(root, width=70, height=115, bg="#282829"), "day_label": None, "icon_label": None, "temp_label": None}
]

positions = [(35, 325), (235, 325), (325, 325), (415, 325), (505, 325), (595, 325)]
for i, pos in enumerate(positions):
    frames[i]["frame"].place(x=pos[0], y=pos[1])
    frames[i]["day_label"] = Label(frames[i]["frame"], font="arial 20", bg="#282829", fg="#fff")
    frames[i]["day_label"].place(x=5, y=5)
    frames[i]["icon_label"] = Label(frames[i]["frame"], bg="#282829")
    frames[i]["icon_label"].place(x=5, y=40)
    frames[i]["temp_label"] = Label(frames[i]["frame"], bg="#282829", fg="#57adff", font="arial 15 bold")
    frames[i]["temp_label"].place(x=5, y=90)

root.mainloop()
