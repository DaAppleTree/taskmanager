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

        self.MARGIN = 120

        self.GREEN = "#008000"
        self.RED = "#ff0000"
        self.WHITE = "#ffffff"
        self.BLACK = "#000000"

        self.assignments = [["2024-08-22 19:00:00", "2024-08-24 22:30:00"], ["2024-08-20 19:00:00", "2024-08-24 23:30:00"], ["2024-01-01 00:00:00", "2025-01-01 00:00:00"]]
        self.tasks = [Task(["code", "complete"]), Task(["cry", "cry", "happy"]), Task(["no", "yes", "no", "yes"])]
        self.timebars, self.taskbars, self.percents, self.times, self.completions, self.currents, self.buttons = [], [], [], [], [], [], []
        
        self.setup()
    
    def setup(self):
        label = Label(self.root, text = "Task Progress:", font=("Arial", 20, "bold"), fg = "#5c9bb7", bg = "#000000")
        label.place(x=150,y=50)

        green_style = ttk.Style()
        green_style.theme_use("clam")
        green_style.configure("green.Horizontal.TProgressbar", foreground = self.GREEN, background = self.GREEN)

        red_style = ttk.Style()
        red_style.theme_use("clam")
        red_style.configure("red.Horizontal.TProgressbar", foreground = self.RED, background = self.RED)

        for i in range(len(self.assignments)):
            timebar = Progressbar(self.root, orient = HORIZONTAL, length = 300, style = "red.Horizontal.TProgressbar")
            timebar.place(x = 100, y = self.MARGIN * i + 100)

            taskbar = Progressbar(self.root, orient = HORIZONTAL, length = 300, style = "green.Horizontal.TProgressbar")
            taskbar.place(x = 100, y = self.MARGIN  * i + 125)

            percent = Label(self.root, text = "0%", font=("Arial", 10), fg = self.RED, bg = self.BLACK)
            percent.place(x = 50, y = self.MARGIN * i + 100)

            time = Label(self.root, font = ("Arial", 10), fg = self.WHITE, bg = self.BLACK)
            time.place(x = 200, y = self.MARGIN  * i + 150)

            completion = Label(self.root, font = ("Arial", 10), fg = self.GREEN, bg = self.BLACK)
            completion.place(x = 50, y = self.MARGIN * i + 125)

            current = Label(self.root, font = ("Ink", 10, "bold"), fg = self.WHITE, bg = self.BLACK)
            current.place(x = 400, y = self.MARGIN * i + 100)

            button = Button(self.root, font = ("Arial", 10, "bold"), text = "complete")
            button.place(x = 200, y = self.MARGIN * i + 170)

            self.timebars.append(timebar)
            self.taskbars.append(taskbar)
            self.percents.append(percent)
            self.times.append(time)
            self.completions.append(completion)
            self.currents.append(current)
            self.buttons.append(button)
        
        for i in range(len(self.tasks)):
            self.currents[i].bind("<Enter>", lambda event, idx = i: self.hovered(event, idx, True))
            self.currents[i].bind("<Leave>", lambda event, idx = i: self.hovered(event, idx, False))

        for i in range(len(self.assignments)):
            self.update(i)

    def update(self, i):
        if self.timebars[i]["value"] < 100:
            start = datetime.datetime.strptime(self.assignments[i][0], "%Y-%m-%d %H:%M:%S")
            end = datetime.datetime.strptime(self.assignments[i][1], "%Y-%m-%d %H:%M:%S")
            passed = int((datetime.datetime.now()-start).total_seconds())
            self.timebars[i]["value"] = passed / (end-start).total_seconds() * 100
            self.taskbars[i]["value"] = ((self.tasks[i].current) / len(self.tasks[i].tasks)) * 100
            
            self.percents[i].config(text = f"{int(passed / (end-start).total_seconds() * 100)}%")
            self.times[i].config(text = self.seconds_to_string((end-start).total_seconds()-passed) + " left")
            self.completions[i].config(text = f"{int(((self.tasks[i].current) / len(self.tasks[i].tasks)) * 100)}%")
            self.buttons[i].config(command = lambda: self.tasks[i].complete())

            self.tasks[i].show(self.currents[i])

            self.root.update_idletasks()
            self.root.after(10, self.update, i)

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
    
    def hovered(self, event, i, state):
        self.tasks[i].hovered = state


class Task:
    def __init__(self, tasks):
        self.tasks = tasks
        self.current = 0
        self.hovered = False
    
    def complete(self):
        if self.current < len(self.tasks):
            self.current += 1
    
    def show(self, label):
        if not self.hovered:
            if self.current < len(self.tasks):
                label.config(text = f"Next Objective:\n{self.current+1}. {self.tasks[self.current]}")
            else:
                label.config(text = "Complete!")
        else:
            tasklist = ""
            for i in range(len(self.tasks)):
                tasklist += f"{i+1}. {self.tasks[i]}\n"
            label.config(text = tasklist)


root = Tk()
app = HomeworkManagerApp(root)
root.mainloop()
