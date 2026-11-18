
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class HumanActivitySimulator:

    def __init__(self, root):
        self.root = root
        self.running = False
        self.paused = False

        self.root.title("Human Activity Simulator")
        self.root.geometry("1050x700")
        self.root.configure(bg="#101820")

        self.create_sidebar()
        self.create_dashboard()

    def create_sidebar(self):
        sidebar = tk.Frame(
            self.root,
            bg="#17232f",
            width=220
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="HAS",
            font=("Arial", 28, "bold"),
            fg="#00d4aa",
            bg="#17232f"
        ).pack(pady=30)

        sections = [
            "Dashboard",
            "Mouse Control",
            "Keyboard Control",
            "Task Manager",
            "Activity Logs",
            "Settings"
        ]

        for section in sections:
            tk.Button(
                sidebar,
                text=section,
                font=("Arial", 11),
                bg="#17232f",
                fg="white",
                relief="flat",
                anchor="w",
                padx=20
            ).pack(fill="x", ipady=12)

    def create_dashboard(self):
        content = tk.Frame(
            self.root,
            bg="#101820"
        )
        content.pack(
            side="left",
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

        tk.Label(
            content,
            text="Human Activity Simulator",
            font=("Arial", 23, "bold"),
            fg="white",
            bg="#101820"
        ).pack(anchor="w")

        tk.Label(
            content,
            text="Desktop automation control center",
            font=("Arial", 11),
            fg="#9baab7",
            bg="#101820"
        ).pack(anchor="w", pady=8)

        status_frame = tk.Frame(
            content,
            bg="#17232f",
            padx=20,
            pady=20
        )
        status_frame.pack(fill="x", pady=20)

        tk.Label(
            status_frame,
            text="AUTOMATION STATUS",
            fg="#9baab7",
            bg="#17232f"
        ).pack(anchor="w")

        self.status_label = tk.Label(
            status_frame,
            text="READY",
            font=("Arial", 24, "bold"),
            fg="#00d4aa",
            bg="#17232f"
        )
        self.status_label.pack(anchor="w", pady=10)

        controls = tk.Frame(
            content,
            bg="#101820"
        )
        controls.pack(anchor="w", pady=10)

        tk.Button(
            controls,
            text="START",
            width=12,
            bg="#00d4aa",
            command=self.start_simulation
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="PAUSE",
            width=12,
            bg="#f0b429",
            command=self.pause_simulation
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="STOP",
            width=12,
            bg="#e05252",
            fg="white",
            command=self.stop_simulation
        ).pack(side="left", padx=5)

        tk.Label(
            content,
            text="ACTIVITY LOG",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#101820"
        ).pack(anchor="w", pady=15)

        self.log_box = tk.Text(
            content,
            height=15,
            bg="#17232f",
            fg="#00d4aa",
            font=("Consolas", 10),
            relief="flat"
        )
        self.log_box.pack(fill="both", expand=True)

        self.log("Application initialized successfully.")

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")

        self.log_box.insert(
            tk.END,
            f"[{timestamp}] {message}\n"
        )

        self.log_box.see(tk.END)

    def start_simulation(self):
        if self.running and not self.paused:
            self.log("Automation is already running.")
            return

        self.running = True
        self.paused = False

        self.status_label.config(
            text="RUNNING",
            fg="#00d4aa"
        )

        self.log("Automation session started.")

    def pause_simulation(self):
        if not self.running or self.paused:
            self.log("No active session to pause.")
            return

        self.paused = True

        self.status_label.config(
            text="PAUSED",
            fg="#f0b429"
        )

        self.log("Automation session paused.")

    def stop_simulation(self):
        if not self.running:
            self.log("No active session.")
            return

        self.running = False
        self.paused = False

        self.status_label.config(
            text="STOPPED",
            fg="#e05252"
        )

        self.log("Automation session stopped.")
