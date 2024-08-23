from tkinter import *
from tkinter.ttk import Progressbar
import datetime

class HomeworkManagerApp: 
    def __init__(self, root):
        self.root = root
        self.root.title("Homework Manager")
        self.root.geometry("500x500")
        self.root.config(background = "#000000")

        self.tasks = [["2024-08-22 19:00:00", "2024-08-24 22:30:00"], ["2024-08-20 19:00:00", "2024-08-24 23:30:00"]]
        self.bars, self.percents, self.times = [], [], [] 
        
        self.setup()
    
    def setup(self):
        label = Label(self.root, text = "Task Progress:", font=("Arial", 20, "bold"), fg = "#5c9bb7", bg = "#000000")
        label.place(x=150,y=50)

        for i in range(len(self.tasks)):
            bar = Progressbar(self.root, orient = HORIZONTAL, length = 300)
            bar.place(x = 100, y = 50 * i + 100)

            percent = Label(self.root, text = "0%", font=("Arial", 10, "italic"), fg = "#5c9bb7", bg = "#000000")
            percent.place(x=150, y = 50 * i + 125)

            time = Label(self.root, font = ("Arial", 10, "bold"), fg = "#5c9bb7", bg = "#000000")
            time.place(x = 300, y = 50 * i + 125)

            self.bars.append(bar)
            self.percents.append(percent)
            self.times.append(time)

        for i in range(len(self.tasks)):
            self.bars[i]["value"] = 0
            start = datetime.datetime.strptime(self.tasks[i][0], "%Y-%m-%d %H:%M:%S")
            end = datetime.datetime.strptime(self.tasks[i][1], "%Y-%m-%d %H:%M:%S")
            self.update(self.bars[i], self.percents[i], self.times[i], start, end)

    def update(self, bar, percent, time, start, end):
        if bar["value"] < 100:

            passed = int((datetime.datetime.now()-start).total_seconds())
            bar["value"] = passed / (end-start).total_seconds() * 100
            
            percent.config(text = f"{int(passed / (end-start).total_seconds() * 100)}%")
            time.config(text = self.seconds_to_string((end-start).total_seconds()-passed))

            self.root.update_idletasks()
            self.root.after(10, self.update, bar, percent, time, start, end)

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