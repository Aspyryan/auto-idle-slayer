# flake8: noqa
from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

import time
from win32gui import FindWindow, GetWindowRect
from pynput.mouse import Button, Controller
from pynput import keyboard
from threading import Thread, Event
from PIL import Image
import pyautogui
import os
from replay_mouse_events import replay_mouse_events, swipe_left, swipe_right

mouse = Controller()
keyboard_listener = None  
chest_hunt = Event()
bonus_stage = Event()
bonus_stage_direction = None
bonus_stage_slider_location = None

# FindWindow takes the Window Class name (can be None if unknown), and the window's display text. 
window_handle = FindWindow(None, "Idle Slayer")
window_rect = GetWindowRect(window_handle)

width = window_rect[2] - window_rect[0]
height = window_rect[3] - window_rect[1]

def safeLocateOnScreen(image, grayscale=True, confidence=0.9):
    try:
        return pyautogui.locateOnScreen(image, grayscale=grayscale, confidence=confidence)
    except Exception:
        return None


def log(msg):
    print(time.strftime('%H:%M:%S') + ' -', msg)

def watch_keyboard():
    global keyboard_listener

    def on_press(key):
        if key == keyboard.Key.esc:
            os._exit(1)
    
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()
    keyboard_listener.join()


def click_mouse(amount, button=Button.left):
    mouse.press(button)
    time.sleep(amount)
    mouse.release(button)


def auto_clicker():
    mouse.position = (window_rect[0] + width // 2, window_rect[1] + 40)
    click_mouse(0.4)
    click_mouse(0.15)
    click_mouse(0.2)
    click_mouse(0.1)
    # click_mouse(0.02)

    click_mouse(0.05, Button.right)
    mouse.position = (window_rect[2] - 210, window_rect[1] + 150)
    click_mouse(0.1)
    time.sleep(0.1)
    # time.sleep(3)


def chest_hunt_detector():
    while True:
        time.sleep(2)

        if chest_hunt.is_set():
            continue

        color = get_average_window_color()
        rGood = 70 <= color[0] <= 74
        gGood = 55 <= color[1] <= 59
        bGood = 37 <= color[2] <= 42
        if rGood and gGood and bGood:
            chest_hunt.set()


def get_average_window_color():
    px = ImageGrab.grab(bbox=window_rect, include_layered_windows=False, all_screens=True).load()
    average_color = [0, 0, 0]
    for x in range(width):
        for y in range(height):
            for i in range(3):
                average_color[i] += px[x, y][i]

    for i in range(3):
        average_color[i] //= width * height

    # log(average_color)
    return average_color


def get_average_box_color(x1, y1, x2, y2):
    px = ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True).load()
    average_color = [0, 0, 0]
    for x in range(x1, x2):
        for y in range(y1, y2):
            for i in range(3):
                average_color[i] += px[x, y][i]

    for i in range(3):
        average_color[i] //= (x2 - x1) * (y2 - y1)

    log(average_color)
    return average_color


def get_pixel_color(x, y):
    px = ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True).load()
    return px[x, y]


def play_chest_hunt():
    topleft = (window_rect[0] + width / 100 * 14, window_rect[1] + height / 100 * 36)
    bottomright = (window_rect[2] - width / 100 * 15, window_rect[3] - height / 100 * 33)

    while True:
        # make a grid from the positions above of 10x3 and make it move from left to right and top to bottom, make it click the middle of the cell
        for y in range(3):
            for x in range(10):
                mouse.position = (topleft[0] + (bottomright[0] - topleft[0]) / 10 * x + (bottomright[0] - topleft[0]) / 20, topleft[1] + (bottomright[1] - topleft[1]) / 3 * y + (bottomright[1] - topleft[1]) / 6)
                click_mouse(0.1)
                time.sleep(0.15)
     
        buttonColor = get_pixel_color(window_rect[0] + width / 100 * 40, window_rect[1] + height / 100 * 90)
        if (buttonColor[0] == 180 and buttonColor[1] == 0 and buttonColor[2] == 0):
            mouse.position = (window_rect[0] + width / 100 * 40, window_rect[1] + height / 100 * 90)
            time.sleep(1)
            click_mouse(0.2)
            time.sleep(1)
            break


def bonus_stage_detector():
    global bonus_stage_direction, bonus_stage_slider_location
    while True:
        time.sleep(4)

        if bonus_stage.is_set():
            continue

        bonusStageStar = safeLocateOnScreen('images/bonus-stage.png', grayscale=True, confidence=0.9)

        if bonusStageStar:
            swipeLeft = safeLocateOnScreen('images/bonus-stage-left-swipe.png', grayscale=True, confidence=0.9)
            swipeRight = safeLocateOnScreen('images/bonus-stage-right-swipe.png', grayscale=True, confidence=0.9)

            if (not swipeLeft and not swipeRight):
                continue

            if (swipeLeft and not swipeRight):
                bonus_stage_direction = 'left'
                bonus_stage_slider_location = swipeLeft

            if (not swipeLeft and swipeRight):
                bonus_stage_direction = 'right'
                bonus_stage_slider_location = swipeRight
                
            bonus_stage.set()
        
        # log(bonusStageStar)

def play_bonus_stage():
    if bonus_stage_direction == 'left':
        swipe_left(bonus_stage_slider_location)
    else:
        swipe_right(bonus_stage_slider_location)
    time.sleep(13.2)
    replay_mouse_events('mouse_data_bonus_stage.json')

    location = safeLocateOnScreen('images/bonus_stage_retry.png', grayscale=True, confidence=0.9)

    if (location):
        (left, top, width, height) = location
        mouse.position = (left + (width / 100 * 65), top + (height / 100 * 85))
        time.sleep(0.5)
        click_mouse(0.2)
        time.sleep(0.5)



def main():
    while True:
        auto_clicker()
        # time.sleep(0.1)
        if chest_hunt.is_set():
            log('CHEST HUNT!')
            play_chest_hunt()
            log('CHEST HUNT OVER!')
            chest_hunt.clear()
        if bonus_stage.is_set():
            log('BONUS STAGE!' + bonus_stage_direction)
            play_bonus_stage()
            log('BONUS STAGE OVER!')
            bonus_stage.clear()

log(window_rect)

t1 = Thread(target=watch_keyboard, name='t1')
t2 = Thread(target=main, name='t2')
t3 = Thread(target=chest_hunt_detector, name='t3')
t4 = Thread(target=bonus_stage_detector, name='t4')

t1.start()
t2.start()
t3.start()
t4.start()


# play_bonus_stage()
# play_chest_hunt()