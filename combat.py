import time
import pyautogui
import cv2
import numpy as np
import random
import win32api, win32con
import keyboard
import os
import threading

# print(pyautogui.mouseInfo())

# RuneScape window title
RUNESCAPE_WINDOW_TITLE = "RuneLite - KaMmAjJaA"
CANNONBALL_REGION = (1748, 916, 28, 17)  # Define the region of the screen to capture for cannonballs
EXIT_DOOR_REGION = (1697, 1143)  # Define the region of the screen to capture for exit door
EXIT_BUTTON = (1690, 1088)  # Define the coordinates of the exit button
PICKUP_CANNON_REGION = (1176, 895)  # Define the region of the screen to capture for picking up cannon
fist_click = 1759, 922  # Coordinates for the first click
second_click = 1252, 851  # Coordinates for the second click

# Function to activate RuneScape window
def activate_runescape_window():
    try:
        window = pyautogui.getWindowsWithTitle(RUNESCAPE_WINDOW_TITLE)[0]
        window.activate()
        time.sleep(1)
        print("RuneScape window activated!")
    except IndexError:
        print("RuneScape window not found!")
        exit()

# Function to check if cannonballs are in inventory
def check_for_cannonballs():
    # Take a screenshot of the inventory
    inventory_screenshot = pyautogui.screenshot(region=CANNONBALL_REGION)  # Define the region of the inventory
    inventory_image = np.array(inventory_screenshot)
    inventory_image = cv2.cvtColor(inventory_image, cv2.COLOR_RGB2BGR)  # Convert to BGR format (OpenCV default)

    # Save the inventory image for debugging
    # cv2.imwrite("inventory_image.png", inventory_image)

    # Load the reference cannonball image and convert it to grayscale
    cannonball_image = cv2.imread("cannonball.png", cv2.IMREAD_GRAYSCALE)

    # Save the cannonball template image for debugging
    # cv2.imwrite("cannonball_image.png", cannonball_image)

    # Convert the inventory image to grayscale
    inventory_gray = cv2.cvtColor(inventory_image, cv2.COLOR_BGR2GRAY)

    # Use OpenCV's template matching to find the cannonball in the inventory
    result = cv2.matchTemplate(inventory_gray, cannonball_image, cv2.TM_CCOEFF_NORMED)

    # Visualize the result of the template matching (matching areas will be highlighted)
    result_img = inventory_image.copy()
    threshold = 0.8  # Adjust the threshold if needed
    locations = np.where(result >= threshold)

    # Draw rectangles around matching regions (for visualization)
    for pt in zip(*locations[::-1]):
        cv2.rectangle(result_img, pt, (pt[0] + cannonball_image.shape[1], pt[1] + cannonball_image.shape[0]), (0, 255, 0), 2)

    # Save the result image with rectangles drawn around matches
    cv2.imwrite("result_image.png", result_img)

    # If no cannonball is found (locations is empty), return True (out of cannonballs)
    if len(locations[0]) == 0:
        return True



# Function to simulate a human-like mouse click
def virtual_click(x, y, click_type='left', move_delay=0.3, click_delay=0.1, precise=False):
    """Simulate a mouse click at the specified coordinates."""
    # Apply offset only if not in 'precise' mode
    if precise:
        offset_x = 0
        offset_y = 0
    else:
        offset_x = random.randint(-10, 10)
        offset_y = random.randint(-10, 10)

    x += offset_x
    y += offset_y

    win32api.SetCursorPos((x, y))
    time.sleep(move_delay)

    if click_type == 'left':
        # Simulate left-click (normal click)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(click_delay)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    elif click_type == 'right':
        # Simulate right-click
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
        time.sleep(click_delay)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)

def pick_up_cannon():
    """Simulate picking up the cannon."""
    virtual_click(second_click[0], second_click[1], click_type='right')  # Right-click on the cannon
    time.sleep(1)  # Wait for the context menu to appear
    virtual_click(PICKUP_CANNON_REGION[0], PICKUP_CANNON_REGION[1], click_type='left', precise=True)  # Click on the "Pick up" option

# Main loop
def main():
    activate_runescape_window()

    last_cannon_click_time = time.time()  # Track time for cannon click loop
    cannon_click_interval = random.randint(53, 60)  # random interval between 53 and 60 seconds
    
    while True:
        if keyboard.is_pressed("q"):
            print("Stopping script...")
            break

        # Main loop: First and second clicks
        virtual_click(fist_click[0], fist_click[1], click_type='left')  # First click
        virtual_click(second_click[0], second_click[1], click_type='left')  # Second click
        time.sleep(2)  # Delay between clicks
        virtual_click(second_click[0], second_click[1], click_type='left')  # Click again on the first click position

         # Check if cannonballs are in the inventory
        if check_for_cannonballs():
            print("Out of cannonballs, picking up cannon...")
            time.sleep(random.randint(2, 3))
            pick_up_cannon()
            time.sleep(2)
            virtual_click(EXIT_DOOR_REGION[0], EXIT_DOOR_REGION[1], click_type='left')  # Click on the exit button
            time.sleep(random.randint(2, 5))
            virtual_click(EXIT_BUTTON[0], EXIT_BUTTON[1], click_type='left')
            time.sleep(2)
            break

        # Handle cannon click loop every 5 minutes
        if time.time() - last_cannon_click_time >= cannon_click_interval:
            time.sleep(5)
            virtual_click(second_click[0], second_click[1], click_type='left')  # Click on cannon
            last_cannon_click_time = time.time()  # Update last click time

        # Move the cursor to a random safe position
        safe_x = random.randint(800, 1120)
        safe_y = random.randint(10, 200)
        win32api.SetCursorPos((safe_x, safe_y))

        # Delay between main actions (20 seconds)
        time.sleep(random.randint(16, 23))

if __name__ == "__main__":
    main()
