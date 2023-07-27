from tkinter import *
from PIL import ImageTk, Image
import requests
import json
import io

url = 'http://api.openweathermap.org/data/2.5/weather'
api_key = '10d816fd2ad802ecc70b04f152c75208'
icon_url = 'http://openweathermap.org/img/wn/{}2x.png'

def get_weather(city):
    params = {'q': city, 'appid': api_key, 'lang': 'tr'}
    data = requests.get(url, params=params).json()

    if data:
        city = data['name'].capitalize()
        country = data["sys"]["country"]
        temp = int(data["main"]["temp"] - 273.15)
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        icon = data["weather"][0]["icon"]
        condition = data["weather"][0]["description"]
        return (city, country, temp, humidity, wind_speed, icon, condition)

def update_weather_label():
    city = cityEntry.get()
    weather = get_weather(city)

    if weather:
        locationLabel["text"] = "{}, {}".format(weather[0], weather[1])
        tempLabel["text"] = '{}°C'.format(weather[2])
        humidityLabel["text"] = "Nem: {}%".format(weather[3])
        windLabel["text"] = "Rüzgar: {} m/s".format(weather[4])
        conditionLabel["text"] = weather[6]

        icon_url = 'http://openweathermap.org/img/wn/{}.png'.format(weather[5])
        response = requests.get(icon_url)
        image_data = response.content

        image = Image.open(io.BytesIO(image_data))
        image = image.resize((125, 125), Image.ANTIALIAS)

        photo = ImageTk.PhotoImage(image)
        iconLabel.config(image=photo)
        iconLabel.image = photo

def on_enter_key(event):
    update_weather_label()

app = Tk()
app.geometry('400x500')
app.title('Hava Durumu')

app.configure(bg='lightblue')

searchFrame = Frame(app, bg='lightblue')
searchFrame.pack(fill=BOTH, padx=10, pady=5)

cityEntry = Entry(searchFrame, justify='center', bg='white', font=("Arial", 14))
cityEntry.pack(side=LEFT, fill=BOTH, expand=True)
cityEntry.focus()

searchButton = Button(searchFrame, text='Ara', font=("Arial", 12), command=update_weather_label)
searchButton.pack(side=LEFT, padx=5)

cityEntry.bind("<Return>", on_enter_key)

iconLabel = Label(app, bg='lightblue')
iconLabel.pack()

locationLabel = Label(app, font=('Arial', 40), bg='lightblue')
locationLabel.pack()

tempLabel = Label(app, font=('Arial', 50, 'bold'), bg='lightblue')
tempLabel.pack()

infoFrame = Frame(app, bg='lightblue')
infoFrame.pack()

conditionLabel = Label(app, font=('Arial', 20), bg='lightblue')
conditionLabel.pack()

humidityLabel = Label(infoFrame, font=('Arial', 16), bg='lightblue')
humidityLabel.pack(side=LEFT, padx=5)

Label(infoFrame, text=" ", bg='lightblue').pack(side=LEFT)

windLabel = Label(infoFrame, font=('Arial', 16), bg='lightblue')
windLabel.pack(side=LEFT, padx=5)

app.mainloop()
