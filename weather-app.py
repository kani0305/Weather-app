import tkinter as tk
from PIL import Image, ImageTk
import requests

# --- API Setup ---
API_KEY = "428cb573d8d90cda74002d9ee23c4a66"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather():
    city = city_entry.get().strip()
    if city:
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            main = data['main']
            weather = data['weather'][0]
            temp = main['temp']
            humidity = main['humidity']
            condition = weather['description'].title()

            # Update labels
            result_label.config(text=f"{city.title()}\n🌡 {temp} °C\n💧 {humidity}%\n☁ {condition}")

            # Choose icon
            icon_code = weather['icon']  # e.g., "01d", "02n"
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

            # Download icon dynamically
            icon_response = requests.get(icon_url, stream=True)
            if icon_response.status_code == 200:
                with open("weather_icon.png", "wb") as f:
                    f.write(icon_response.content)
                img = Image.open("weather_icon.png").resize((80, 80))
                weather_icon = ImageTk.PhotoImage(img)
                icon_label.config(image=weather_icon)
                icon_label.image = weather_icon
        else:
            result_label.config(text="❌ City not found!")
            icon_label.config(image="")
    else:
        result_label.config(text="⚠ Please enter a city name.")
        icon_label.config(image="")

root = tk.Tk()
root.title("🌍 Weather App")
root.geometry("400x400")
root.config(bg="#87CEEB")  # light sky blue background

title_label = tk.Label(root, text="🌦 Weather App", font=("Arial", 18, "bold"), bg="#87CEEB")
title_label.pack(pady=10)

city_entry = tk.Entry(root, font=("Arial", 14), justify="center")
city_entry.pack(pady=5)


get_button = tk.Button(root, text="Get Weather", command=get_weather, font=("Arial", 12), bg="white")
get_button.pack(pady=10)

icon_label = tk.Label(root, bg="#87CEEB")
icon_label.pack()

result_label = tk.Label(root, text="", font=("Arial", 14), bg="#87CEEB", justify="center")
result_label.pack(pady=20)

root.mainloop()