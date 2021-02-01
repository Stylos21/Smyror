from Screen import Mirror
from tkinter import Tk
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

root = Tk()
root.attributes("-fullscreen", True)
s = Mirror(root)
ENTRY = "description"
CHANNEL = "channel"
pnconfig = PNConfiguration()
pnconfig.publish_key = "PUBLISH_KEY"
pnconfig.subscribe_key = "SUBSCRIBE_KEY"
pnconfig.uuid = "pepepepepeep"
pubnub = PubNub(pnconfig)
pubnub.add_listener(s)
pubnub.subscribe().channels("channel").with_presence().execute()
root.mainloop()
