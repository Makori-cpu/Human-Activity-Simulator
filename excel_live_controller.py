
import threading
import time
import pyautogui

from excel_automation import ExcelAutomation


class ExcelLiveController:

    def __init__(self, on_progress=None, on_status=None):
        self.excel = ExcelAutomation()
        self.on_progress = on_progress
        self.on_status = on_status

        self.records = []
        self.running = False
        self.paused = False
        self.thread = None

        self.typing_delay = 0.08
        self.stop_event = threading.Event()

        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1

    def load_source(self, file_path):
        self.records = self.excel.load_source(file_path)
        return len(self.records)

    def start(self):
        if not self.records:
            raise ValueError("Load a source Excel file first.")

        if self.running:
            return

        self.running = True
        self.paused = False
        self.stop_event.clear()

        self.thread = threading.Thread(
            target=self._typing_loop,
            daemon=True
        )
        self.thread.start()

    def pause(self):
        self.paused = True

    def resume(self):
        if self.running:
            self.paused = False

    def stop(self):
        self.stop_event.set()
        self.running = False
        self.paused = False

    def _typing_loop(self):
        completed = 0

        try:
            if self.on_status:
                self.on_status("Switch to Excel and select the first destination cell. Starting in 5 seconds.")

            time.sleep(5)

            for record in self.records:

                if self.stop_event.is_set():
                    break

                while self.paused and not self.stop_event.is_set():
                    time.sleep(0.1)

                if self.stop_event.is_set():
                    break

                values = [
                    record.get("Name", ""),
                    record.get("Salary", ""),
                    record.get("Department", "")
                ]

                for index, value in enumerate(values):
                    while self.paused and not self.stop_event.is_set():
                        time.sleep(0.1)

                    if self.stop_event.is_set():
                        break

                    pyautogui.write(str(value), interval=self.typing_delay)

                    if index < len(values) - 1:
                        pyautogui.press("tab")

                if self.stop_event.is_set():
                    break

                pyautogui.press("enter")
                pyautogui.press("home")

                completed += 1

                if self.on_progress:
                    self.on_progress(completed, len(self.records))

                time.sleep(0.5)

            if self.on_status:
                self.on_status(
                    "Stopped." if self.stop_event.is_set()
                    else "Excel entry completed."
                )

        except pyautogui.FailSafeException:
            if self.on_status:
                self.on_status("Emergency stop activated.")

        except Exception as error:
            if self.on_status:
                self.on_status(f"Error: {error}")

        finally:
            self.running = False
            self.paused = False
