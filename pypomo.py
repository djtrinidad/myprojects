#!/usr/bin/python3

# Simple Pomodoro Timer in Python3

import tkinter as tk
import time

# Set up the main application window
root = tk.Tk()
root.title("Pomodoro timer")

# Set the dimentsions of the window
root.geometry("300x150")

# Create a label to display the countdown
label = tk.Label(root, text="", font=("Helvetica", 48))
label.pack(pady=20)

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
    for _ in range(2):  # Run two sessions
        root.config(bg="white")
        countdown(25 * 60,  "study")  # 25 min study sessions
        root.config(bg="green")
        countdown(5 * 60, "break")  # 5 min break session
    label.config(text="Done!", font=("Helvetica", 32))
    root.config(bg="blue")

# Add a start button
start_button = tk.Button(root, text="Start", command=start_pomodoro, font=("Helvetica", 16))
start_button.pack(pady=10)

# Run main loop
root.mainloop()
