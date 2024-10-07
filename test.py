from PIL import ImageGrab, ImageDraw  
from win32gui import GetWindowRect, GetDesktopWindow  
from PyHook3 import HookManager  
import ctypes
import pythoncom  
from win32gui import FindWindow, GetWindowRect

class Draw_Screen_Rect:  
    def __init__(self):  
        self.start_pos = None  
        self.end_pos = None  
        self.final_rect = None  
        self.clicked = False  
        self.screen_img = None  
  
    def _draw_rect_on_image(self):  

        window_handle = FindWindow(None, "Idle Slayer")
        window_rect   = GetWindowRect(window_handle)
        center = window_rect[0] + (window_rect[2] - window_rect[0]) // 2, window_rect[1] + (window_rect[3] - window_rect[1]) // 2

        # Capture the current screen image  
        self.screen_img = ImageGrab.grab()  
        draw = ImageDraw.Draw(self.screen_img)  
  
        # Draw the rectangle on the image  
        draw.rectangle([self.start_pos, self.end_pos], outline='red', width=3)  
        draw.rectangle([center[0] - 5, center[1] - 5, center[0] + 5, center[1] + 5], outline='blue', width=3)
        draw.rectangle([center[0] - 235, center[1] - 260, center[0] + 235, center[1] + 45], outline='blue', width=3)
        del draw  # Release the drawing context  
  
    def _OnMouseEvent(self, event):  
        if event.Message == 513:  # WM_LBUTTONDOWN  
            self.clicked = True  
            self.start_pos = event.Position  
        elif event.Message == 514:  # WM_LBUTTONUP  
            self.clicked = False  
            self.end_pos = event.Position  
            self._draw_rect_on_image()  
            self.final_rect = (self.start_pos, self.end_pos)  
            self._destroy_hooks()  
        elif event.Message == 512 and self.clicked:  # WM_MOUSEMOVE  
            self.end_pos = event.Position  
        return True  
  
    def create_hooks(self):  
        self.hm = HookManager()  
        self.hm.MouseLeftDown = self._OnMouseEvent  
        self.hm.MouseLeftUp = self._OnMouseEvent  
        self.hm.MouseMove = self._OnMouseEvent  
        self.hm.HookMouse()  
        self.hm.HookKeyboard()  
  
    def _destroy_hooks(self):  
        self.hm.UnhookMouse()  
        self.hm.UnhookKeyboard()
        ctypes.windll.user32.PostQuitMessage(0)
  
    def output(self):  
        return self.final_rect  
  
    def show_image(self):  
        if self.screen_img:  
            self.screen_img.show()  
  
if __name__ == '__main__':  
    app = Draw_Screen_Rect()  
    app.create_hooks()  
    pythoncom.PumpMessages()  
    out = app.output()  

    window_handle = FindWindow(None, "Idle Slayer")
    window_rect   = GetWindowRect(window_handle)
    center = window_rect[0] + (window_rect[2] - window_rect[0]) // 2, window_rect[1] + (window_rect[3] - window_rect[1]) // 2

    leftFromCenter = out[0][0] - center[0]
    topFromCenter = out[0][1] - center[1]
    rightFromCenter = out[1][0] - center[0]
    bottomFromCenter = out[1][1] - center[1]

    print(f'({leftFromCenter}, {topFromCenter}, {rightFromCenter}, {bottomFromCenter})')

    app.show_image()  
