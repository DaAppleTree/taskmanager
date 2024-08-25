from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
import datetime

class HomeworkManager: 
    
    MARGIN = 120
    GREEN = "#008000"
    RED = "#ff0000"
    WHITE = "#ffffff"
    BLACK = "#000000"

    def __init__(self, root):
        self.root = root
        self.root.title("Homework Manager")
        self.root.geometry("800x500")
        self.root.config(background = "#000000")
        self.root.resizable(False, False)

        self.mainframe = Frame(self.root)
        self.mainframe.pack(fill = BOTH, expand = 1)

        self.scroller = Scroller(self.mainframe)

        self.assignments = [["2024-08-22 19:00:00", "2024-08-26 22:30:00"], ["2024-08-20 19:00:00", "2024-08-26 23:30:00"], ["2024-01-01 00:00:00", "2025-01-01 00:00:00"], ["2024-08-20 19:00:00", "2024-08-26 23:30:00"], ["2024-08-20 19:00:00", "2024-08-26 23:30:00"], ["2024-08-20 19:00:00", "2024-08-26 23:30:00"]]
        self.tasks = [Task(self.mainframe, 0, ["code", "complete"]), Task(self.mainframe, 1, ["cry", "cry", "happy"]), Task(self.mainframe, 2, ["no", "yes", "no", "yes"]), Task(self.mainframe, 3, ["hi"]), Task(self.mainframe, 4, ["HELLO, BYE"]), Task(self.mainframe, 5, ["hello", "goodbye", "later"])]
        self.timebars, self.taskbars, self.percents, self.times, self.completions, self.buttons = [], [], [], [], [], []
        
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
            info = Frame(self.scroller.frame)
            info.pack()

            time = Frame(info)
            percent = Label(time, font=("Arial", 10), fg = self.RED, bg = self.BLACK)
            percent.pack(side = LEFT)
            timebar = Progressbar(time, orient = HORIZONTAL, length = 300, style = "red.Horizontal.TProgressbar")
            timebar.pack(side = LEFT)
            time.pack(side = TOP)

            work = Frame(info)
            completion = Label(work, font = ("Arial", 10), fg = self.GREEN, bg = self.BLACK)
            completion.pack(side = LEFT)
            taskbar = Progressbar(work, orient = HORIZONTAL, length = 300, style = "green.Horizontal.TProgressbar")
            taskbar.pack(side = LEFT)
            work.pack(side = TOP)

            time = Label(info, font = ("Arial", 10), fg = self.WHITE, bg = self.BLACK)
            time.pack(side = TOP)

            button = Button(info, font = ("Arial", 10, "bold"), text = "complete")
            button.pack(side = TOP)

            # self.tasks[i].tasklist.

            self.timebars.append(timebar)
            self.taskbars.append(taskbar)
            self.percents.append(percent)
            self.times.append(time)
            self.completions.append(completion)
            self.buttons.append(button)

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

            self.tasks[i].show()

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


class Task:
    def __init__(self, root, i, tasks):
        self.tasks = tasks
        self.current = 0
        self.hovered = False

        self.tasklist = Frame(root, bg = HomeworkManager.BLACK, width = 150, height = 100)
        self.tasklist.place(x = 400, y = HomeworkManager.MARGIN * i + 100)
        self.tasklist.pack_propagate(False)

        self.completed = Label(self.tasklist, font = ("Ink Free", 10, "bold"), fg = HomeworkManager.GREEN, bg = HomeworkManager.BLACK)
        self.inprogress = Label(self.tasklist, font = ("Ink Free", 10, "bold"), fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
        self.incompleted = Label(self.tasklist, font = ("Ink Free", 10, "bold"), fg = HomeworkManager.RED, bg = HomeworkManager.BLACK)
        
        self.completed.pack(side = TOP)
        self.inprogress.pack(side = TOP)
        self.incompleted.pack(side = TOP)

        self.tasklist.bind("<Enter>", lambda event: self.is_on_mouse(event, True))
        self.tasklist.bind("<Leave>", lambda event: self.is_on_mouse(event, False))
    
    def complete(self):
        if self.current < len(self.tasks):
            self.current += 1
    
    def show(self):
        if not self.hovered:
            self.completed.config(text = "")
            self.incompleted.config(text = "")
            if self.current < len(self.tasks):
                self.inprogress.config(text = f"Next Objective:\n{self.current+1}. {self.tasks[self.current]}")
            else:
                self.inprogress.config(text = "Complete!")
        else:
            incomplete_tasklist = str()
            inprogress_tasklist = str()
            complete_tasklist = str()
            for i in range(len(self.tasks)):
                if self.current < i:
                    incomplete_tasklist += f"{i+1}. {self.tasks[i]}"
                    if self.current - 1 != i:
                        incomplete_tasklist += "\n"
                elif self.current > i:
                    complete_tasklist += f"{i+1}. {self.tasks[i]}\n"
                else:
                    inprogress_tasklist += f"{i+1}. {self.tasks[i]}"
            self.completed.config(text = complete_tasklist.strip())
            self.incompleted.config(text = incomplete_tasklist.strip())
            self.inprogress.config(text = inprogress_tasklist.strip())
    
    def is_on_mouse(self, event, state):
        self.hovered = state

class Scroller:
    def __init__(self, mainframe):
        self.canvas = Canvas(mainframe, bg = HomeworkManager.BLACK)
        self.canvas.pack(side = LEFT, fill = BOTH, expand = TRUE)

        self.scrollbar = Scrollbar(mainframe, orient = VERTICAL, command = self.canvas.yview)
        self.scrollbar.pack(side = RIGHT, fill = Y)

        self.canvas.configure(yscrollcommand = self.scrollbar.set)
        self.canvas.bind("<Configure>", lambda event: self.canvas.configure(scrollregion = self.canvas.bbox("all")))

        self.frame = Frame(self.canvas, bg = HomeworkManager.WHITE, padx = 10, pady = 10)
        self.canvas.create_window((0,0), window = self.frame, anchor = NW)
        self.frame.bind_all("<MouseWheel>", self.is_on_mouse)
    
    def is_on_mouse(self, event):
        self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

root = Tk()
app = HomeworkManager(root)
root.mainloop()
