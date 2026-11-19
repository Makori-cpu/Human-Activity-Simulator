
import json
from pathlib import Path


class SettingsManager:
    def __init__(self):
        self.file_path = Path(__file__).parent / "settings.json"

        self.default_settings = {
            "session_duration": 30,
            "mouse_speed": 5,
            "typing_speed": 3,
            "log_activities": True
        }

        self.settings = self.load_settings()

    def load_settings(self):
        if self.file_path.exists():
            try:
                with open(self.file_path, "r", encoding="utf-8") as file:
                    saved_settings = json.load(file)

                return {**self.default_settings, **saved_settings}

            except (json.JSONDecodeError, OSError):
                return self.default_settings.copy()

        return self.default_settings.copy()

    def save_settings(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.settings, file, indent=4)

    def get_setting(self, key):
        return self.settings.get(key)

    def update_setting(self, key, value):
        if key not in self.default_settings:
            return False

        self.settings[key] = value
        self.save_settings()
        return True

    def get_all_settings(self):
        return self.settings
