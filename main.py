from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
import datetime, math

class HomeworkManager: 
    
    MARGIN = 120
    GREEN = "#008000"
    RED = "#ff0000"
    WHITE = "#ffffff"
    BLACK = "#000000"

    def __init__(self, root):
        self.root = root
        self.root.title("Homework Manager")
        self.root.geometry("1000x500")
        self.root.config(background = "#000000")
        self.root.resizable(False, False)

        self.mainframe = Frame(self.root, width = 800, height = 500)
        self.mainframe.pack_propagate(False)
        self.mainframe.pack(fill = BOTH, expand = 1)

        self.scroller = Scroller(self.mainframe)

        self.assignments = [Assignment("2023-08-22 19:00:00", "2024-08-26 22:30:00", 0), Assignment("2024-08-24 19:00:00", "2024-08-26 23:30:00", 1), Assignment("2024-01-01 00:00:00", "2025-01-01 00:00:00", 2), Assignment("2024-08-20 19:00:00", "2024-08-26 23:30:00", 3), Assignment("2024-08-20 19:00:00", "2024-08-26 23:30:00", 4), Assignment("2024-08-20 19:00:00", "2024-08-26 23:30:00", 5)]
        self.tasks = [Task(["code", "complete"]), Task(["cry", "cry", "happy"]), Task(["no", "yes", "no", "yes"]), Task(["hi"]), Task(["HELLO, BYE"]), Task(["hello", "goodbye", "later"])]
        self.time_bars, self.task_bars, self.time_percents, self.task_percents, self.time_lefts, self.buttons = [], [], [], [], [], []

        self.setup()
    
    def setup(self):
        label = Label(self.scroller.frame, text = "Task Progress:", font=("Arial", 20, "bold"), fg = "#5c9bb7", bg = "#000000")
        label.pack(side = TOP)

        green_style = ttk.Style()
        green_style.theme_use("clam")
        green_style.configure("green.Horizontal.TProgressbar", foreground = self.GREEN, background = self.GREEN)

        red_style = ttk.Style()
        red_style.theme_use("clam")
        red_style.configure("red.Horizontal.TProgressbar", foreground = self.RED, background = self.RED)

        bars = Frame(self.scroller.frame, bg = HomeworkManager.BLACK)
        bars.pack(side = LEFT)

        for i in range(len(self.assignments)):
            unit = Frame(bars, bg = HomeworkManager.BLACK, bd = 5, relief = SUNKEN)
            unit.pack(side = TOP)

            info = Frame(unit, bg = HomeworkManager.BLACK)
            info.pack(side = LEFT)

            time_info = Frame(info, bg = HomeworkManager.BLACK, width = 400, height = 40)
            time_info.pack_propagate(False)
            time_info.pack(side = TOP)

            time_percent = Label(time_info, font=("Arial", 10), fg = self.RED, bg = self.BLACK, width = 5, padx = 5, pady = 0)
            time_percent.pack(side = LEFT)
            time_bar = Progressbar(time_info, orient = HORIZONTAL, length = 300, style = "red.Horizontal.TProgressbar")
            time_bar.pack(side = LEFT)

            task_info = Frame(info, bg = HomeworkManager.BLACK, width = 400, height = 40)
            task_info.pack_propagate(False)
            task_info.pack(side = TOP)
            
            task_percent = Label(task_info, font = ("Arial", 10), fg = self.GREEN, bg = self.BLACK, width = 5, padx = 5, pady = 0)
            task_percent.pack(side = LEFT)
            task_bar = Progressbar(task_info, orient = HORIZONTAL, length = 300, style = "green.Horizontal.TProgressbar")
            task_bar.pack(side = LEFT)

            time_left = Label(info, font = ("Arial", 10), fg = self.WHITE, bg = self.BLACK)
            time_left.pack(side = TOP, pady = 10)

            button = Button(info, font = ("Arial", 10, "bold"), text = "complete")
            button.pack(side = TOP, pady = 10)

            self.tasks[i].place(unit)

            self.time_bars.append(time_bar)
            self.task_bars.append(task_bar)
            self.time_percents.append(time_percent)
            self.task_percents.append(task_percent)
            self.time_lefts.append(time_left)
            self.buttons.append(button)

        settings = Frame(self.scroller.frame, bg = HomeworkManager.WHITE)
        settings.pack(side = TOP)

        sort_time = Button(settings, font = ("Arial", 10, "bold"), text = "Time", command = lambda: self.reorder(1))
        sort_time.pack(side = TOP)

        for i in range(len(self.assignments)):
            self.update(self.assignments[i].pos)

    def update(self, i):
        if self.time_bars[i]["value"] < 100 and self.task_bars[i]:
            passed = int((datetime.datetime.now()-self.assignments[i].start).total_seconds())
            interval = (self.assignments[i].end - self.assignments[i].start).total_seconds()
            passed_percent = int((passed / interval) * 100)

            self.time_bars[i]["value"] = passed_percent
            self.task_bars[i]["value"] = ((self.tasks[i].current) / len(self.tasks[i].tasks)) * 100
            
            self.time_percents[i].config(text = f"{passed_percent}%")
            self.task_percents[i].config(text = f"{int(((self.tasks[i].current) / len(self.tasks[i].tasks)) * 100)}%")

            self.time_lefts[i].config(fg = f"#ff{hex(int(255 - math.pow(1.05, passed_percent)))[2:]}{hex(int(255 - math.pow(1.05, passed_percent)))[2:]}")
            self.time_lefts[i].config(text = self.seconds_to_string(interval-passed) + " left")

            self.buttons[i].config(command = lambda: self.tasks[i].complete())

            self.tasks[i].show()

            self.root.update_idletasks()
            self.root.after(100, self.update, self.assignments[i].pos)
        
    def reorder(self, n):
        a = self.assignments.copy()
        if n == 1:
            checked = []
            for x in range(len(a)):
                min = -1
                for i in range(len(a)):
                    if ((a[i].end-a[i].start).total_seconds() - int((datetime.datetime.now()-a[i].start).total_seconds()) < min or min == -1) and i not in checked:
                        min = (a[i].end-a[i].start).total_seconds() - int((datetime.datetime.now()-a[i].start).total_seconds())
                        index = i
                self.assignments[index].pos = x
                checked.append(index)

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

class Assignment:
    def __init__(self, start, end, pos):
        self.start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        self.end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        self.pos = pos


class Task:
    def __init__(self, tasks):
        self.tasks = tasks
        self.current = 0
        self.hovered = False

    def place(self, frame):
        self.tasklist = Frame(frame, bg = HomeworkManager.BLACK, width = 150, height = 100)
        self.tasklist.pack_propagate(False)

        self.completed = Label(self.tasklist, font = ("Ink Free", 10, "bold"), fg = HomeworkManager.GREEN, bg = HomeworkManager.BLACK)
        self.inprogress = Label(self.tasklist, font = ("Ink Free", 10, "bold"), fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
        self.incompleted = Label(self.tasklist, font = ("Ink Free", 10, "bold"), fg = HomeworkManager.RED, bg = HomeworkManager.BLACK)
        
        self.completed.pack(side = TOP)
        self.inprogress.pack(side = TOP)
        self.incompleted.pack(side = TOP)

        self.tasklist.bind("<Enter>", lambda event: self.is_on_mouse(event, True))
        self.tasklist.bind("<Leave>", lambda event: self.is_on_mouse(event, False))

        self.tasklist.pack(side = RIGHT)
    
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

        self.frame = Frame(self.canvas, bg = HomeworkManager.BLACK, padx = 10, pady = 10)
        self.canvas.create_window((0,0), window = self.frame, anchor = NW)
        self.frame.bind_all("<MouseWheel>", self.is_on_mouse)
    
    def is_on_mouse(self, event):
        self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

root = Tk()
app = HomeworkManager(root)
root.mainloop()