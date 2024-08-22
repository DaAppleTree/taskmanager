from tkinter import *
from tkinter.ttk import Progressbar, Button
import time, datetime

def initiate():
    bar["value"] = 0
    update(start_date, timeframe)

def update(start, interval):
    if bar["value"] < 100:
        bar["value"] = ((datetime.datetime.now()-start).total_seconds()/ interval) * 100
        w.update_idletasks()
        w.after(10, update, start, interval)

w = Tk()
w.title("Task Manager")
w.geometry("500x500")
w.config(background = "#000000")

s1, s2 = "2024-08-22 17:30:00", "2024-08-23 17:30:00"
start_date = datetime.datetime.strptime(s1, "%Y-%m-%d %H:%M:%S")
end_date = datetime.datetime.strptime(s2, "%Y-%m-%d %H:%M:%S")
timeframe = (end_date-start_date).total_seconds()

label = Label(w, text = "Task Progress:", 
              font=("Arial", 20, "bold"), 
              fg = "#5c9bb7", 
              bg = "#000000")

label.place(x=150,y=50)


bar = Progressbar(w, orient=HORIZONTAL, length = 300)
bar.place(x=100,y=100)

button = Button(w, text = "Initiate", command = lambda: initiate())
button.place(x=200, y=200)

w.mainloop()