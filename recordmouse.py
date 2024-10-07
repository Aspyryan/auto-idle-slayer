# https://www.shedloadofcode.com/blog/record-mouse-and-keyboard-for-automation-scripts-with-python
"""  
Records mouse and keyboard and outputs the actions to a JSON file recording.json  
  
To begin recording:  
- Run `python record.py`  
  
To end recording:  
- Hold right click for 2 seconds then release to end the recording for mouse.  
"""  
  
import time  
import json  
from pynput import mouse, keyboard  
from win32gui import FindWindow, GetWindowRect  
  
print("Hold right click for 2 seconds then release to end the recording for mouse")  
  
recording = []  
count = 0  
  
# Find the window handle and its rectangle  
window_handle = FindWindow(None, "Idle Slayer")  
window_rect = GetWindowRect(window_handle)  
window_x, window_y, window_w, window_h = window_rect  
  
def on_move(x, y):  
    if len(recording) >= 1:  
        if (recording[-1]['action'] == "pressed" and  
            recording[-1]['button'] == 'Button.left') or \
           (recording[-1]['action'] == "moved" and  
            time.time() - recording[-1]['_time'] > 0.02):  
            json_object = {  
                'action': 'moved',  
                'x': x - window_x,  # Convert to relative x  
                'y': y - window_y,  # Convert to relative y  
                '_time': time.time()  
            }  
            recording.append(json_object)  
  
def on_click(x, y, button, pressed):  
    json_object = {  
        'action': 'clicked' if pressed else 'unclicked',  
        'button': str(button),  
        'x': x - window_x,  # Convert to relative x  
        'y': y - window_y,  # Convert to relative y  
        '_time': time.time()  
    }  
    recording.append(json_object)  
    if len(recording) > 1:  
        if recording[-1]['action'] == 'unclicked' and \
           recording[-1]['button'] == 'Button.right' and \
           recording[-1]['_time'] - recording[-2]['_time'] > 2:  
            with open('recording.json', 'w') as f:  
                json.dump(recording, f)  
            print("Mouse recording ended.")  
            return False  
  
def on_scroll(x, y, dx, dy):  
    json_object = {  
        'action': 'scroll',  
        'vertical_direction': int(dy),  
        'horizontal_direction': int(dx),  
        'x': x - window_x,  # Convert to relative x  
        'y': y - window_y,  # Convert to relative y  
        '_time': time.time()  
    }  
    recording.append(json_object)  
  
def start_recording():  
    mouse_listener = mouse.Listener(  
        on_click=on_click,  
        on_scroll=on_scroll,  
        on_move=on_move)  
    mouse_listener.start()  
    mouse_listener.join()  
  
if __name__ == "__main__":  
    print('Starting in 2 seconds')
    time.sleep(2)
    print('Recording...')
    start_recording()  