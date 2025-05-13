import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Checky")
        self.root.geometry("400x400+200+200")
        self.root.config(bg="#2e2e2e")
        self.root.resizable(True, True)

        tk.Label(root, text="My Tasks", font=("Arial", 16, 'bold'), fg="#f0f0f0", bg="#2e2e2e").pack(pady=10)

        self.task_listbox = tk.Listbox(root, font=("Arial", 12), bg="#333333", fg="#ffffff", selectbackground="#555555", selectforeground="#ffffff")
        self.task_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        scroll = tk.Scrollbar(self.task_listbox)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scroll.set)
        scroll.config(command=self.task_listbox.yview)

        self.task_entry = tk.Entry(root, font=("Arial", 12), bg="#444444", fg="#ffffff", insertbackground="white")
        self.task_entry.pack(padx=10, pady=5, fill=tk.X)

        self.priority_label = tk.Label(root, text="Priority:", fg="#f0f0f0", bg="#2e2e2e")
        self.priority_label.pack(pady=5)
        self.priority_combobox = ttk.Combobox(root, values=["High", "Medium", "Low"], state="readonly")
        self.priority_combobox.set("Medium")
        self.priority_combobox.pack(pady=5)

        btn_frame = tk.Frame(root, bg="#2e2e2e")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Add Task", width=15, command=self.add_task, bg="#444444", fg="#ffffff").pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Delete Selected", width=15, command=self.delete_task, bg="#444444", fg="#ffffff").pack(side=tk.LEFT, padx=2)
        tk.Button(root, text="Clear All", width=32, command=self.clear_tasks, bg="#444444", fg="#ffffff").pack(pady=2)

        self.load_tasks()

    def add_task(self):
        task = self.task_entry.get().strip()
        priority = self.priority_combobox.get()
        if task:
            task_color = self.get_task_color(priority)
            task_data = {
                "task": task,
                "priority": priority,
                "priority_color": task_color,
                "date_added": datetime.now().isoformat()
            }
            self.task_listbox.insert(tk.END, task)
            self.task_listbox.itemconfig(tk.END, {'bg': task_color})
            self.sort_tasks_by_priority()
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Empty Field", "Please enter a task.")

    def get_task_color(self, priority):
        if priority == "High":
            return "#B22222"
        elif priority == "Medium":
            return "orange"
        else:
            return "lightgreen"

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            self.task_listbox.delete(selected)
            self.save_tasks()
        else:
            messagebox.showwarning("No Selection", "Please select a task to delete.")

    def clear_tasks(self):
        if messagebox.askyesno("Confirm", "Delete all tasks?"):
            self.task_listbox.delete(0, tk.END)
            self.save_tasks()

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                tasks = json.load(f)
                for task in tasks:
                    self.task_listbox.insert(tk.END, task['task'])
                    self.task_listbox.itemconfig(tk.END, {'bg': task['priority_color']})
            self.sort_tasks_by_priority()

    def sort_tasks_by_priority(self):
        priority_map = {"High": 3, "Medium": 2, "Low": 1}
        tasks = []
        for i in range(self.task_listbox.size()):
            task = self.task_listbox.get(i)
            priority_color = self.task_listbox.itemcget(i, 'bg')
            priority = "High" if priority_color == "#B22222" else "Medium" if priority_color == "orange" else "Low"
            date_added = datetime.now().isoformat()
            tasks.append({'task': task, 'priority_color': priority_color, 'priority': priority, 'date_added': date_added})

        tasks.sort(key=lambda x: priority_map[x['priority']], reverse=True)

        self.task_listbox.delete(0, tk.END)
        for task in tasks:
            self.task_listbox.insert(tk.END, task['task'])
            self.task_listbox.itemconfig(tk.END, {'bg': task['priority_color']})
        self.save_tasks()

    def save_tasks(self):
        tasks = []
        for i in range(self.task_listbox.size()):
            task = self.task_listbox.get(i)
            priority_color = self.task_listbox.itemcget(i, 'bg')
            priority = "High" if priority_color == "#B22222" else "Medium" if priority_color == "orange" else "Low"
            date_added = datetime.now().isoformat()
            tasks.append({'task': task, 'priority_color': priority_color, 'priority': priority, 'date_added': date_added})

        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    TaskManager(root)
    root.mainloop()
