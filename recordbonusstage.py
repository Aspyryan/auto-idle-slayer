import json  
import time  
from pynput import mouse, keyboard  
  
# List to hold the recorded data  
data = []  
  
# Variables to track the time  
press_time = 0  
release_time = 0  
last_release_time = 0  
  
def on_click(x, y, button, pressed):  
    global press_time, release_time, last_release_time  
      
    if button == mouse.Button.left:  
        if pressed:  
            press_time = time.time()  
            if last_release_time != 0:  
                delay_between_presses = press_time - last_release_time  
                data.append({'event': 'delay', 'value': delay_between_presses})  
        else:  
            release_time = time.time()  
            press_duration = release_time - press_time  
            data.append({'event': 'press_duration', 'value': press_duration})  
            last_release_time = release_time  
  
def on_press(key):  
    if key == keyboard.Key.esc:  
        # Stop listener  
        return False  
  
# Set up the mouse listener  
mouse_listener = mouse.Listener(on_click=on_click)  
  
# Set up the keyboard listener  
keyboard_listener = keyboard.Listener(on_press=on_press)  
  
# Start both listeners  
mouse_listener.start()  
keyboard_listener.start()  
  
# Wait for the keyboard listener to stop  
keyboard_listener.join()  
  
# Stop the mouse listener if it's still running  
mouse_listener.stop()  
  
# Save the recorded data to a JSON file  
with open('mouse_data_bonus_stage_spirit_boost.json', 'w') as json_file:  
    json.dump(data, json_file, indent=4)  
  
print("Mouse data has been recorded to mouse_data.json")  