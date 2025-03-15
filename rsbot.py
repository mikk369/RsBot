import pyautogui
import time
import cv2
import numpy as np
from PIL import ImageGrab

# print(pyautogui.mouseInfo())

# Constants
RUNESCAPE_WINDOW_TITLE = "RuneScape"
HEAT_BAR_REGION = (1256, 679, 1305, 683)
FURNACE_POSITION = (1337, 690) 
ANVIL_POSITION = (1280, 660)
YELLOW_THRESHOLD = 10  # Percentage of yellow/orange pixels required to trigger a click

# Define the color range for yellow/orange in BGR format
# Adjust these values based on your heat bar's exact colors
LOWER_YELLOW = np.array([0, 50, 100])  # Lower bound for yellow/orange
UPPER_YELLOW = np.array([80, 255, 255])  # Upper bound for yellow/orange

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

    print(f"Heat left: {yellow_percentage:.2f}%")
    return yellow_percentage <= YELLOW_THRESHOLD

def click_furnace():
    """Click on the furnace."""
    pyautogui.click(FURNACE_POSITION)
    print("Clicked on the furnace!")

def click_anvil():
    """Click on the anvil."""
    pyautogui.click(ANVIL_POSITION)
    print("Clicked on the anvil!")

def main():
    print("Starting script...")
    activate_runescape_window()

    while True:
        print("Capturing heat bar...")
        heat_bar_image = capture_heat_bar()

        if is_heat_bar_cooled(heat_bar_image):
            print("Heat bar is mostly blue! Clicking furnace...")
            click_furnace()
            time.sleep(3)
            click_anvil()

             # Wait for the heat bar to change before checking again
            print("Waiting for heat bar to change...")
            while is_heat_bar_cooled(heat_bar_image):
                time.sleep(1)  # Wait 1 second before rechecking
                heat_bar_image = capture_heat_bar()
        
        time.sleep(5)

if __name__ == "__main__":
    main()