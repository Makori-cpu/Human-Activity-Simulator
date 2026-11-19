
import pyautogui
import random
import threading
import time


class MouseController:
        
    def click_at_current_position(self):
        pyautogui.click()

    def __init__(self):
        self.running = False
        self.paused = False
        self.interval = 2

        self.thread = None
        self.lock = threading.Lock()

        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1

    def get_random_position(self):
        screen_width, screen_height = pyautogui.size()

        x = random.randint(100, max(100, screen_width - 100))
        y = random.randint(100, max(100, screen_height - 100))

        return x, y

    def move_to_random_position(self):
        x, y = self.get_random_position()

        pyautogui.moveTo(x, y, duration=0.5)

        print(f"Mouse moved to: ({x}, {y})")

    def movement_loop(self):
        while self.running:

            if not self.paused:
                try:
                    self.move_to_random_position()

                except pyautogui.FailSafeException:
                    self.stop_movement()
                    print("Emergency stop activated.")
                    break

            time.sleep(self.interval)

    def start_random_movement(self):
        if self.running:
            return

        self.running = True
        self.paused = False

        self.thread = threading.Thread(
            target=self.movement_loop,
            daemon=True
        )

        self.thread.start()

        print("Random mouse movement started.")

    def pause_movement(self):
        self.paused = True
        print("Mouse movement paused.")

    def resume_movement(self):
        if self.running:
            self.paused = False
            print("Mouse movement resumed.")

    def stop_movement(self):
        self.running = False
        self.paused = False
        print("Mouse movement stopped.")
