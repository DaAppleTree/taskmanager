from tkinter import *
from tkinter.ttk import Progressbar, Button
import datetime

def initiate():
    for i in range(len(bars)):
        bars[i]["value"] = 0
        update(bars[i], labels[i], times_left[i], start_date, timeframe)

def update(bar, label, timeleft, start, interval):
    if bar["value"] < 100:

        passed = int((datetime.datetime.now()-start).total_seconds())
        bar["value"] = passed / interval * 100
        label.config(text = f"{int(passed / interval * 100)}%")

        timeleft.config(text = seconds_to_string(interval-passed))
        w.update_idletasks()
        w.after(10, update, bar, label, timeleft, start, interval)

def seconds_to_string(seconds):
    days = int(seconds//(60*60*24))
    daysstr = str(days) if days >= 10 else "0" + str(days)

    hours = int(seconds % (60*60*24) //(60*60))
    hoursstr = str(hours) if hours >= 10 else "0" + str(hours)

    minutes = int(seconds % (60*60) // 60)
    minutesstr = str(minutes) if minutes >= 10 else "0" + str(minutes)

    seconds = int(seconds % 60)
    secondsstr = str(seconds) if seconds >= 10 else "0" + str(seconds)

    return f"{daysstr}:{hoursstr}:{minutesstr}:{secondsstr}"

w = Tk()
w.title("Task Manager")
w.geometry("500x500")
w.config(background = "#000000")

s1, s2 = "2024-08-22 19:00:00", "2024-08-24 22:30:00"
start_date = datetime.datetime.strptime(s1, "%Y-%m-%d %H:%M:%S")
end_date = datetime.datetime.strptime(s2, "%Y-%m-%d %H:%M:%S")
timeframe = (end_date-start_date).total_seconds()

label = Label(w, text = "Task Progress:", 
              font=("Arial", 20, "bold"), 
              fg = "#5c9bb7", 
              bg = "#000000")

label.place(x=150,y=50)

tasks = 2
bars, labels, times_left = [], [], []
for i in range(tasks):
    bar = Progressbar(w, orient = HORIZONTAL, length = 300)
    bar.place(x = 100, y = 50 * i + 100)

    label = Label(w, text = "0%", font=("Arial", 10, "italic"), fg = "#5c9bb7", bg = "#000000")
    label.place(x=150, y = 50 * i + 125)

    time_left = Label(w, font = ("Arial", 10, "bold"), fg = "#5c9bb7", bg = "#000000")
    time_left.place(x = 300, y = 50 * i + 125)

    bars.append(bar)
    labels.append(label)
    times_left.append(time_left)

button = Button(w, text = "Initiate", command = lambda: initiate())
button.place(x=200, y=200)

w.mainloop()