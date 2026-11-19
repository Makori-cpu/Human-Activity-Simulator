
import json
from pathlib import Path


class TaskManager:

    def __init__(self):
        self.file_path = Path(__file__).parent / "tasks.json"
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if self.file_path.exists():
            try:
                with open(self.file_path, "r", encoding="utf-8") as file:
                    self.tasks = json.load(file)
            except (json.JSONDecodeError, OSError):
                self.tasks = []

    def save_tasks(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, title):
        if not title.strip():
            return False

        task = {
            "id": len(self.tasks) + 1,
            "title": title.strip(),
            "completed": False
        }

        self.tasks.append(task)
        self.save_tasks()
        return True

    def get_tasks(self):
        return self.tasks

    def complete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_tasks()
                return True

        return False

    def delete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                return True

        return False
