import pyautogui
import time

time.sleep(1)

button7location = pyautogui.locateOnScreen('images/bonus_stage_retry.png', confidence=0.9)

print(button7location)