import json  
import time  
from pynput.mouse import Button, Controller  
import pyautogui
from win32gui import FindWindow, GetWindowRect
  
def replay_mouse_events(filename):  
    """  
    Replays mouse events from a specified JSON file.  
  
    :param filename: The path to the JSON file containing mouse data.
    """  
    # Load the recorded data from the JSON file  
    with open(filename, 'r') as json_file:  
        data = json.load(json_file)  
  
    # Create a mouse controller object  
    mouse = Controller()  
  
    # Replay the recorded events  
    for event in data:  
        if event['event'] == 'press_duration':  
            # Press and hold the left mouse button  
            mouse.press(Button.left)  
            # Hold it for the recorded duration  
            time.sleep(event['value'])  
            # Release the left mouse button  
            mouse.release(Button.left)  
        elif event['event'] == 'delay':  
            # Wait for the recorded delay between presses  
            time.sleep(event['value'])  
      
    print("Mouse events replayed successfully.")  


def swipe_right(location):
    (left, top, width, height) = location

    startX = left + 20
    startY = top + (height / 2)

    pyautogui.moveTo(startX, startY, duration=0.0)
    pyautogui.mouseDown()
    pyautogui.moveTo(startX + width, startY, duration=0.5)
    pyautogui.mouseUp()

def swipe_left(location):
    (left, top, width, height) = location

    startX = left + (width - 20)
    startY = top + (height / 2)

    pyautogui.moveTo(startX, startY, duration=0.0)
    pyautogui.mouseDown()
    pyautogui.moveTo(startX - width, startY, duration=0.5)
    pyautogui.mouseUp()