import tkinter as tk
from Window import Smyror

root = tk.Tk()
root.attributes('-fullscreen', True)
main_frame = tk.Frame(root)
main_frame.config(background="black", cursor='none')
main_frame.pack(fill=tk.BOTH, expand=tk.TRUE)
mirror = Smyror(root)
root.mainloop()
