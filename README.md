# ToDo List App (Kivy)

A functional, real-world productivity desktop application built with Python and the Kivy framework to help users manage their daily tasks.

## Features
- Add, view, and complete tasks via a clean graphical user interface (GUI).
- Persistent data storage: Tasks are automatically saved to and loaded from a local `tarefas.json` file.
- Modular code architecture separating application layout from data handling logic.

## How to Run the Project

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AlexMarques00/ToDo-List.git
   cd ToDo-List
   ```

2. **Install dependencies:**
   Make sure you have Kivy installed:
   ```bash
   pip install kivy
   ```

3. **Run the application:**
   ```bash
   python todo_kivy_app.py
   ```

## Project Structure
- `todo_kivy_app.py`: The main GUI interface and frontend layout built using Kivy.
- `todo_functions.py`: The data-handling module managing JSON reading and writing.
- `tarefas.json`: The local text database used to store active task lists.
