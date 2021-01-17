import base64
import io
import tkinter as tk
import datetime
import PIL
import requests
from PIL import ImageTk, Image
from urllib.request import urlopen
import requests
from io import BytesIO

class Smyror:
    def __init__(self, master):
        coord = 1290, 441, 1620, 771
        self.master = master
        self.canvas = tk.Canvas(self.master, bg="blue", width=1920, height=1080, highlightcolor="black", highlightthickness=0)
        self.canvas.configure(background="black")
        self.canvas.pack()
        self.time_label = self.canvas.create_text(860, 280, text="N/A", font="AvenirNextLTPro 50", fill="white")
        self.date = self.canvas.create_text(860, 380, text="N/A", font="AvenirNextLTPro 40", fill="white")
        self.arc = self.canvas.create_arc(coord, start=0, extent=0, outline="#333", style=tk.ARC, width=6)
        self.wqi = self.canvas.create_text(coord[0] + ((coord[2] - coord[0]) / 2), coord[1] + (coord[3] - coord[1]) / 2 ,
                                      font="AvenirNextLTPro 30", fill="white", text=f"NaN WQI")

        self.forecast_img = self.canvas.create_image((50, (1030 * .7) - 200), image="", anchor='nw')
        self.temperature = self.canvas.create_text((340, (1030 * .7) - 130), text=f"N/AºF", font="AvenirNextLTPro 25",
                                              fill="white", anchor="nw")
        self.wind = self.canvas.create_text((860, (1030 * .7) - 80), text=f"N/A MPH NA", font="AvenirNextLTPro 35",
                                       fill="white")
        self.forecast = self.canvas.create_text((340, (1030 * .7) - 80), text=f"Forecast is unavailable.", font="AvenirNextLTPro 20",
                                           fill="white", anchor="nw", width=470)
        # self.update_weather_and_awi("Clear sky", 46)
        self.update_weather()
        self.time()
        print(self.canvas)
        
    def update_weather(self):
        response = requests.get(
            "https://api.weatherbit.io/v2.0/current?city=Rockville,MD&key=b289f4b7e9a44b4498de1aa1687673ce&units=I").json()
        desc = response['data'][0]['weather']["description"]
        desc_l = desc.lower()
        wind = response['data'][0]['wind_spd']
        direct = response['data'][0]['wind_cdir']
        temp = response['data'][0]['temp']
        image_dict = {"thunderstorm" in desc_l: "thunder", "thunderstorm" not in desc_l and ("shower rain" in desc_l or "rain" in desc_l or "drizzle" in desc_l or "hail" in desc_l):"rainy","Clear sky" == desc:"clear","snow shower" in desc_l or "snow" in desc_l or "flurries" == desc_l:"snow","sleet" in desc_l or desc == "Mix snow/rain":"sleet", "clouds" in desc_l:"cloudy"}
        f = ""
        for e, i in enumerate(image_dict):
            if e:
                f =  image_dict[e]
        img = Image.open(f"./assets/{f}.png").resize((200, 200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.canvas.img = img
        self.canvas.itemconfig(self.forecast_img, image=img)
        self.canvas.itemconfig(self.forecast, text=desc)
        self.canvas.itemconfig(self.wind, text=f"{wind} MPH {direct}")
        self.canvas.itemconfig(self.temperature, text=f"{temp}ºF")

        name = self.canvas.create_text(860, 180, text=f"Hello, Joshua.", font="AvenirNextLTPro 50", fill="white")

        self.update_awi(desc, temp, wind)

        self.master.after(600000, self.update_weather)

    def update_awi(self, condition, temperature, wind):
        awi = 0
        COLOR = ""

        dict_temp = {range(-150, 40): -15, range(40, 45): -7.5, range(45, 50): -5, range(50, 60): 0, range(60, 68): 5, range(68, 74): 7.5,
                range(74, 79): 12.5, range(79, 83): 8, range(83, 85): 5, range(85, 90): 0, range(90, 95): -7,
                range(95, 190): -15}
        
        condition = condition.lower()

        dict_condition = {"heavy" in condition: -10, "overcast" in condition or "scattered" in condition: -5,  "moderate" in condition: -5, "broken" in condition: -3, "light" in condition: -3.5, "few" in condition: -1, "freezing" in condition: -12.5}
        dict_forecast = {"drizzle" in condition: -2.5, "rain" in condition: -5, "snow" in condition: -8, "mix" in condition: -10, "sleet" in condition:-15, "thunder" in condition:-10, "fog" in condition:-2, "clear" in condition: 15, "clouds" in condition:10}

        for e, j in enumerate(dict_condition):
            print(e)

            if e:
                print(dict_condition[e])
                awi += dict_condition[e]

        for exp, _ in enumerate(dict_forecast):
            print(e)

            if exp:
                print(dict_forecast[e])
                awi += dict_forecast[e]


        
        for j, k in enumerate(dict_temp):
            if temperature in k:
                awi += dict_temp[k]

        awi -= wind * 0.1
        dict_color = {"#ed493e":-25 <= awi < -15, "#eb783b":-15 <= awi <= -10, "#eda73e":-10 <= awi < -5, "#eaed3e":-5 <= awi < 0,
                      "#b6ed3e": 0 <= awi <= 10, "#56f580":10 <= awi < 20,
                      "#3eedbb": 20 <= awi < 25}
        for j, k in enumerate(dict_color):
            if dict_color[k]:

                COLOR = k
                print(COLOR)

        deg = ((awi + 25) / 50) * 359
        self.canvas.itemconfig(self.wqi, text=f"{round(awi, 3)} WQI")
        self.canvas.itemconfig(self.arc, extent=deg, outline=COLOR)

    def time(self):
        now = datetime.datetime.now()
        time = now.strftime('%I:%M')
        date = now.strftime('%B %d, %Y')
        self.canvas.itemconfig(self.time_label, text=f"{time}")
        self.canvas.itemconfig(self.date, text=f"{date}")

        self.master.after(1000, self.time)

