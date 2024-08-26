from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Progressbar
import datetime, math

class HomeworkManager: 
    
    MARGIN = 120
    GREEN = "#008000"
    RED = "#ff0000"
    WHITE = "#ffffff"
    BLACK = "#000000"

    scrolling = False
    updating = False

    def __init__(self, root):
        self.root = root
        self.root.title("Homework Manager")
        self.root.geometry("1000x500")
        self.root.config(background = "#000000")
        self.root.resizable(False, False)

        self.mainframe = Frame(self.root, width = 800, height = 500)
        self.mainframe.pack_propagate(False)
        self.mainframe.pack(fill = BOTH, expand = 1)

        self.green_style = ttk.Style()
        self.green_style.theme_use("clam")
        self.green_style.configure("green.Horizontal.TProgressbar", foreground = HomeworkManager.GREEN, background = HomeworkManager.GREEN)

        self.red_style = ttk.Style()
        self.red_style.theme_use("clam")
        self.red_style.configure("red.Horizontal.TProgressbar", foreground = HomeworkManager.RED, background = HomeworkManager.RED)

        self.scroller = Scroller(self.mainframe)

        self.assignments, self.tasks = [], []
        self.time_bars, self.task_bars, self.time_percents, self.task_percents, self.time_lefts, self.buttons = [], [], [], [], [], []

        self.setup()
    
    def setup(self):
        label = Label(self.scroller.frame, text = "Task Progress:", font=("Arial", 20, "bold"), fg = "#5c9bb7", bg = "#000000")
        label.pack(side = TOP)

        bars = Frame(self.scroller.frame, bg = HomeworkManager.BLACK)
        bars.pack(side = LEFT)

        for i in range(len(self.assignments)):
            unit = Frame(bars, bg = HomeworkManager.BLACK, bd = 5, relief = SUNKEN)
            unit.pack(side = TOP, pady = 10)

            header = Frame(unit, bg = HomeworkManager.BLACK, width = 500, height = 50)
            header.pack_propagate(False)
            header.pack(side = TOP)

            topic = Label(header, font = ("Arial", 10, "bold"), text = self.assignments[i].topic, fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
            topic.pack(side = TOP)
            title = Label(header, font = ("Arial", 10), text = self.assignments[i].title, fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
            title.pack(side = TOP)

            info = Frame(unit, bg = HomeworkManager.BLACK)
            info.pack(side = LEFT)

            time_info = Frame(info, bg = HomeworkManager.BLACK, width = 400, height = 40)
            time_info.pack_propagate(False)
            time_info.pack(side = TOP)

            time_percent = Label(time_info, font = ("Arial", 10), fg = HomeworkManager.RED, bg = HomeworkManager.BLACK, width = 5, padx = 5, pady = 0)
            time_percent.pack(side = LEFT)
            time_bar = Progressbar(time_info, orient = HORIZONTAL, length = 300, style = "red.Horizontal.TProgressbar")
            time_bar.pack(side = LEFT)

            task_info = Frame(info, bg = HomeworkManager.BLACK, width = 400, height = 40)
            task_info.pack_propagate(False)
            task_info.pack(side = TOP)
            
            task_percent = Label(task_info, font = ("Arial", 10), fg = HomeworkManager.GREEN, bg = HomeworkManager.BLACK, width = 5, padx = 5, pady = 0)
            task_percent.pack(side = LEFT)
            task_bar = Progressbar(task_info, orient = HORIZONTAL, length = 300, style = "green.Horizontal.TProgressbar")
            task_bar.pack(side = LEFT)

            time_left = Label(info, font = ("Arial", 10), fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
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

        settings = Frame(self.scroller.frame, bg = HomeworkManager.BLACK, width = 200, height = 500)
        settings.pack_propagate(False)
        settings.pack(side = TOP)

        sort_label = Label(settings, font = ("Arial", 10, "bold"), text = "Sort by", fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
        sort_label.pack(side = TOP, pady = 10)

        sort_time = Button(settings, font = ("Arial", 10, "bold"), text = "Time", command = lambda: self.reorder("time"))
        sort_time.pack(side = TOP)

        sort_time_percent = Button(settings, font = ("Arial", 10, "bold"), text = "Time%", command = lambda: self.reorder("time%"))
        sort_time_percent.pack(side = TOP)

        sort_progress = Button(settings, font = ("Arial", 10, "bold"), text = "Progress", command = lambda: self.reorder("progress"))
        sort_progress.pack(side = TOP)

        sort_topic = Button(settings, font = ("Arial", 10, "bold"), text = "Topic", command = lambda: self.reorder("topic"))
        sort_topic.pack(side = TOP)

        add_label = Label(settings, font = ("Arial", 10, "bold"), text = "Add an assignment", fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
        add_label.pack(side = TOP)
        add = Button(settings, font = ("Arial", 10, "bold"), text = "Add assignment", command = lambda: self.create_window())
        add.pack(side = TOP)

        self.start_updating()

    def start_updating(self):
        HomeworkManager.updating = True
        self.update_widgets()

    def stop_updating(self):
        HomeworkManager.updating = False

    def update_widgets(self):
        for i in range(len(self.assignments)):
            self.update(i)
        if HomeworkManager.updating:
            self.root.after(200, self.update_widgets)

    def update(self, i):
        if self.time_bars[i]["value"] < 100 and self.task_bars[i] and not HomeworkManager.scrolling:
            passed = int((datetime.datetime.now()-self.assignments[i].start).total_seconds())
            interval = (self.assignments[i].end - self.assignments[i].start).total_seconds()
            passed_percent = int((passed / interval) * 100)
            self.time_percents[i].config(text = f"{passed_percent}%")
            self.task_percents[i].config(text = f"{int(((self.tasks[i].current) / len(self.tasks[i].tasks)) * 100)}%")

            self.time_lefts[i].config(fg = f"#ff{hex(int(255 - math.pow(1.05, passed_percent)))[2:]}{hex(int(255 - math.pow(1.05, passed_percent)))[2:]}")
            self.time_lefts[i].config(text = self.seconds_to_string(interval-passed) + " left")
            self.buttons[i].config(command = lambda: self.tasks[i].complete())

            self.time_bars[i]["value"] = passed_percent
            self.task_bars[i]["value"] = ((self.tasks[i].current) / len(self.tasks[i].tasks)) * 100

            self.tasks[i].show()

            self.root.update_idletasks()
    
    def reorder(self, order):
        self.stop_updating()
        if order == "time":
            now = datetime.datetime.now()
            sorted_data = sorted(zip(self.assignments, self.tasks), key = lambda a : (a[0].end - now).total_seconds())
        elif order == "time%":
            now = datetime.datetime.now()
            sorted_data = sorted(zip(self.assignments, self.tasks), key = lambda a : (a[0].end - now).total_seconds() / (a[0].end - a[0].start).total_seconds())
        elif order == "progress":
            sorted_data = sorted(zip(self.assignments, self.tasks), key = lambda a : (a[1].current / len(a[1].tasks)))
        elif order == "topic":
            sorted_data = sorted(zip(self.assignments, self.tasks), key = lambda a : (a[0].topic))
        
        self.assignments, self.tasks = map(list, zip(*sorted_data))

        self.clear_widgets()
        self.setup()

    def clear_widgets(self):
        for widget in self.scroller.frame.winfo_children():
            widget.destroy()
        self.time_bars.clear()
        self.task_bars.clear()
        self.time_percents.clear()
        self.task_percents.clear()
        self.time_lefts.clear()
        self.buttons.clear()

    def create_window(self):
        self.new_window = UserInput(self, "Create an Assignment")

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
    def __init__(self, start, end, title, topic):
        self.start = datetime.datetime.strptime(start, "%Y/%m/%d %H:%M:%S")
        self.end = datetime.datetime.strptime(end, "%Y/%m/%d %H:%M:%S")

        self.title = title
        self.topic = topic


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

class UserInput():
    def __init__(self, root, name):
        self.window = Toplevel()
        self.window.title(name)
        self.window.geometry("200x400")
        self.window.config(background = HomeworkManager.BLACK)
        self.window.resizable(False, False)

        self.questions = ["Title", "Topic", "Start Time", "End Time", "Tasks"]
        # 2024-08-20 19:19:19

        self.entries = []

        for i in range(len(self.questions)):
            self.frame = Frame(self.window, bg = HomeworkManager.BLACK, width = 200, height = 50)
            self.frame.pack_propagate(False)
            self.frame.pack(side = TOP)

            self.label = Label(self.frame, font = ("Ink Free", 10, "bold"), text = self.questions[i], fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
            self.label.pack(side = TOP)

            self.entry = Entry(self.frame, font = ("Arial", 10), fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
            self.entry.pack(side = TOP)
            self.entries.append(self.entry)

        self.submit = Button(self.window, text = "Submit", command = lambda: self.update(root))
        self.submit.pack(side = TOP)

        self.reset = Button(self.window, text = "Reset", command = lambda: self.clear())
        self.reset.pack(side = TOP)

    def update(self, root):
        title, topic, start, end = self.entries[0].get().strip(), self.entries[1].get().strip(), self.entries[2].get().strip(), self.entries[3].get().strip()
        
        if len(start) == 10:
            start += " 23:59:59"
        if len(end) == 10:
            end += " 23:59:59"
            
        try:
            starttime = datetime.datetime.strptime(start, "%Y/%m/%d %H:%M:%S")
            endtime = datetime.datetime.strptime(end, "%Y/%m/%d %H:%M:%S")
        except:
            messagebox.showwarning(title = "Formatting Error", message = "Please enter times in the format YYYY/MM/DD HH-MM-SS")
        else:
            now = datetime.datetime.now()
            if (now - starttime).total_seconds() < 0:
                messagebox.showwarning(title = "Time Error", message = "Please ensure start time is before current time")
            elif (endtime - now).total_seconds() < 0:
                messagebox.showwarning(title = "Time Error", message = "Please ensure end time is after current time")
            else:
                tasks = self.entries[4].get().split(",")
                for i in range(len(tasks)):
                    tasks[i].strip()

                root.stop_updating()
                root.assignments.append(Assignment(start, end, title, topic))
                root.tasks.append(Task(tasks))

                root.clear_widgets()
                root.setup()
                root.scroller.canvas.configure(scrollregion=root.scroller.canvas.bbox("all"))
                self.window.destroy()
        
    def clear(self):
        for i in range(len(self.entries)):
            self.entries[i].delete(0, END)


# some code taken from https://www.youtube.com/watch?v=0WafQCaok6g
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
        self.canvas.bind("<MouseWheel>", self.scrolling)
        self.canvas.bind("<ButtonRelease-1>", self.stop_scrolling)

        self.is_scrolling = False

    def scrolling(self, event):
        if not self.is_scrolling:
            HomeworkManager.scrolling = True
        self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
        self.is_scrolling = True
    
    def stop_scrolling(self, event):
        HomeworkManager.scrolling = False
        self.is_scrolling = False
        
root = Tk()
app = HomeworkManager(root)
root.mainloop()
