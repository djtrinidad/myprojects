#!/usr/bin/python3

# Simple Pomodoro Timer in Python3

import tkinter as tk
from tkinter import ttk
import time

# Set up the main application window
root = tk.Tk()
root.title("Pomodoro Timer")

# Set the dimensions of the window
root.geometry("300x165")

# Create a label to display the countdown
label = tk.Label(root, text="", font=("Helvetica", 48))
label.pack(pady=20)

# Add a combobox to select between 25/5 or 50/10
session_options = [("25/5", 25, 5), ("50/10", 50, 10)]
session_var = tk.StringVar()
session_dropdown = ttk.Combobox(root, textvariable=session_var, values=[opt[0] for opt in session_options], state="readonly")
session_dropdown.set("25/5") # Default selection
session_dropdown.pack(pady=5)

# Function to start the countdown
def countdown(time_in_seconds, session_type):
    while time_in_seconds > 0:
        mins, secs = divmod(time_in_seconds, 60)
        time_format = f"{mins:02d}:{secs:02d}"
        label.config(text=time_format)
        root.update()
        time.sleep(1)
        time_in_seconds -= 1

    # Change the background color when the session ends
    if session_type == "study":
        root.config(bg="green") # indicates break time
    else:
        root.config(bg="red")  # indicates study time

    root.update()
    time.sleep(2)  # Pause for 2 seconds to show background color change

# Function to start Pomodoro Timer
def start_pomodoro():
    # Get the selected session type
    selected_option = session_dropdown.get()
    study_time = next(opt[1] for opt in session_options if opt[0] == selected_option)
    break_time = next(opt[2] for opt in session_options if opt[0] == selected_option)
    
    for _ in range(2):  # Run two sessions
        root.config(bg="white")
        countdown(study_time * 60,  "study")  # 25 min study sessions
        root.config(bg="green")
        countdown(break_time * 60, "break")  # 5 min break session
    label.config(text="Done!", font=("Helvetica", 32))
    root.config(bg="blue")

# Add a start button
start_button = tk.Button(root, text="Start", command=start_pomodoro, font=("Helvetica", 16))
start_button.pack(pady=10)

# Run main loop
root.mainloop()
