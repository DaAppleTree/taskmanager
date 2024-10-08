"""
homeworkmanager.py - a homework managing application with real time progress
"""

# import all necessary modules
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Progressbar
import datetime, math, os, calendar

# main class for the main window
class HomeworkManager: 

    # constants
    MARGIN = 120
    GREEN = "#008000"
    RED = "#ff0000"
    WHITE = "#ffffff"
    BLACK = "#000000"
    SECTION = 3

    scrolling = False
    updating = False

    def __init__(self, root):

        # window setup
        self.root = root
        self.root.title("Homework Manager")
        self.root.geometry("1000x600")
        self.root.config(background = "#000000")
        self.root.resizable(False, False)
        
        # mainframe setup
        self.mainframe = Frame(self.root, width = 800, height = 500)
        self.mainframe.pack_propagate(False)
        self.mainframe.pack(fill = BOTH, expand = 1)

        # progressbar styles declaration
        self.green_style = ttk.Style()
        self.green_style.theme_use("clam")
        self.green_style.configure("green.Horizontal.TProgressbar", foreground = HomeworkManager.GREEN, background = HomeworkManager.GREEN)

        self.red_style = ttk.Style()
        self.red_style.theme_use("clam")
        self.red_style.configure("red.Horizontal.TProgressbar", foreground = HomeworkManager.RED, background = HomeworkManager.RED)

        # scroller setup
        self.scroller = Scroller(self.mainframe)

        # widget list declaration
        self.assignments, self.tasks = [], []
        self.time_bars, self.task_bars, self.time_percents, self.task_percents, self.time_lefts = [], [], [], [], []
        self.next_buttons, self.back_buttons, self.end_buttons = [], [], []

        # opens file to read assignments and tasks
        os.chdir(os.path.dirname(os.path.realpath(__file__))) # line of code taken from https://stackoverflow.com/questions/509742/change-directory-to-the-directory-of-a-python-script

        with open("assignments.txt", "r") as f:
            lines = f.readlines()
            if len(lines) > HomeworkManager.SECTION - 1:
                for i in range(0, len(lines), HomeworkManager.SECTION):
                    line = lines[i].split()
                    self.assignments.append(Assignment(f"{line[2]} {line[3]}", f"{line[4]} {line[5]}", line[0], line[1], i//HomeworkManager.SECTION))
                    self.tasks.append(Task(lines[i+1].split(","), int(lines[i+2]), i//HomeworkManager.SECTION))

        # set up all widgets
        self.setup()
    
    def setup(self):

        # set up title label
        label = Label(self.scroller.frame, text = "Homework Manager", font=("Constantia", 30, "bold"), fg = "#5c9bb7", bg = "#000000")
        label.pack(side = TOP)

        # set up frame for all progress bars
        units = Frame(self.scroller.frame, bg = HomeworkManager.BLACK)
        units.pack(side = LEFT)

        # create units for all assignments
        for i in range(len(self.assignments)):

            # set up frame for one progress bar
            unit = Frame(units, bg = HomeworkManager.BLACK, bd = 5, relief = RAISED, width = 600, height = 300)
            unit.pack_propagate(False)
            unit.pack(side = TOP, pady = 10, padx = 15)

            # set up frame for header
            header = Frame(unit, bg = HomeworkManager.BLACK)
            header.pack(side = TOP)

            # set up labels for topic and title
            topic = Label(header, font = ("Constantia", 20, "bold"), text = self.assignments[i].topic, fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
            topic.pack(side = TOP)
            title = Label(header, font = ("Constantia", 15), text = self.assignments[i].title, fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
            title.pack(side = TOP)

            # set up frames, labels, and progressbars
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

            # set up time left label
            time_left = Label(info, font = ("Constantia", 15), fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
            time_left.pack(side = TOP, pady = 10)

            # set up frames and buttons
            button_info = Frame(info, bg = HomeworkManager.BLACK, width = 300, height = 50)
            button_info.pack_propagate(False)
            button_info.pack(side = TOP, pady = 10)

            next_button = Button(button_info, font = ("Constantia", 10, "bold"), text = "complete")
            next_button.pack(side = LEFT, padx = 10)

            back_button = Button(button_info, font = ("Constantia", 10, "bold"), text = "back")
            back_button.pack(side = LEFT, padx = 10)

            end_button = Button(button_info, font = ("Constantia", 10, "bold"), text = "end")
            end_button.pack(side = LEFT, padx = 10)

            # set up widgets for the tasklist
            self.tasks[i].place(unit)
            
            # add widgets to lists
            self.time_bars.append(time_bar)
            self.task_bars.append(task_bar)
            self.time_percents.append(time_percent)
            self.task_percents.append(task_percent)
            self.time_lefts.append(time_left)
            self.next_buttons.append(next_button)
            self.back_buttons.append(back_button)
            self.end_buttons.append(end_button)

        # set up settings frame and add settings button
        settings = Frame(self.scroller.frame, bg = HomeworkManager.BLACK, bd = 5, relief = RAISED, width = 300, height = 400)
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

        # set up calendar frame and add calendar widget
        calendar_frame = Frame(self.scroller.frame, bg = HomeworkManager.BLACK, bd = 5, relief = RAISED, width = 300, height = 400)
        calendar_frame.pack_propagate(False)
        calendar_frame.pack(side = TOP, padx = 15)

        self.calendar = Calendar(calendar_frame, "24", "08", self)
        calendar_frame.pack()

        # start updating widgets
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
            # update passed and interval
            passed = int((datetime.datetime.now()-self.assignments[i].start).total_seconds())
            interval = (self.assignments[i].end - self.assignments[i].start).total_seconds()
            passed_percent = int((passed / interval) * 100)

            # update progressbars
            self.time_bars[i]["value"] = passed_percent
            self.task_bars[i]["value"] = ((self.tasks[i].current) / len(self.tasks[i].tasks)) * 100

            # update button commands
            self.next_buttons[i].config(command = lambda: self.tasks[i].complete())
            self.back_buttons[i].config(command = lambda: self.tasks[i].back())
            self.end_buttons[i].config(command = lambda: self.end(i))

            # update labels
            self.time_percents[i].config(text = f"{passed_percent}%")
            self.task_percents[i].config(text = f"{int(((self.tasks[i].current) / len(self.tasks[i].tasks)) * 100)}%")
            self.time_lefts[i].config(fg = f"#ff{hex(int(255 - math.pow(1.05, passed_percent)))[2:]}{hex(int(255 - math.pow(1.05, passed_percent)))[2:]}")
            self.time_lefts[i].config(text = self.seconds_to_string(interval-passed) + " left")

            # update tasklists
            self.tasks[i].show()

            # show or hide end buttons accordingly
            if self.time_bars[i]["value"] < 100 and self.task_bars[i]["value"] < 100:
                self.end_buttons[i].pack_forget()
            elif self.task_bars[i]["value"] == 100:
                self.end_buttons[i].pack(side = LEFT, padx = 10)

        # update window
        self.root.update_idletasks()
    
    def reorder(self, order):
        self.stop_updating()

        # reorder assignments and tasks accordingly
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
        
        # create new IDs and update text file
        self.assignments, self.tasks = map(list, zip(*sorted_data))
        for i in range(len(self.assignments)):
            self.assignments[i].id = i
            self.tasks[i].id = i
        
        with open('assignments.txt', "w") as f:
            f.seek(0)
            for i in range(len(self.assignments)):
                f.write(f"{self.assignments[i].title.strip()} {self.assignments[i].topic.strip()} {self.assignments[i].start_string().strip()} {self.assignments[i].end_string().strip()}\n")
                for j in range(len(self.tasks[i].tasks)):
                    if j != len(self.tasks[i].tasks) - 1:
                        f.write(f"{self.tasks[i].tasks[j].strip()}, ")
                    else:
                        f.write(f"{self.tasks[i].tasks[j].strip()}")
                f.write(f"\n{self.tasks[i].current}\n")

        # reset frames
        self.clear_widgets()
        self.setup()

    def clear_widgets(self):
        # destory all widgets and clear all lists
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
        # converts seconds into proper time notation
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
        # removes assignments and tasks from lists and text file
        self.stop_updating()

        with open("assignments.txt", "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for i in range(len(lines)):
                if self.assignments[index].id * HomeworkManager.SECTION != i // HomeworkManager.SECTION:
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
    
    # returns datetime information in string format
    def start_string(self):
        return self.start.strftime("%Y/%m/%d %H:%M:%S")
    
    def end_string(self):
        return self.end.strftime("%Y/%m/%d %H:%M:%S")
    
    def end_date(self):
        return self.end.strftime("%Y/%m/%d")
    
    def end_time(self):
        return self.end.strftime("%H:%M:%S")


class Task:
    def __init__(self, tasks, current, id):
        self.tasks = tasks
        self.current = current
        self.hovered = False
        self.id = id

    def place(self, frame):
        # set up frame for tasks and labels
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
    
    # increase and decrease current task
    def complete(self):
        if self.current < len(self.tasks):
            self.current += 1
        self.update_file()

    def back(self):
        if self.current > 0:
            self.current -= 1
        self.update_file()

    # updates text file every time current task changes
    def update_file(self):
        with open("assignments.txt", "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for i in range(len(lines)):
                if i - (HomeworkManager.SECTION - 1) != self.id * HomeworkManager.SECTION:
                    f.write(lines[i])
                else:
                    f.write(f"{self.current}\n")
            f.truncate()
    
    # fromats the text on the tasklist
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
    
    # detects if mouse is hovering
    def is_on_mouse(self, event, state):
        self.hovered = state

class UserInput():
    def __init__(self, root, name):

        # new window for user input
        self.window = Toplevel()
        self.window.title(name)
        self.window.geometry("200x450")
        self.window.config(background = HomeworkManager.BLACK)
        self.window.resizable(False, False)

        self.questions = ["Title", "Topic", "Start Time", "End Time", "Tasks"]

        self.entries = []

        # set up labels and entries for all questions
        for i in range(len(self.questions)):
            self.frame = Frame(self.window, bg = HomeworkManager.BLACK, width = 200, height = 70)
            self.frame.pack_propagate(False)
            self.frame.pack(side = TOP)

            self.label = Label(self.frame, font = ("Constantia", 10, "bold"), text = self.questions[i], fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
            self.label.pack(side = TOP, pady = 5)

            self.entry = Entry(self.frame, font = ("Ink Free", 10), fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
            self.entry.pack(side = TOP, pady = 5)
            self.entries.append(self.entry)
            
        # set up two buttons for submitting and resetting
        self.submit = Button(self.window, font = ("Constantia", 10, "bold"), text = "Submit", command = lambda: self.update(root))
        self.submit.pack(side = TOP, pady = 10)

        self.reset = Button(self.window, font = ("Constantia", 10, "bold"), text = "Reset", command = lambda: self.clear())
        self.reset.pack(side = TOP, pady = 10)

    def update(self, root):

        # analyze conditions where user input is invalid
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
                # add assignments and tasks to lists and text file if user input is valid
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

                # clears all widgets and resets frames
                root.clear_widgets()
                root.setup()
                root.scroller.canvas.configure(scrollregion=root.scroller.canvas.bbox("all"))
                self.window.destroy()
    
    # clears all user input
    def clear(self):
        for i in range(len(self.entries)):
            self.entries[i].delete(0, END)


# some code taken from https://www.youtube.com/watch?v=0WafQCaok6g
class Scroller:
    def __init__(self, mainframe):
        # set up scroller
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

    # detects whether scrollbar is being used
    def scrolling(self, event):
        if not self.is_scrolling:
            HomeworkManager.scrolling = True
        self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
        self.is_scrolling = True
    
    def stop_scrolling(self, event):
        HomeworkManager.scrolling = False
        self.is_scrolling = False

class Calendar:
    def __init__(self, frame, year, month, root):
        # set up calendar frame
        self.year = int(year)
        self.month = int(month)

        self.calendar = Frame(frame, bg = HomeworkManager.BLACK, padx = 10, pady = 10)
        self.calendar.pack()

        self.weekdays = ["M", "T", "W", "T", "F", "S", "S"]
        self.months = ["January", "Februrary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.update(root)

    def update(self, root):
        if not HomeworkManager.scrolling:
            # set up the header for the calendar
            header = Frame(self.calendar, bg = HomeworkManager.BLACK)
            header.pack(side = TOP)

            back_button = Button(header, text = "<", width = 2, height = 1, command = lambda : self.prev_month(root))
            back_button.pack(side = LEFT)

            title = Label(header, text = f"{self.months[self.month-1]} 20{self.year}", font = ("Constantia", 15, "bold"), fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
            title.pack(side = LEFT, padx = 10)

            next_button = Button(header, text = ">", width = 2, height = 1, command = lambda : self.next_month(root))
            next_button.pack(side = LEFT)

            cal = calendar.monthcalendar(self.year, self.month)

            # check due dates for all assignments
            self.assignments = []
            self.ids = []
            for i in range(len(root.assignments)):
                self.assignments.append(root.assignments[i].end_date())
                self.ids.append(root.assignments[i].id)
            
            # set up the columns with buttons in the calendar
            columns = Frame(self.calendar, bg = HomeworkManager.BLACK)
            columns.pack(side = TOP)

            for i in range(len(self.weekdays)):
                column = Frame(columns, bg = HomeworkManager.BLACK, width = 30, height = 250)
                column.pack_propagate(False)
                column.pack(side = LEFT)

                header = Label(column, text = self.weekdays[i], font = ("Constantia", 10, "bold"), fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK, width = 2, height = 2)
                header.pack(side = TOP)

                for week in range(len(cal)):
                    for day in range(len(cal[week])):
                        if day == i:
                            if cal[week][day] != 0:
                                button = Button(column, text = str(cal[week][day]), command = lambda d = cal[week][day]: self.clicked(root, d), width = 2, height = 1)
                                button.pack(side = TOP, pady = 2)

                                m = f"0{self.month}" if self.month < 10 else f"{self.month}"
                                d = f"0{cal[week][day]}" if cal[week][day] < 10 else f"{cal[week][day]}"
                                self.date = f"20{self.year}/{m}/{d}"

                                if self.date in self.assignments:
                                    button.config(bg = HomeworkManager.RED)
                            else:
                                button = Button(column, width = 2, height = 1, bg = HomeworkManager.BLACK)
                                button.pack(side = TOP, pady = 2)

            # set up the description
            self.description = Label(self.calendar, font = ("Constantia", 10, "bold"), fg = HomeworkManager.WHITE, bg = HomeworkManager.BLACK)
            self.description.pack(side = TOP)

    def clicked(self, root, day):

        # clicking a date on the calendar will show its date and all due assignments
        m = f"0{self.month}" if self.month < 10 else f"{self.month}"
        d = f"0{day}" if day < 10 else f"{day}"
        string = f"20{self.year}/{m}/{d}"

        for i in range(len(self.assignments)):
            if self.assignments[i] == f"20{self.year}/{m}/{d}":
                for j in range(len(root.assignments)):
                    if root.assignments[j].id == self.ids[i]:
                        string += f"\n{root.assignments[j].end_time()} - {root.assignments[j].title}"
        self.description.config(text = string)
    
    # go back and forward a month on the calendar (only from 2000 to 2099)
    def prev_month(self, root):
        if self.month > 1:
            self.month -= 1
        elif self.year > 0:
            self.month = 12
            self.year -= 1

        for widget in self.calendar.winfo_children():
            widget.destroy()
        self.update(root)
    
    def next_month(self, root):
        if self.month < 12:
            self.month += 1
        elif self.year < 99:
            self.month = 1
            self.year += 1

        for widget in self.calendar.winfo_children():
            widget.destroy()
        self.update(root)
            
# main program
root = Tk()
app = HomeworkManager(root)
root.mainloop()