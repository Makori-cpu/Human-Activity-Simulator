
import json
from datetime import datetime
from pathlib import Path


class ActivityLogger:

    def __init__(self):
        self.file_path = Path(__file__).parent / "activity_history.json"
        self.activities = []
        self.load_activities()

    def load_activities(self):
        """Load previously saved activities."""
        if self.file_path.exists():
            try:
                with open(self.file_path, "r", encoding="utf-8") as file:
                    self.activities = json.load(file)
            except (json.JSONDecodeError, OSError):
                self.activities = []

    def save_activities(self):
        """Save activities permanently to JSON."""
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.activities, file, indent=4)

    def log_activity(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        activity = {
            "time": timestamp,
            "message": message
        }

        self.activities.append(activity)
        self.save_activities()

        print(f"[{timestamp}] {message}")

    def get_activities(self):
        return self.activities

    def clear_activities(self):
        self.activities.clear()
        self.save_activities()
