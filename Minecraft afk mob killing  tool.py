import time
import threading
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Listener, KeyCode, Controller as KeyboardController

keyboard = KeyboardController()
mouse = MouseController()

delay = 0.08
button = Button.left
start_stop_key = KeyCode(char='[')
exit_key = KeyCode(char=']')


class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True
    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                keyboard.press(Key.space)
                time.sleep(self.delay)


click_thread = ClickMouse(delay, button)
click_thread.start()


def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
            keyboard.release(Key.space)
        else:
            click_thread.start_clicking()
    elif key == exit_key:
        keyboard.release(Key.space)
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()
