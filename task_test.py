
from task_manager import TaskManager

manager = TaskManager()

manager.add_task("Test mouse controller")
manager.add_task("Test keyboard controller")
manager.add_task("Check activity history")

print("\nAll Tasks:")

for task in manager.get_tasks():
    print(task)

manager.complete_task(1)

print("\nAfter Completing Task 1:")

for task in manager.get_tasks():
    print(task)
