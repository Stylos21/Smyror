import tkinter as tk
from Window import Smyror
from NBAGames import NBAGame
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
class Mirror(SubscribeCallback):
    def __init__(self, master):
        self.master = master
        self.active_class = Smyror(self.master)
        self.active_screen = self.active_class.canvas
        self.active_screen.pack()

    def presence(self, pubnub, event):
        print("[PRESENCE: {}]".format(event.event))
        print("uuid: {}, channel: {}".format(event.uuid, event.channel))

    def status(self, pubnub, event):
        if event.category == PNStatusCategory.PNConnectedCategory:
            print("[STATUS: PNConnectedCategory]")
            print("connected to channels: {}".format(event.affected_channels))

    def message(self, pubnub, event):
        if type(event.message) == int:

            if type(self.active_class).__name__ == "NBAGame":
                # for widget in self.active_class.widgets[0]:
                #     print(self.active_screen[widget])
                #     widget.pack_forget()
                # print(self.active_screen.find_all())
                self.active_class.forget_all_widgets()
                # self.active_screen.delete('all')
                self.active_class.game_id = int(event.message)
                self.active_class.update_information_intervally()
                self.active_screen = self.active_class.canvas
                self.active_screen.pack()

                # self.active_class.update_information()
                # self.active_screen = self.active_class.canvas

            else:
                self.active_screen.pack_forget()
                self.active_class = NBAGame(self.master, int(event.message))
                self.active_class.update_information()
                self.active_screen = self.active_class.canvas
                self.active_screen.pack()

        else:
            print("SWITCHING TO WEATHER !")
            if type(self.active_class).__name__ == "NBAGame":
                self.active_class.forget_all_widgets()
                self.active_class.canvas.pack_forget()
                self.active_class = Smyror(self.master)
                self.active_screen = self.active_class.canvas
                self.active_screen.pack()
        # self.active_class = NBAGame(self.master, int(event.message))
        
        # del self.active_screen
        # self.active_screen = self.canvas_nbagames
        


# root = tk.Tk()
# root.attributes('-fullscreen', True)
# mirror = Mirror(root)
# root.mainloop()
