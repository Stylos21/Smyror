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
pnconfig.publish_key = "pub-c-bc20a898-d25e-4f56-ab48-425a6cc55f09"
pnconfig.subscribe_key = "sub-c-ffe2fd82-607d-11ea-8216-b6c21e45eadc"
pnconfig.uuid = "pepepepepeep"
pubnub = PubNub(pnconfig)
pubnub.add_listener(s)
pubnub.subscribe().channels("channel").with_presence().execute()
root.mainloop()