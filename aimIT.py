from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# File to store tasks
TASKS_FILE = "tasks.json"

# Function to load tasks from the file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save tasks to the file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Home route to display tasks
@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    due_date = request.form['due_date']
    
    tasks = load_tasks()
    tasks.append({
        "title": title,
        "description": description,
        "due_date": due_date,
        "completed": False
    })
    save_tasks(tasks)
    
    return redirect(url_for('index'))

# Route to mark a task as completed
@app.route('/complete/<int:task_index>')
def complete_task(task_index):
    tasks = load_tasks()
    tasks[task_index]["completed"] = True
    save_tasks(tasks)
    
    return redirect(url_for('index'))

# Route to delete a task
@app.route('/delete/<int:task_index>')
def delete_task(task_index):
    tasks = load_tasks()
    tasks.pop(task_index)
    save_tasks(tasks)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

