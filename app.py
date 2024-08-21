from tkinter import *
from tkinter.ttk import Progressbar, Button
import time


def progress():
    while bar["value"] < 100:
        time.sleep(0.01)
        bar["value"] += 1
        window.update_idletasks()

window = Tk()
window.title("Task Manager")
window.geometry("500x500")
window.config(background = "#000000")

label = Label(window, text = "Task Progress:", 
              font=("Arial", 20, "bold"), 
              fg = "#5c9bb7", 
              bg = "#000000")

label.place(x=150,y=50)


bar = Progressbar(window, orient=HORIZONTAL, length = 300)
bar.place(x=100,y=100)

button = Button(window, text = "Initiate", command = progress)
button.place(x=200, y=200)

window.mainloop()


