# Smyror v1.1.1
# Weatherbit API key is hidden.

import tkinter as tk
import datetime
import requests
from PIL import Image, ImageTk

class Smyror:
    def __init__(self, master):
        coord = 1290, 441, 1620, 771
        self.master = master
        self.C = tk.Canvas(self.master, bg="blue", width=1920, height=1080, highlightcolor="black", highlightthickness=0)
        self.C.configure(background="black")
        self.C.pack()
        self.time_label = self.C.create_text(860, 280, text="N/A", font="AvenirNextLTPro 50", fill="white")
        self.date = self.C.create_text(860, 380, text="N/A", font="AvenirNextLTPro 40", fill="white")
        self.arc = self.C.create_arc(coord, start=0, extent=0, outline="#333", style=tk.ARC, width=6)
        self.wqi = self.C.create_text(coord[0] + ((coord[2] - coord[0]) / 2), coord[1] + (coord[3] - coord[1]) / 2,
                                      font="AvenirNextLTPro 30", fill="white", text="NaN WQI")

        self.forecast_img = self.C.create_image((50, (1030 * .7) - 200), image="", anchor='nw')
        self.temperature = self.C.create_text((340, (1030 * .7) - 130), text="N/AºF", font="AvenirNextLTPro 25",
                                              fill="white", anchor="nw")
        self.wind = self.C.create_text((860, (1030 * .7) - 80), text="N/A MPH NA", font="AvenirNextLTPro 35",
                                       fill="white")
        self.forecast = self.C.create_text((340, (1030 * .7) - 80), text="Forecast is unavailable.", font="AvenirNextLTPro 20",
                                           fill="white", anchor="nw", width=470)
        # self.update_weather_and_awi("Clear sky", 46)
        self.update_weather()
        self.time()

    def update_weather(self):
        response = requests.get(
            "https://api.weatherbit.io/v2.0/current?city=Rockville,MD&key=[api_key]&units=I").json()
        desc = response['data'][0]['weather']["description"]
        desc_l = desc.lower()
        wind = response['data'][0]['wind_spd']
        direct = response['data'][0]['wind_cdir']
        temp = response['data'][0]['temp']
        image_dict = {"thunderstorms" in desc_l: "thunder", "shower rain" in desc_l or "rain" in desc_l or "drizzle" in desc_l or "hail" in desc_l:"rainy","Clear sky" == desc:"clear","snow shower" in desc_l or "snow" in desc_l or "flurries" == desc_l:"snow","sleet" in desc_l or desc == "Mix snow/rain":"sleet", "clouds" in desc_l:"cloudy"}
        f = ""
        for e, i in enumerate(image_dict):
            if e:
                f =  image_dict[e]
        print(f)
        img = Image.open(f"./assets/{f}.png").resize((200, 200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.C.img = img
        self.C.itemconfig(self.forecast_img, image=img)
        self.C.itemconfig(self.forecast, text=desc)
        self.C.itemconfig(self.wind, text=f"{wind} MPH {direct}")
        self.C.itemconfig(self.temperature, text=f"{temp}ºF")

        self.C.create_text(860, 180, text="Hello.", font="AvenirNextLTPro 50", fill="white")

        self.update_awi(desc, temp, wind)

        self.master.after(600000, self.update_weather)
        # res = urlopen(f"https://www.weatherbit.io/static/img/icons/{icon}.png").read()

    def update_awi(self, condition, temperature, wind):

        awi = 0
        COLOR = ""

        dict = {range(-150, 40): -10, range(40, 45): -5, range(45, 50): -2.5, range(50, 60): -1, range(60, 62): 1, range(62, 65): 2.5, range(65, 68): 5, range(68, 74): 7.5,
                range(74, 79): 10, range(79, 83): 7.5, range(83, 85): 5, range(85, 90): 0, range(90, 95): -5,
                range(95, 190): -10}

        
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


        
        for j, k in enumerate(dict):
            if temperature in k:
                awi += dict[k]

        awi -= wind * 0.1
        dict_color = {"#ed493e":-25 <= awi < -15, "#eb783b":-15 <= awi <= -10, "#eda73e":-10 <= awi < -5, "#eaed3e":-5 <= awi < 0,
                      "#b6ed3e": 0 <= awi <= 10, "#56f580":10 <= awi < 20,
                      "#3eedbb": 20 <= awi < 25}
        for j, k in enumerate(dict_color):
            if dict_color[k]:

                COLOR = k
                print(COLOR)

        deg = ((awi + 25) / 50) * 359
        self.C.itemconfig(self.wqi, text=f"{round(awi, 3)} WQI")
        self.C.itemconfig(self.arc, extent=deg, outline=COLOR)

    def time(self):
        now = datetime.datetime.now()
        time = now.strftime('%I:%M')
        date = now.strftime('%B %d, %Y')
        self.C.itemconfig(self.time_label, text=f"{time}")
        self.C.itemconfig(self.date, text=f"{date}")

        self.master.after(1000, self.time)
