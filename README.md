# Task Manager

## Intro

This is a task management application designed to streamline your workflow and enhance productivity. The application offers a user-friendly interface where you can easily create, edit, organize, and track your tasks. With features such as user authentication, task prioritization, and filtering options, this task manager ensures that you stay on top of your commitments and deadlines.

It leverages the power of Django, providing a robust and scalable backend, while TailwindCSS ensures a clean and modern user interface.
- Django, TailwindCSS

## Key Features

- User Authentication: Secure login and registration to personalize your task management experience.
- Task Creation and Editing: Easily add new tasks, and update existing tasks.
- Task Organization: Categorize tasks by priority, status, and due date to maintain an organized workflow.
- Filtering and Sorting: Quickly find tasks using filter and sort options to manage your tasks efficiently.
- Responsive Design: Accessible on various devices, ensuring you can manage your tasks on the go.

## Setup

1. Clone the repository
2. Create a virtual environment (optional, but better)
3. Install dependencies: `pip install -r requirements.txt`
4. Apply migrations: `python manage.py migrate`
5. Create a superuser: `python manage.py createsuperuser`
6. Run the server: `python manage.py runserver`

## Usage

1. Navigate to `http://127.0.0.1:8000/` (root url) to view the task home page.
2. Use the links to create, edit, view, or delete tasks.
3. Use the authenticate links - login, register, logout.


### NB:
The device(laptop, ipad, PC, etc) needs to be online for the app to function properly.