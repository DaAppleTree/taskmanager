from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Progressbar
import datetime, math, os

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
        self.root.geometry("900x600")
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
        self.time_bars, self.task_bars, self.time_percents, self.task_percents, self.time_lefts = [], [], [], [], []
        self.next_buttons, self.back_buttons, self.end_buttons = [], [], []

        # line of code taken from https://github.com/DaAppleTree/taskmanager/commit/fdd118ffdb49dad07c4627ef62bcc04dd2129c37
        os.chdir(os.path.dirname(os.path.realpath(__file__)))

        with open("assignments.txt", "r") as f:
            lines = f.readlines()

        for i in range(0, len(lines), 3):
            line = lines[i].split()
            self.assignments.append(Assignment(f"{line[2]} {line[3]}", f"{line[4]} {line[5]}", line[0], line[1], i))
            self.tasks.append(Task(lines[i+1].split(","), int(lines[i+2]), i))

        self.setup()
    
    def setup(self):
        label = Label(self.scroller.frame, text = "Homework Manager", font=("Constantia", 30, "bold"), fg = "#5c9bb7", bg = "#000000")
        label.pack(side = TOP)

        bars = Frame(self.scroller.frame, bg = HomeworkManager.BLACK)
        bars.pack(side = LEFT)

        for i in range(len(self.assignments)):
            unit = Frame(bars, bg = HomeworkManager.BLACK, bd = 5, relief = RAISED, width = 600, height = 300)
            unit.pack_propagate(False)
            unit.pack(side = TOP, pady = 10, padx = 15)

            header = Frame(unit, bg = HomeworkManager.BLACK)
            header.pack(side = TOP)

            topic = Label(header, font = ("Constantia", 20, "bold"), text = self.assignments[i].topic, fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
            topic.pack(side = TOP)
            title = Label(header, font = ("Constantia", 15), text = self.assignments[i].title, fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
            title.pack(side = TOP)

            info = Frame(unit, bg = HomeworkManager.BLACK)
            info.pack(side = LEFT)

            time_info = Frame(info, bg = HomeworkManager.BLACK, width = 400, height = 40)
            time_info.pack_propagate(False)
            time_info.pack(side = TOP)

            time_percent = Label(time_info, font = ("Constantia", 15), fg = HomeworkManager.RED, bg = HomeworkManager.BLACK, width = 5, padx = 5, pady = 0)
            time_percent.pack(side = LEFT)
            time_bar = Progressbar(time_info, orient = HORIZONTAL, length = 300, style = "red.Horizontal.TProgressbar")
            time_bar.pack(side = LEFT)

            task_info = Frame(info, bg = HomeworkManager.BLACK, width = 400, height = 40)
            task_info.pack_propagate(False)
            task_info.pack(side = TOP)
            
            task_percent = Label(task_info, font = ("Constantia", 15), fg = HomeworkManager.GREEN, bg = HomeworkManager.BLACK, width = 5, padx = 5, pady = 0)
            task_percent.pack(side = LEFT)
            task_bar = Progressbar(task_info, orient = HORIZONTAL, length = 300, style = "green.Horizontal.TProgressbar")
            task_bar.pack(side = LEFT)

            time_left = Label(info, font = ("Constantia", 15), fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
            time_left.pack(side = TOP, pady = 10)

            button_info = Frame(info, bg = HomeworkManager.BLACK, width = 300, height = 50)
            button_info.pack_propagate(False)
            button_info.pack(side = TOP, pady = 10)

            next_button = Button(button_info, font = ("Constantia", 10, "bold"), text = "complete")
            next_button.pack(side = LEFT, padx = 10)

            back_button = Button(button_info, font = ("Constantia", 10, "bold"), text = "back")
            back_button.pack(side = LEFT, padx = 10)

            end_button = Button(button_info, font = ("Constantia", 10, "bold"), text = "end")
            end_button.pack(side = LEFT, padx = 10)

            self.tasks[i].place(unit)

            self.time_bars.append(time_bar)
            self.task_bars.append(task_bar)
            self.time_percents.append(time_percent)
            self.task_percents.append(task_percent)
            self.time_lefts.append(time_left)
            self.next_buttons.append(next_button)
            self.back_buttons.append(back_button)
            self.end_buttons.append(end_button)

        settings = Frame(self.scroller.frame, bg = HomeworkManager.BLACK, bd = 5, relief = RAISED, width = 200, height = 400)
        settings.pack_propagate(False)
        settings.pack(side = TOP, padx = 15)

        add_label = Label(settings, font = ("Constantia", 15, "bold"), text = "Add", fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
        add_label.pack(side = TOP, pady = 10)
        add = Button(settings, font = ("Constantia", 10, "bold"), text = "Add assignment", command = lambda: self.create_window())
        add.pack(side = TOP, pady = 10)

        sort_label = Label(settings, font = ("Constantia", 15, "bold"), text = "Sort by", fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
        sort_label.pack(side = TOP, pady = 10)

        sort_time = Button(settings, font = ("Constantia", 10, "bold"), text = "Time", command = lambda: self.reorder("time"))
        sort_time.pack(side = TOP, pady = 10)

        sort_time_percent = Button(settings, font = ("Constantia", 10, "bold"), text = "Time%", command = lambda: self.reorder("time%"))
        sort_time_percent.pack(side = TOP, pady = 10)

        sort_progress = Button(settings, font = ("Constantia", 10, "bold"), text = "Progress", command = lambda: self.reorder("progress"))
        sort_progress.pack(side = TOP, pady = 10)

        sort_topic = Button(settings, font = ("Constantia", 10, "bold"), text = "Topic", command = lambda: self.reorder("topic"))
        sort_topic.pack(side = TOP, pady = 10)

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
        if not HomeworkManager.scrolling:
            passed = int((datetime.datetime.now()-self.assignments[i].start).total_seconds())
            interval = (self.assignments[i].end - self.assignments[i].start).total_seconds()
            passed_percent = int((passed / interval) * 100)

            self.time_bars[i]["value"] = passed_percent
            self.task_bars[i]["value"] = ((self.tasks[i].current) / len(self.tasks[i].tasks)) * 100

            self.next_buttons[i].config(command = lambda: self.tasks[i].complete())
            self.back_buttons[i].config(command = lambda: self.tasks[i].back())
            self.end_buttons[i].config(command = lambda: self.end(i))

            self.time_percents[i].config(text = f"{passed_percent}%")
            self.task_percents[i].config(text = f"{int(((self.tasks[i].current) / len(self.tasks[i].tasks)) * 100)}%")

            self.time_lefts[i].config(fg = f"#ff{hex(int(255 - math.pow(1.05, passed_percent)))[2:]}{hex(int(255 - math.pow(1.05, passed_percent)))[2:]}")
            self.time_lefts[i].config(text = self.seconds_to_string(interval-passed) + " left")

            self.tasks[i].show()

            if self.time_bars[i]["value"] < 100 and self.task_bars[i]["value"] < 100:
                self.end_buttons[i].pack_forget()

            elif self.task_bars[i]["value"] == 100:
                self.end_buttons[i].pack(side = LEFT, padx = 10)
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
        self.next_buttons.clear()
        self.back_buttons.clear()
        self.end_buttons.clear()

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
    
    def end(self, index):
        self.stop_updating()

        with open("assignments.txt", "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for i in range(len(lines)):
                if self.assignments[index].id != i // 3:
                    f.write(lines[i])
            f.truncate()

        self.assignments.pop(index)
        self.tasks.pop(index)

        self.clear_widgets()
        self.setup()


class Assignment:
    def __init__(self, start, end, title, topic, id):
        self.start = datetime.datetime.strptime(start, "%Y/%m/%d %H:%M:%S")
        self.end = datetime.datetime.strptime(end, "%Y/%m/%d %H:%M:%S")

        self.title = title
        self.topic = topic
        self.id = id


class Task:
    def __init__(self, tasks, current, id):
        self.tasks = tasks
        self.current = current
        self.hovered = False
        self.id = id

    def place(self, frame):
        self.tasklist = Frame(frame, bg = HomeworkManager.BLACK, width = 300, height = 300)
        self.tasklist.pack_propagate(False)

        self.completed = Label(self.tasklist, font = ("Ink Free", 12, "bold"), fg = HomeworkManager.GREEN, bg = HomeworkManager.BLACK)
        self.inprogress = Label(self.tasklist, font = ("Ink Free", 12, "bold"), fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
        self.incompleted = Label(self.tasklist, font = ("Ink Free", 12, "bold"), fg = HomeworkManager.RED, bg = HomeworkManager.BLACK)
        
        self.completed.pack(side = TOP)
        self.inprogress.pack(side = TOP)
        self.incompleted.pack(side = TOP)

        self.tasklist.bind("<Enter>", lambda event: self.is_on_mouse(event, True))
        self.tasklist.bind("<Leave>", lambda event: self.is_on_mouse(event, False))

        self.tasklist.pack(side = RIGHT)
    
    def complete(self):
        if self.current < len(self.tasks):
            self.current += 1
        self.update_file()

    def back(self):
        if self.current > 0:
            self.current -= 1
        self.update_file()

    def update_file(self):
        with open("assignments.txt", "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for i in range(len(lines)):
                if i - 2 != self.id:
                    f.write(lines[i])
                else:
                    f.write(f"{self.current}")
            f.truncate()
    
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
        self.window.geometry("200x450")
        self.window.config(background = HomeworkManager.BLACK)
        self.window.resizable(False, False)

        self.questions = ["Title", "Topic", "Start Time", "End Time", "Tasks"]
        # 2024-08-20 19:19:19

        self.entries = []

        for i in range(len(self.questions)):
            self.frame = Frame(self.window, bg = HomeworkManager.BLACK, width = 200, height = 70)
            self.frame.pack_propagate(False)
            self.frame.pack(side = TOP)

            self.label = Label(self.frame, font = ("Constantia", 10, "bold"), text = self.questions[i], fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
            self.label.pack(side = TOP, pady = 5)

            self.entry = Entry(self.frame, font = ("Ink Free", 10), fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
            self.entry.pack(side = TOP, pady = 5)
            self.entries.append(self.entry)

        self.submit = Button(self.window, font = ("Constantia", 10, "bold"), text = "Submit", command = lambda: self.update(root))
        self.submit.pack(side = TOP, pady = 10)

        self.reset = Button(self.window, font = ("Constantia", 10, "bold"), text = "Reset", command = lambda: self.clear())
        self.reset.pack(side = TOP, pady = 10)

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
                root.assignments.append(Assignment(start, end, title, topic, len(root.assignments)))
                root.tasks.append(Task(tasks, 0, len(root.tasks)))

                with open('assignments.txt', "a") as f:
                    f.write(f"{title} {topic} {start} {end}\n")
                    for i in range(len(tasks)):
                        if i != len(tasks) - 1:
                            f.write(f"{tasks[i]}, ")
                        else:
                            f.write(f"{tasks[i]}")
                    f.write("\n0\n")

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
