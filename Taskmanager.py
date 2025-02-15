import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from datetime import datetime
import json

tasks = []

class Task:
    def __init__(self, task, due_date=None, priority=None, category=None):
        self.task = task
        self.completed = False
        self.due_date = due_date if due_date else "No due date"
        self.priority = priority if priority else "No priority"
        self.category = category if category else "No category"

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f'{self.task} [{status}] - Due: {self.due_date} - Priority: {self.priority} - Category: {self.category}'

class TimedTask(Task):
    def __init__(self, task, due_date=None, priority=None, category=None, time_required=None):
        super().__init__(task, due_date, priority, category)
        self.time_required = time_required if time_required else "No time required"

    def __str__(self):
        base_str = super().__str__()
        return f'{base_str} - Time Required: {self.time_required}'

def add_task():
    task = task_entry.get()
    if task:
        due_date = askstring("Due Date", "Enter due date (YYYY-MM-DD) or leave blank:")
        priority = askstring("Priority", "Enter priority (High/Medium/Low) or leave blank:")
        category = askstring("Category", "Enter category or leave blank:")
        time_required = askstring("Time Required", "Enter time required or leave blank:")
        if time_required:
            task_details = TimedTask(task, due_date, priority, category, time_required)
        else:
            task_details = Task(task, due_date, priority, category)
        tasks.append(task_details)
        update_tasks()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def delete_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        tasks.pop(selected_task_index[0])
        update_tasks()
    else:
        messagebox.showwarning("Warning", "No task selected!")

def complete_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        tasks[selected_task_index[0]].mark_completed()
        update_tasks()
    else:
        messagebox.showwarning("Warning", "No task selected!")

def edit_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task = tasks[selected_task_index[0]]
        new_task = askstring("Edit Task", "Edit task:", initialvalue=task.task)
        if new_task:
            task.task = new_task
            task.due_date = askstring("Due Date", "Enter due date (YYYY-MM-DD) or leave blank:", initialvalue=task.due_date)
            task.priority = askstring("Priority", "Enter priority (High/Medium/Low) or leave blank:", initialvalue=task.priority)
            task.category = askstring("Category", "Enter category or leave blank:", initialvalue=task.category)
            if isinstance(task, TimedTask):
                task.time_required = askstring("Time Required", "Enter time required or leave blank:", initialvalue=task.time_required)
            update_tasks()
    else:
        messagebox.showwarning("Warning", "No task selected!")

def search_tasks():
    keyword = search_entry.get()
    if keyword:
        search_results = [task for task in tasks if keyword.lower() in task.task.lower()]
        task_listbox.delete(0, tk.END)
        for task in search_results:
            task_listbox.insert(tk.END, str(task))
    else:
        messagebox.showwarning("Warning", "Search keyword cannot be empty!")

def sort_tasks_by_due_date():
    tasks.sort(key=lambda x: x.due_date if x.due_date != "No due date" else "")
    update_tasks()

def sort_tasks_by_priority():
    priority_order = {"High": 1, "Medium": 2, "Low": 3, "No priority": 4}
    tasks.sort(key=lambda x: priority_order[x.priority])
    update_tasks()

def update_tasks():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, str(task))

def clear_all_tasks():
    tasks.clear()
    update_tasks()

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump([task.__dict__ for task in tasks], file)
    messagebox.showinfo("Info", "Tasks saved successfully!")

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            loaded_tasks = json.load(file)
            for task_data in loaded_tasks:
                if "time_required" in task_data:
                    task = TimedTask(**task_data)
                else:
                    task = Task(**task_data)
                tasks.append(task)
        update_tasks()
        messagebox.showinfo("Info", "Tasks loaded successfully!")
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No saved tasks found!")

# Create the main window
root = tk.Tk()
root.title("Task Manager")
root.geometry("600x400")  # Set a fixed window size

# Define a common font
common_font = ("Helvetica", 12)

# Create frames for better organization
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

listbox_frame = tk.Frame(root)
listbox_frame.pack(pady=10)

# Create and place the widgets in the input frame
task_label = tk.Label(input_frame, text="Enter a task:", font=common_font)
task_label.grid(row=0, column=0, padx=5, pady=5)

task_entry = tk.Entry(input_frame, width=50, font=common_font)
task_entry.grid(row=0, column=1, padx=5, pady=5)

add_button = tk.Button(input_frame, text="Add Task", command=add_task, bg="green", fg="white", font=common_font)
add_button.grid(row=0, column=2, padx=5, pady=5)

# Create and place the widgets in the button frame
delete_button = tk.Button(button_frame, text="Delete Task", command=delete_task, bg="red", fg="white", font=common_font)
delete_button.grid(row=0, column=0, padx=5, pady=5)

complete_button = tk.Button(button_frame, text="Complete Task", command=complete_task, font=common_font)
complete_button.grid(row=0, column=1, padx=5, pady=5)

edit_button = tk.Button(button_frame, text="Edit Task", command=edit_task, font=common_font)
edit_button.grid(row=0, column=2, padx=5, pady=5)

search_label = tk.Label(button_frame, text="Search tasks:", font=common_font)
search_label.grid(row=1, column=0, padx=5, pady=5)

search_entry = tk.Entry(button_frame, width=50, font=common_font)
search_entry.grid(row=1, column=1, padx=5, pady=5)

search_button = tk.Button(button_frame, text="Search", command=search_tasks, font=common_font)
search_button.grid(row=1, column=2, padx=5, pady=5)

sort_due_date_button = tk.Button(button_frame, text="Sort by Due Date", command=sort_tasks_by_due_date, font=common_font)
sort_due_date_button.grid(row=2, column=0, padx=5, pady=5)

sort_priority_button = tk.Button(button_frame, text="Sort by Priority", command=sort_tasks_by_priority, font=common_font)
sort_priority_button.grid(row=2, column=1, padx=5, pady=5)

clear_button = tk.Button(button_frame, text="Clear All Tasks", command=clear_all_tasks, font=common_font)
clear_button.grid(row=2, column=2, padx=5, pady=5)

save_button = tk.Button(button_frame, text="Save Tasks", command=save_tasks, font=common_font)
save_button.grid(row=3, column=0, padx=5, pady=5)

load_button = tk.Button(button_frame, text="Load Tasks", command=load_tasks, font=common_font)
load_button.grid(row=3, column=1, padx=5, pady=5)

# Create and place the listbox and scrollbar in the listbox frame
task_listbox = tk.Listbox(listbox_frame, width=80, height=15, font=common_font)
task_listbox.pack(side=tk.LEFT, padx=5, pady=5)

scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=task_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_listbox.config(yscrollcommand=scrollbar.set)

# Start the main loop
root.mainloop()
