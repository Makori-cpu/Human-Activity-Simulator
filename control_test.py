
import tkinter as tk

from mouse_control import MouseController
from keyboard_control import KeyboardController

root = tk.Tk()
root.title("HAS - Control Testing")
root.geometry("750x600")
root.configure(bg="#101820")

tk.Label(
    root,
    text="MOUSE CONTROL TEST",
    font=("Arial", 18, "bold"),
    fg="#00d4aa",
    bg="#101820"
).pack(pady=15)

canvas = tk.Canvas(
    root,
    width=650,
    height=280,
    bg="#17232f",
    highlightthickness=0
)
canvas.pack(pady=10)

mouse = MouseController(canvas)

tk.Label(
    root,
    text="KEYBOARD CONTROL TEST",
    font=("Arial", 15, "bold"),
    fg="white",
    bg="#101820"
).pack(pady=10)

entry = tk.Entry(root, width=55, font=("Arial", 12))
entry.pack(pady=10)

keyboard = KeyboardController(entry)

def move_test():
    mouse.move_pointer(200, 120)

def click_test():
    mouse.click_position(350, 150)

def type_test():
    keyboard.type_text(
        "Human Activity Simulator is working!"
    )

def clear_test():
    keyboard.clear_text()

buttons = tk.Frame(root, bg="#101820")
buttons.pack(pady=15)

tk.Button(
    buttons, text="MOVE POINTER",
    command=move_test
).pack(side="left", padx=5)

tk.Button(
    buttons, text="TEST CLICK",
    command=click_test
).pack(side="left", padx=5)

tk.Button(
    buttons, text="TYPE TEXT",
    command=type_test
).pack(side="left", padx=5)

tk.Button(
    buttons, text="CLEAR",
    command=clear_test
).pack(side="left", padx=5)

root.mainloop()
