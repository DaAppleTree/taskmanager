from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
import datetime

class HomeworkManagerApp: 
    def __init__(self, root):
        self.root = root
        self.root.title("Homework Manager")
        self.root.geometry("500x500")
        self.root.config(background = "#000000")

        self.MARGIN = 100

        self.assignments = [["2024-08-22 19:00:00", "2024-08-24 22:30:00"], ["2024-08-20 19:00:00", "2024-08-24 23:30:00"], ["2024-01-01 00:00:00", "2025-01-01 00:00:00"]]
        self.tasks = [[3,5],[5,6],[2,7]]
        self.timebars, self.taskbars, self.percents, self.times, self.completion = [], [], [], [], [] 
        
        self.setup()
    
    def setup(self):
        label = Label(self.root, text = "Task Progress:", font=("Arial", 20, "bold"), fg = "#5c9bb7", bg = "#000000")
        label.place(x=150,y=50)

        for i in range(len(self.assignments)):
            green = "#008000"
            red = "#ff0000"

            s1 = ttk.Style()
            s1.theme_use("clam")
            s1.configure("green.Horizontal.TProgressbar", foreground = green, background = green)
            s2 = ttk.Style()
            s2.theme_use("clam")
            s2.configure("red.Horizontal.TProgressbar", foreground = red, background = red)

            timebar = Progressbar(self.root, orient = HORIZONTAL, length = 300, style = "red.Horizontal.TProgressbar")
            timebar.place(x = 100, y = self.MARGIN * i + 100)

            taskbar = Progressbar(self.root, orient = HORIZONTAL, length = 300, style = "green.Horizontal.TProgressbar")
            taskbar.place(x = 100, y = self.MARGIN  * i + 125)

            percent = Label(self.root, text = "0%", font=("Arial", 10), fg = red, bg = "#000000")
            percent.place(x = 50, y = self.MARGIN * i + 100)

            time = Label(self.root, font = ("Arial", 10), fg = "#ffffff", bg = "#000000")
            time.place(x = 200, y = self.MARGIN  * i + 150)

            completed = Label(self.root, font = ("Arial", 10), fg = green, bg = "#000000")
            completed.place(x = 50, y = self.MARGIN * i + 125)

            self.timebars.append(timebar)
            self.taskbars.append(taskbar)
            self.percents.append(percent)
            self.times.append(time)
            self.completion.append(completed)

        for i in range(len(self.assignments)):
            start = datetime.datetime.strptime(self.assignments[i][0], "%Y-%m-%d %H:%M:%S")
            end = datetime.datetime.strptime(self.assignments[i][1], "%Y-%m-%d %H:%M:%S")
            self.update(self.timebars[i], self.taskbars[i], self.percents[i], self.times[i], self.completion[i], start, end, self.tasks[i])

    def update(self, timebar, taskbar, percent, time, completion, start, end, tasks):
        if timebar["value"] < 100:

            passed = int((datetime.datetime.now()-start).total_seconds())
            timebar["value"] = passed / (end-start).total_seconds() * 100
            taskbar["value"] = (tasks[0] / tasks[1]) * 100
            
            percent.config(text = f"{int(passed / (end-start).total_seconds() * 100)}%")
            time.config(text = self.seconds_to_string((end-start).total_seconds()-passed) + " left")
            completion.config(text = f"{int((tasks[0]/tasks[1])*100)}%")

            self.root.update_idletasks()
            self.root.after(10, self.update, timebar, taskbar, percent, time, completion, start, end, tasks)

    def seconds_to_string(self, seconds):
        days = int(seconds//(60*60*24))
        days = str(days) if abs(days) >= 10 else "0" + str(days)

        hours = int(seconds % (60*60*24) //(60*60))
        hours = str(hours) if abs(hours) >= 10 else "0" + str(hours)

        minutes = int(seconds % (60*60) // 60)
        minutes = str(minutes) if abs(minutes) >= 10 else "0" + str(minutes)

        seconds = int(seconds % 60)
        seconds = str(seconds) if abs(seconds) >= 10 else "0" + str(seconds)

        return f"{days}:{hours}:{minutes}:{seconds}"

root = Tk()
app = HomeworkManagerApp(root)
root.mainloop()