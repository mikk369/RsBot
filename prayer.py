import tkinter as tk
import threading
import pyautogui
import time
import win32api
import win32con
import random
from PIL import Image, ImageChops

# Constants
RUNESCAPE_WINDOW_TITLE = "RuneScape"
BANK = (1857, 577)
ASH_REGION = (1071, 633)
ASHES = (1095, 654)
WITHDRAWALL = (1000, 765)
BUFFER = 3
ALTAR_CLICK = (603, 849)
OFFER_ASHES = (565, 907)
OFFER_BONES = (570, 891)
FIRSTCLICK = (2204, 412)
SECONDCLICK = (2222, 573)
THIRD_RIGHTCLICK = (2248, 617)
FOURTHCLICK = (2222, 644)
FIRSTBACK_CLICK = (70, 833)
SECONDBACK_CLICK = (682, 999)
THIRDBACK_CLICK = (759, 1024)
FOURTHBACK_CLICK = (674, 761)
FIFTH_CLICK_ON_ALTAR = (773, 721)
running = False 
start_time = None
total_timer = None
selected_coords = None

def virtual_click(x, y, right_click=False, move_delay=0.3, click_delay=0.1):
    """Simulate a mouse click at the specified coordinates."""
    # Apply a random offset to make clicks more human-like
    offset_x = random.randint(-BUFFER, BUFFER)
    offset_y = random.randint(-BUFFER, BUFFER)

    x += offset_x
    y += offset_y

    win32api.SetCursorPos((x, y))
    time.sleep(move_delay)

    if right_click:
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
        time.sleep(1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
    else:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def activate_runescape_window():
    """Activate the RuneScape window."""
    try:
        window = pyautogui.getWindowsWithTitle(RUNESCAPE_WINDOW_TITLE)[0]
        window.activate()
        time.sleep(1)
        print("RuneScape window activated!")
    except IndexError:
        print("RuneScape window not found!")
        exit()

def click_bank():
    """Click the bank."""
    virtual_click(*BANK)
    time.sleep(3)

def prayer_loop():
    """Main loop for the prayer bot."""
    global running, start_time

    while running:
        if start_time is None:
            start_time = time.time()
        
        duration = 9 * 60  # 1 minute duration

        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            print("Going to take buffs!")
            move_and_pause()  # Move, then return
            start_time = time.time()  # ✅ Reset timer AFTER returning
            continue  # Restart loop from the beginning

        print("Running prayer loop...")

        click_bank()
        virtual_click(*ASHES, right_click=True)
        time.sleep(1)
        virtual_click(*WITHDRAWALL)
        time.sleep(0.5)
        virtual_click(*ALTAR_CLICK, right_click=True)
        time.sleep(1)
        virtual_click(*selected_coords)
        time.sleep(60)

def move_and_pause():
    """Moves the bot to a specific location, pauses for 1 minute, then returns to prayer_loop."""
    print("Moving to a different location...")
    virtual_click(*FIRSTCLICK)
    time.sleep(5)
    virtual_click(*SECONDCLICK)
    time.sleep(5)
    virtual_click(*THIRD_RIGHTCLICK, right_click=True)
    time.sleep(5)
    virtual_click(*FOURTHCLICK)
    time.sleep(30)
    virtual_click(*FIRSTBACK_CLICK)
    time.sleep(5)
    virtual_click(*SECONDBACK_CLICK)
    time.sleep(5)
    virtual_click(*THIRDBACK_CLICK)
    time.sleep(5)
    virtual_click(*FOURTHBACK_CLICK)
    time.sleep(5)
    virtual_click(*FIFTH_CLICK_ON_ALTAR)
    time.sleep(5)

    print("Returning to prayer loop...")
    return
    
def update_timer():
    """Updates the timer label every second."""
    global total_timer

    if running:
        elapsed_time = int(time.time() - total_timer)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
        root.after(1000, update_timer)

def start_prayer(start_button, stop_button):
    """Starts the prayer script in a new thread."""
    global running, start_time, total_timer
    if running:
        return
    running = True

    start_time = time.time()
    total_timer = time.time()
        
    activate_runescape_window()
    print("Prayer script started!")

    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    threading.Thread(target=prayer_loop, daemon=True).start()
    update_timer()

def stop_prayer(start_button, stop_button):
    """Stop the script."""
    global running
    running = False
    print("Prayer script stopped!")

    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    timer_label.config(text="Time: 00:00") #reset timer

def update_click_coordinates():
    """Update click coordinates based on selected checkbox."""
    global selected_coords

    if ashes_checkbox.get():
        print("Ashes selected")
        selected_coords = OFFER_ASHES
    elif bones_checkbox.get():
        print("Bones selected")
        selected_coords = OFFER_BONES


# GUI Setup
root = tk.Tk()
root.title("RuneScape Prayer Bot")
root.geometry("300x300")

title_label = tk.Label(root, text="Prayer Bot", font=("Arial", 14))
title_label.pack(pady=10)

timer_label = tk.Label(root, text="Run Time: 00:00", font=("Arial", 12))
timer_label.pack(pady=5)

# Checkbox variables
ashes_checkbox = tk.BooleanVar(value=False) 
bones_checkbox = tk.BooleanVar(value=False) 

# Checkboxes
checkbox1 = tk.Checkbutton(root, text="Offer Ashes", variable=ashes_checkbox, command=lambda: [bones_checkbox.set(False), update_click_coordinates()])
checkbox1.pack()

checkbox2 = tk.Checkbutton(root, text="Offer Bones", variable=bones_checkbox, command=lambda: [ashes_checkbox.set(False), update_click_coordinates()])
checkbox2.pack()

start_button = tk.Button(root, text="Start", command=lambda: start_prayer(start_button, stop_button))
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop", command=lambda: stop_prayer(start_button, stop_button))
stop_button.pack(pady=5)
stop_button.config(state=tk.DISABLED)

root.mainloop()
