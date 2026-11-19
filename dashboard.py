from datetime import datetime
import tkinter as tk
from activity_logger import ActivityLogger
from keyboard_control import KeyboardController
from mouse_control import MouseController
from task_manager import TaskManager
from settings_manager import SettingsManager
from tkinter import filedialog, messagebox
from excel_live_controller import ExcelLiveController


class HumanActivitySimulator:
    def __init__(self, root):
        self.logger = ActivityLogger()
        self.task_manager = TaskManager()
        self.settings_manager = SettingsManager()
        self.excel_controller = ExcelLiveController(
            on_progress=self.update_excel_progress,
            on_status=self.update_excel_status,
        )
        self.excel_source_path = None
        self.root = root
        self.running = False
        self.paused = False

        self.root.title("Human Activity Simulator")
        self.root.geometry("1100x750")
        self.root.configure(bg="#101820")

        self.create_sidebar()
        self.create_dashboard()

    def create_sidebar(self):
        sidebar = tk.Frame(self.root, bg="#17232f", width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="HAS",
            font=("Arial", 28, "bold"),
            fg="#00d4aa",
            bg="#17232f",
        ).pack(pady=30)

        sections = [
            "Dashboard",
            "Mouse Control",
            "Keyboard Control",
            "Task Manager",
            "Excel Automation",
            "Activity Logs",
            "Settings",
        ]
        for section in sections:
            if section == "Task Manager":
                action = self.open_task_manager
            elif section == "Settings":
                action = self.open_settings
            elif section == "Excel Automation":
                action = self.open_excel_automation
            else:
                action = lambda s=section: self.log(f"{s} selected.")

            tk.Button(
                sidebar,
                text=section,
                font=("Arial", 11),
                bg="#17232f",
                fg="white",
                relief="flat",
                anchor="w",
                padx=20,
                command=action,
            ).pack(fill="x", ipady=12)


    def create_dashboard(self):
        content = tk.Frame(self.root, bg="#101820")
        content.pack(
            side="left",
            fill="both",
            expand=True,
            padx=25,
            pady=20,
        )

        tk.Label(
            content,
            text="Human Activity Simulator",
            font=("Arial", 23, "bold"),
            fg="white",
            bg="#101820",
        ).pack(anchor="w")

        tk.Label(
            content,
            text="Desktop automation control center",
            font=("Arial", 11),
            fg="#9baab7",
            bg="#101820",
        ).pack(anchor="w", pady=5)

        status = tk.Frame(content, bg="#17232f", padx=15, pady=12)
        status.pack(fill="x", pady=12)

        tk.Label(
            status,
            text="AUTOMATION STATUS",
            fg="#9baab7",
            bg="#17232f",
        ).pack(anchor="w")

        self.status_label = tk.Label(
            status,
            text="READY",
            font=("Arial", 20, "bold"),
            fg="#00d4aa",
            bg="#17232f",
        )
        self.status_label.pack(anchor="w")

        controls = tk.Frame(content, bg="#101820")
        controls.pack(anchor="w", pady=8)

        tk.Button(
            controls,
            text="START",
            width=12,
            bg="#00d4aa",
            command=self.start_session,
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="PAUSE",
            width=12,
            bg="#f0b429",
            command=self.pause_session,
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="STOP",
            width=12,
            bg="#e05252",
            fg="white",
            command=self.stop_session,
        ).pack(side="left", padx=5)

        tk.Label(
            content,
            text="MOUSE CONTROL",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#101820",
        ).pack(anchor="w", pady=(12, 5))

        self.canvas = tk.Canvas(
            content,
            height=145,
            bg="#17232f",
            highlightthickness=0,
        )
        self.canvas.pack(fill="x")
        self.mouse = MouseController()

        
        mouse_buttons = tk.Frame(content, bg="#101820")
        mouse_buttons.pack(anchor="w", pady=7)

        tk.Button(
            mouse_buttons,
            text="START RANDOM MOVEMENT",
            command=self.mouse.start_random_movement,
        ).pack(side="left", padx=5)

        tk.Button(
            mouse_buttons,
            text="PAUSE",
            command=self.mouse.pause_movement,
        ).pack(side="left", padx=5)

        tk.Button(
            mouse_buttons,
            text="RESUME",
            command=self.mouse.resume_movement,
        ).pack(side="left", padx=5)

        tk.Button(
            mouse_buttons,
            text="STOP",
            command=self.mouse.stop_movement,
        ).pack(side="left", padx=5)


        self.text_entry = tk.Entry(content, font=("Arial", 12))
        self.text_entry.pack(fill="x", pady=5)
        self.keyboard = KeyboardController(self.text_entry)

        keyboard_buttons = tk.Frame(content, bg="#101820")
        keyboard_buttons.pack(anchor="w", pady=5)

        tk.Button(
            keyboard_buttons,
            text="TYPE TEST TEXT",
            command=self.test_keyboard,
        ).pack(side="left", padx=5)

        tk.Button(
            keyboard_buttons,
            text="CLEAR TEXT",
            command=self.clear_keyboard,
        ).pack(side="left", padx=5)

        tk.Label(
            content,
            text="ACTIVITY LOG",
            font=("Arial", 13, "bold"),
            fg="white",
            bg="#101820",
        ).pack(anchor="w", pady=(10, 5))

        self.log_box = tk.Text(
            content,
            height=5,
            bg="#17232f",
            fg="#00d4aa",
            font=("Consolas", 9),
            relief="flat",
        )
        self.log_box.pack(fill="both", expand=True)

        tk.Button(
            content,
            text="VIEW ACTIVITY HISTORY",
            bg="#00d4aa",
            fg="#101820",
            font=("Arial", 10, "bold"),
            command=self.view_activity_history,
        ).pack(anchor="w", pady=8)

        self.log("HAS initialized successfully.")
        self.log("Mouse and keyboard test modules connected.")

    def log(self, message):
        if hasattr(self, "log_box"):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.log_box.insert(tk.END, f"[{timestamp}] {message}\n")
            self.log_box.see(tk.END)

    def start_session(self):
        if self.running and not self.paused:
            self.log("Session is already running.")
            return

        self.running = True
        self.paused = False
        self.status_label.config(text="RUNNING", fg="#00d4aa")
        self.log("Test session started.")
        self.logger.log_activity("Test session started.")

    def pause_session(self):
        if not self.running or self.paused:
            self.log("No active session to pause.")
            return

        self.paused = True
        self.status_label.config(text="PAUSED", fg="#f0b429")
        self.log("Test session paused.")
        self.logger.log_activity("Test session paused.")

    def stop_session(self):
        if not self.running:
            self.log("No active session.")
            return

        self.running = False
        self.paused = False
        self.status_label.config(text="STOPPED", fg="#e05252")
        self.log("Test session stopped.")
        self.logger.log_activity("Test session stopped.")

   
    def test_mouse_move(self):
        position = self.mouse.move_to_random_position()
        self.log(f"Windows mouse moved to {position}.")

    def test_mouse_click(self):
        self.mouse.click_at_current_position()
        self.log("Windows mouse clicked at its current position.")


    def test_keyboard(self):
        self.keyboard.type_text(
            "Human Activity Simulator is working!"
        )
        self.log("Test text entered.")

    def clear_keyboard(self):
        self.keyboard.clear_text()
        self.log("Test field cleared.")

    def view_activity_history(self):
        activities = self.logger.get_activities()
        self.log_box.insert(tk.END, "\n--- ACTIVITY HISTORY ---\n")

        if not activities:
            self.log_box.insert(tk.END, "No recorded activities.\n")
        else:
            for activity in activities:
                self.log_box.insert(
                    tk.END,
                    f"[{activity['time']}] {activity['message']}\n",
                )

        self.log_box.see(tk.END)

    def open_task_manager(self):
        task_window = tk.Toplevel(self.root)
        task_window.title("HAS - Task Manager")
        task_window.geometry("650x500")
        task_window.configure(bg="#101820")

        tk.Label(
            task_window,
            text="TASK MANAGER",
            font=("Arial", 20, "bold"),
            fg="#00d4aa",
            bg="#101820",
        ).pack(pady=15)

        task_entry = tk.Entry(task_window, font=("Arial", 12), width=40)
        task_entry.pack(pady=10)

        task_list = tk.Listbox(
            task_window,
            font=("Arial", 11),
            bg="#17232f",
            fg="white",
            selectbackground="#00d4aa",
            height=12,
            width=65,
        )
        task_list.pack(pady=10, padx=15)

        def refresh_tasks():
            task_list.delete(0, tk.END)
            for task in self.task_manager.get_tasks():
                status = "COMPLETED" if task["completed"] else "PENDING"
                task_list.insert(
                    tk.END,
                    f'{task["id"]}. {task["title"]} - {status}',
                )

        def add_task():
            title = task_entry.get()
            if self.task_manager.add_task(title):
                clean_title = title.strip()
                self.logger.log_activity(f"Task added: {clean_title}")
                task_entry.delete(0, tk.END)
                refresh_tasks()
                self.log(f"Task added: {clean_title}")
            else:
                self.log("Please enter a task title.")

        def complete_task():
            selection = task_list.curselection()
            if not selection:
                self.log("Select a task first.")
                return

            task = self.task_manager.get_tasks()[selection[0]]
            if self.task_manager.complete_task(task["id"]):
                self.logger.log_activity(
                    f"Task completed: {task['title']}"
                )
                refresh_tasks()

        def delete_task():
            selection = task_list.curselection()
            if not selection:
                self.log("Select a task first.")
                return

            task = self.task_manager.get_tasks()[selection[0]]
            if self.task_manager.delete_task(task["id"]):
                self.logger.log_activity(
                    f"Task deleted: {task['title']}"
                )
                refresh_tasks()

        buttons = tk.Frame(task_window, bg="#101820")
        buttons.pack(pady=10)

        tk.Button(
            buttons,
            text="ADD TASK",
            bg="#00d4aa",
            command=add_task,
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="COMPLETE TASK",
            bg="#f0b429",
            command=complete_task,
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="DELETE TASK",
            bg="#e05252",
            fg="white",
            command=delete_task,
        ).pack(side="left", padx=5)

        refresh_tasks()


    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("450x450")
        settings_window.configure(bg="#f4f4f4")

        tk.Label(
            settings_window,
            text="Application Settings",
            font=("Arial", 18, "bold"),
            bg="#f4f4f4"
        ).pack(pady=20)

        settings = self.settings_manager.get_all_settings()

        # Session duration
        tk.Label(
            settings_window,
            text="Session Duration (minutes)",
            bg="#f4f4f4"
        ).pack()

        session_entry = tk.Entry(settings_window)
        session_entry.insert(0, str(settings["session_duration"]))
        session_entry.pack(pady=5)

        # Mouse speed
        tk.Label(
            settings_window,
            text="Mouse Movement Speed",
            bg="#f4f4f4"
        ).pack()

        mouse_entry = tk.Entry(settings_window)
        mouse_entry.insert(0, str(settings["mouse_speed"]))
        mouse_entry.pack(pady=5)

        # Typing speed
        tk.Label(
            settings_window,
            text="Keyboard Typing Speed",
            bg="#f4f4f4"
        ).pack()

        typing_entry = tk.Entry(settings_window)
        typing_entry.insert(0, str(settings["typing_speed"]))
        typing_entry.pack(pady=5)

        # Activity logging
        log_var = tk.BooleanVar(
            value=settings["log_activities"]
        )

        tk.Checkbutton(
            settings_window,
            text="Enable Activity Logging",
            variable=log_var,
            bg="#f4f4f4"
        ).pack(pady=15)

        def save_settings():
            try:
                session_duration = int(session_entry.get())
                mouse_speed = int(mouse_entry.get())
                typing_speed = int(typing_entry.get())

                if session_duration <= 0:
                    raise ValueError

                if not 1 <= mouse_speed <= 10:
                    raise ValueError

                if not 1 <= typing_speed <= 10:
                    raise ValueError

                self.settings_manager.update_setting(
                    "session_duration", session_duration
                )

                self.settings_manager.update_setting(
                    "mouse_speed", mouse_speed
                )

                self.settings_manager.update_setting(
                    "typing_speed", typing_speed
                )

                self.settings_manager.update_setting(
                    "log_activities", log_var.get()
                )

                tk.messagebox.showinfo(
                    "Success",
                    "Settings saved successfully!"
                )

                settings_window.destroy()

            except ValueError:
                tk.messagebox.showerror(
                    "Invalid Input",
                    "Enter valid numbers. Session duration must be positive, and speeds must be between 1 and 10."
                )

        tk.Button(
            settings_window,
            text="Save Settings",
            command=save_settings,
            bg="#2e8b57",
            fg="white",
            width=20
        ).pack(pady=15)

    def open_excel_automation(self):

        window = tk.Toplevel(self.root)
        window.title("Excel Automation")
        window.geometry("550x400")
        window.configure(bg="#101820")

        self.excel_status_label = tk.Label(
            window,
            text="Select a source workbook.",
            fg="white",
            bg="#101820"
        )
        self.excel_status_label.pack(pady=10)

        self.excel_progress_label = tk.Label(
            window,
            text="Records completed: 0 / 0",
            fg="white",
            bg="#101820"
        )
        self.excel_progress_label.pack(pady=10)

        tk.Button(
            window,
            text="SELECT SOURCE EXCEL FILE",
            command=self.select_excel_source
        ).pack(pady=8)

        controls = tk.Frame(window, bg="#101820")
        controls.pack(pady=15)

        tk.Button(controls, text="START",
                  command=self.start_excel_typing).pack(side="left", padx=5)

        tk.Button(controls, text="PAUSE",
                  command=self.excel_controller.pause).pack(side="left", padx=5)

        tk.Button(controls, text="RESUME",
                  command=self.excel_controller.resume).pack(side="left", padx=5)

        tk.Button(controls, text="STOP",
                  command=self.excel_controller.stop).pack(side="left", padx=5)


    def select_excel_source(self):

        file_path = filedialog.askopenfilename(
            title="Select source Excel workbook",
            filetypes=[("Excel files", "*.xlsx")]
        )

        if not file_path:
            return

        try:
            count = self.excel_controller.load_source(file_path)
            self.excel_source_path = file_path

            self.excel_status_label.config(
                text=f"Loaded {count} records."
            )

            self.excel_progress_label.config(
                text=f"Records completed: 0 / {count}"
            )

            messagebox.showinfo(
                "Success",
                f"Loaded {count} records successfully."
            )

        except Exception as error:
            messagebox.showerror("Excel Error", str(error))


    def start_excel_typing(self):

        if not self.excel_source_path:
            messagebox.showwarning(
                "Missing file",
                "Select a source workbook first."
            )
            return

        if self.excel_controller.running:
            return

        self.excel_controller.start()


    def update_excel_progress(self, completed, total):

        self.root.after(
            0,
            lambda: self.excel_progress_label.config(
                text=f"Records completed: {completed} / {total}"
            )
        )


    def update_excel_status(self, status):

        self.root.after(
            0,
            lambda: self.excel_status_label.config(text=status)
        )




if __name__ == "__main__":
    root = tk.Tk()
    app = HumanActivitySimulator(root)
    root.mainloop()
