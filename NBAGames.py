import tkinter as tk
import requests
from datetime import datetime
from PIL import Image, ImageTk
class NBAGame:
    def __init__(self, master, game_id):
        self.game_id = game_id
        self.sizeH, self.sizeA = (300, 300), (300, 300)
        self.widgets = []
        self.master = master
        self.background_canvas = tk.Canvas(self.master, bg="black", width=1920, height=1080, highlightcolor="black", highlightthickness=0)
        self.canvas = tk.Canvas(self.master, bg="black", width=1920, height=1080, highlightcolor="black", highlightthickness=0)
        # self.canvas.pack() 
        self.time_label = self.canvas.create_text(100, 100, text="", fill="white", font="AvenirNextLTPro 30")

        self.image = self.canvas.create_image((0.25 * 1920 - 300/2, 0.4 * 1080 - 300/2), anchor=tk.NW)
        self.image2 = self.canvas.create_image((0.65 * 1920 - 300/2, 0.4 * 1080 - 300/2), anchor=tk.NW)
        self.tricode_away = self.canvas.create_text((0.25 * 1920 - 300/2) + self.sizeH[0] / 2, (0.4 * 1080 - 300/2) + 350, text="", fill="white", font="AvenirNextLTPro 25")
        self.tricode_home = self.canvas.create_text((0.65 * 1920 - 300/2) + self.sizeA[0] / 2, (0.4 * 1080 - 300/2) + 350, text="", fill="white", font="AvenirNextLTPro 25")
        
        self.record_away = self.canvas.create_text((0.25 * 1920 - 300/2) + self.sizeH[0] / 2, (0.45 * 1080 - 300/2) + 350, text="", fill="white", font="AvenirNextLTPro 25")
        self.record_home = self.canvas.create_text((0.65 * 1920 - 300/2) + self.sizeA[0] / 2, (0.45 * 1080 - 300/2) + 350, text="", fill="white", font="AvenirNextLTPro 25")
        
        self.period = self.canvas.create_text(0.45 * 1920, 0.225 * 1080, fill="white", text="", font="AvenirNextLTPro 35")
        self.arena = self.canvas.create_text(0.45 * 1920, 0.60 * 1080, fill="white", text="", font="AvenirNextLTPro 27")
        self.location = self.canvas.create_text(0.45 * 1920, 0.65 * 1080, fill="white", text="", font="AvenirNextLTPro 23")
        self.away_score = self.canvas.create_text(0.4 * 1920, 0.4 * 1080, fill="white", text="", font="AvenirNextLTPro 45")
        self.home_score = self.canvas.create_text(0.5 * 1920, 0.4 * 1080, fill="white", text="", font="AvenirNextLTPro 45")
        self.info_after = None
        self.time_after = None
        self.update_information_intervally()
        # self.master.after(100000, self.__init__(self.master, self.game_id))
        # self.home_team.image=image_home
        # self.home_team.config(image=image_home)
        
        # image_away = ImageTk.PhotoImage(Image.open(f"./NBALogos/{response['vTeam']['triCode'].lower()}.png").resize((1000, 1000)))
        # self.away_team.image=image_away
        # self.away_team.config(image=image_away)
        #

    def update_information(self):

        date = datetime.now()
        year = date.strftime("%Y")
        month = date.strftime("%m")
        date = date.strftime("%d")
        
        response = requests.get(f"http://data.nba.net/10s/prod/v1/{year}{month}{int(date)}/scoreboard.json").json()['games'][self.game_id - 1]
        image_home = Image.open(f"/home/pi/NBALogos/{response['hTeam']['triCode'].lower()}.png")
        image_away = Image.open(f"/home/pi/NBALogos/{response['vTeam']['triCode'].lower()}.png")
        period = f"Q{response['period']['current']} - {response['clock']}" if 0 < int(response['period']['current']) <= 4 and response['clock'] != '' and response['gameDuration']['hours'] != '' and not response['period']['isHalftime'] else "HALF" if response['period']['isHalftime'] else "FINAL" if response['gameDuration']['hours'] != '' and int(response['period']['current']) == 4 else f"{response['startTimeEastern']}"
        image_home = ImageTk.PhotoImage(image_home.resize(self.sizeH))
        image_away = ImageTk.PhotoImage(image_away.resize(self.sizeA))

        self.master.image_home = image_home
        self.master.image_away = image_away
        self.canvas.itemconfig(self.image, image=image_away)
        self.canvas.itemconfig(self.image2, image=image_home)
        self.canvas.itemconfig(self.period, text=period)
        self.canvas.itemconfig(self.record_away, text=f"({response['vTeam']['win']}-{response['vTeam']['loss']})")
        self.canvas.itemconfig(self.record_home, text=f"({response['hTeam']['win']}-{response['hTeam']['loss']})")
        self.canvas.itemconfig(self.home_score, text=f"{response['hTeam']['score'] if response['hTeam']['score'] != '' else 0}")
        self.canvas.itemconfig(self.away_score, text=f"{response['vTeam']['score'] if response['vTeam']['score'] != '' else 0}")
        self.canvas.itemconfig(self.arena, text=f'{response["arena"]["name"]}')
        self.canvas.itemconfig(self.location, text=f'{response["arena"]["city"]}, {response["arena"]["stateAbbr"]}')
        self.canvas.itemconfig(self.tricode_home, text=f"{response['hTeam']['triCode']}")
        self.canvas.itemconfig(self.tricode_away, text=f"{response['vTeam']['triCode']}")
    
    def update_information_intervally(self):
        self.update_information()
        # self.time()
        self.info_after = self.master.after(10000, self.update_information_intervally)

    def forget_all_widgets(self):
        # self.master.after_cancel(self.time_after)
        
        self.canvas.itemconfig(self.image, image="")
        self.canvas.itemconfig(self.image2, image="")
        self.canvas.itemconfig(self.period, text='')
        self.canvas.itemconfig(self.record_away, text=f"")
        self.canvas.itemconfig(self.record_home, text=f"")
        self.canvas.itemconfig(self.home_score, text=f"")
        self.canvas.itemconfig(self.away_score, text=f"")
        self.canvas.itemconfig(self.arena, text=f'')
        self.canvas.itemconfig(self.location, text=f'')
        self.canvas.itemconfig(self.tricode_home, text=f"")
        self.canvas.itemconfig(self.tricode_away, text=f"") 
        self.canvas.itemconfig(self.time_label, text="")
        self.master.after_cancel(self.info_after)
    # def time(self):
    #     now = datetime.now()
    #     time = now.strftime('%I:%M')
    #     self.canvas.itemconfig(self.time_label, text=f"{time}")
    #     self.time_after = self.master.after(1000, self.time)