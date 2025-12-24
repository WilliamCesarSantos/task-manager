# 🗂️ Task Manager – Python Console Application

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Clean Code](https://img.shields.io/badge/code-clean%20code-brightgreen)](#clean-code-principles)
[![Architecture](https://img.shields.io/badge/architecture-layered-blueviolet)](#architecture)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](#license)

A simple **console-based task management application**, built with Python and designed to demonstrate **Clean Code**, **layered architecture**, and **good software design practices**.

This project is well-suited for **educational purposes**, small experiments, and as a reference for structuring CLI applications in Python.

---

## 📌 Project Idea

The goal of this project is to provide a lightweight task manager that runs entirely in the **terminal**, without external dependencies.

Each task contains:
- **Description**
- **Status**: `OPEN` or `CLOSED`
- **Due date**

All tasks are persisted in a **SQLite database**, ensuring data is preserved between executions.

This project focuses on:
- Code readability
- Separation of concerns
- Maintainability
- Simplicity

---

## 🧱 Architecture

The application follows a **layered architecture**, inspired by common Python conventions.

```
task_manager/
│
├── src/
│   └── task_manager/
│       ├── main.py # Application entry point
│       │
│       ├── domain/ # Business domain
│       │ └── task.py
│       │
│       ├── service/ # Business logic / use cases
│       │ └── task_service.py
│       │
│       ├── repository/ # Persistence layer
│       │ └── task_repository.py
│       │
│       ├── ui/ # Console user interface
│       │ └── console_menu.py
│       │
│       └── rest_api/ # REST API
│           └── rest_api.py
│
├── tests/ # Unit tests
│
└── data/
    └── tasks.db # SQLite storage file
```

### 📦 Domain Layer
Defines the `Task` entity and its behavior, independent of storage or user interface.

### ⚙️ Service Layer
Contains application use cases such as creating, editing, completing, and deleting tasks.

### 💾 Repository Layer
Handles persistence, converting tasks to and from SQLite format.

### 🖥️ UI Layer
Manages user interaction via terminal menus and input.

---

## 🧭 Features

The console menu provides the following options:
```
0 - Exit
1 - List tasks
2 - Edit task
3 - Delete task
4 - Add new task
5 - Complete task
```

---

## ▶️ How to Run

### 1️⃣ Requirements
- Python **3.10+**

### 2️⃣ Clone the repository
```bash
git clone <repository-url>
cd task_manager
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the application

**Console Mode:**
```bash
python src/task_manager/main.py CONSOLE
```

**REST API Mode:**
```bash
python src/task_manager/main.py REST_API
```

## 💾 Data Persistence

Tasks are stored in the following file: data/tasks.db

The file is automatically created on the first run if it does not exist.

## 🧼 Clean Code Principles

This project applies several Clean Code and design principles:

- Single Responsibility Principle (SRP)
- Clear and meaningful naming
- Low coupling between layers
- High cohesion
- Domain isolated from infrastructure
- Simple and readable code

## 📚 References

Clean Code – Robert C. Martin

Architecture Patterns with Python – Harry Percival

PEP 8 – Python Style Guide