import pyautogui
import time
import cv2
import numpy as np
from PIL import ImageGrab
import tkinter as tk
from tkinter import ttk
import win32api
import win32con

# Constants
RUNESCAPE_WINDOW_TITLE = "RuneScape"
HEAT_BAR_REGION = (1256, 679, 1305, 683) 
FURNACE_POSITION = (1337, 690) 
ANVIL_POSITION = (1280, 660) 
YELLOW_THRESHOLD = 10  

# Define the color range for yellow/orange in BGR format
LOWER_YELLOW = np.array([0, 50, 100])  
UPPER_YELLOW = np.array([80, 255, 255])

# Global variables
running = False

def virtual_click(x, y):
    """Simulate a mouse click at the specified coordinates without moving the physical cursor."""
    # Save the current cursor position
    original_pos = win32api.GetCursorPos()

    # Move the cursor to the target position
    win32api.SetCursorPos((x, y))

    # Simulate a mouse click
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)  # Left button down
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)  # Left button up

    # Restore the original cursor position
    win32api.SetCursorPos(original_pos)

    print(f"Clicked at ({x}, {y})")

def activate_runescape_window():
    """Activate the RuneScape window."""
    try:
        window = pyautogui.getWindowsWithTitle(RUNESCAPE_WINDOW_TITLE)[0]
        window.activate()
        time.sleep(1)  # Wait for the window to activate
        print("RuneScape window activated!")
    except IndexError:
        print("RuneScape window not found!")
        exit()

def capture_heat_bar():
    """Capture the heat bar region."""
    try:
        screenshot = ImageGrab.grab(bbox=HEAT_BAR_REGION)
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV
    except Exception as e:
        print(f"Error capturing heat bar: {e}")
        exit()

def is_heat_bar_cooled(heat_bar_image):
    """Check if the heat bar is mostly blue (i.e., yellow/orange is close to the left)."""
    # Convert the image to HSV for better color detection
    hsv_image = cv2.cvtColor(heat_bar_image, cv2.COLOR_BGR2HSV)

    # Create a mask for yellow/orange pixels
    yellow_mask = cv2.inRange(hsv_image, LOWER_YELLOW, UPPER_YELLOW)

    # Calculate the percentage of yellow/orange pixels
    total_pixels = heat_bar_image.shape[0] * heat_bar_image.shape[1]
    yellow_pixels = cv2.countNonZero(yellow_mask)
    yellow_percentage = (yellow_pixels / total_pixels) * 100

    return yellow_percentage <= YELLOW_THRESHOLD, yellow_percentage

def click_furnace():
    """Click on the furnace."""
    virtual_click(*FURNACE_POSITION)  # Use virtual click
    print("Clicked on the furnace!")

def click_anvil():
    """Click on the anvil."""
    virtual_click(*ANVIL_POSITION)  # Use virtual click
    print("Clicked on the anvil!")

def update_gui():
    """Update the GUI with the current heat bar percentage."""
    if running:
        heat_bar_image = capture_heat_bar()
        cooled, yellow_percentage = is_heat_bar_cooled(heat_bar_image)
        heat_percentage = 100 - yellow_percentage

        # Update the progress bar and label
        progress_bar['value'] = heat_percentage
        percentage_label.config(text=f"Heat Left: {heat_percentage:.2f}%")

        if cooled:
            print("Heat bar is mostly blue! Clicking furnace...")
            click_furnace()
            time.sleep(3)
            click_anvil()

    # Schedule the function to run again after 1 second
    root.after(1000, update_gui)

def start_script():
    """Start the script."""
    global running
    running = True
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    activate_runescape_window()
    update_gui()

def stop_script():
    """Stop the script."""
    global running
    running = False
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# Create the GUI
root = tk.Tk()
root.title("RuneScape Heat Bar Monitor")

# Progress bar
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.pack(pady=10)

# Percentage label
percentage_label = tk.Label(root, text="Heat Left: 0.00%", font=("Arial", 14))
percentage_label.pack(pady=10)

# Start/Stop buttons
start_button = tk.Button(root, text="Start", command=start_script)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop", command=stop_script, state=tk.DISABLED)
stop_button.pack(pady=5)

# Run the GUI
root.mainloop()