
print("Starting Human Activity Simulator...")

import tkinter as tk

print("Tkinter imported successfully!")

from dashboard import HumanActivitySimulator

print("Dashboard imported successfully!")

root = tk.Tk()
print("Window created successfully!")

app = HumanActivitySimulator(root)

print("Dashboard initialized!")

root.mainloop()

print("Application closed.")

