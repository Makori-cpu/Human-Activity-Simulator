
from mouse_control import MouseController
import time

mouse = MouseController()

print("Mouse test starting in 3 seconds...")
time.sleep(3)

position = mouse.move_to_random_position()

print("Mouse successfully moved!")
print("New position:", position)
