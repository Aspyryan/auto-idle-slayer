import json  
import time  
from pynput.mouse import Button, Controller  
from pynput import keyboard  
  
# Global flag to stop the replay  
stop_replay = False  
  
def on_press(key):  
    global stop_replay  
    if key == keyboard.Key.esc:  
        stop_replay = True  
        return False  # Stop the keyboard listener  
  
# Load the recorded data from the JSON file  
with open('mouse_data.json', 'r') as json_file:  
    data = json.load(json_file)  
  
# Create a mouse controller object  
mouse = Controller()  
  
# Start the keyboard listener  
keyboard_listener = keyboard.Listener(on_press=on_press)  
keyboard_listener.start()  
  
# Replay the recorded events  
for event in data:  
    if stop_replay:  
        break  
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
  
# Ensure the keyboard listener is stopped  
keyboard_listener.stop()  
  
print("Mouse events replayed successfully or stopped by user.")  