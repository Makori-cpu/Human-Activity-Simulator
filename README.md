# Human Activity Simulator

## Project Overview

Human Activity Simulator is a Python-based desktop application designed to simulate and automate selected computer activities through a graphical user interface. The application combines mouse and keyboard automation, activity logging, task management, configurable settings, and Excel data automation in one centralized platform.

Built with Python and Tkinter, the system provides users with an interactive dashboard for controlling automation tasks, monitoring activity sessions, and managing Excel workbook operations.

## Key Features

- **Mouse Automation:** Simulates mouse movements across the computer screen.
- **Keyboard Automation:** Provides keyboard control functionality.
- **Activity Logging:** Records and maintains a history of application activities.
- **Task Management:** Organizes and manages configured automation tasks.
- **Session Controls:** Provides controls for starting, pausing, and stopping activities.
- **Settings Management:** Stores and manages application configurations.
- **Excel Automation:** Automates operations involving Excel workbooks.
- **Live Excel Interaction:** Supports automated interaction with Excel during active sessions.
- **Graphical Dashboard:** Provides a centralized interface for accessing and managing application features.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Tkinter | Desktop graphical user interface |
| PyAutoGUI | Mouse and keyboard automation |
| OpenPyXL | Excel workbook processing |
| JSON | Activity history, settings, and task storage |
| Threading | Background automation processes |

## Project Structure

- `main.py` – Application entry point.
- `dashboard.py` – Main graphical dashboard.
- `mouse_control.py` – Mouse automation functionality.
- `keyboard_control.py` – Keyboard control functionality.
- `activity_logger.py` – Activity logging.
- `task_manager.py` – Task management.
- `settings_manager.py` – Application settings.
- `excel_automation.py` – Excel workbook automation.
- `excel_live_controller.py` – Live Excel automation controller.

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Makori-cpu/Human-Activity-Simulator.git
   ```

2. Navigate into the project directory:

   ```bash
   cd Human-Activity-Simulator
   ```

3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   **Windows PowerShell**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

5. Install the required dependencies:

   ```bash
   pip install pyautogui openpyxl
   ```

6. Run the application:

   ```bash
   python main.py
   ```

## Project Goal

The goal of Human Activity Simulator is to bring multiple desktop automation capabilities into a single Python application, reducing repetitive manual operations and providing a structured environment for managing computer-based tasks.

## Future Improvements

- Enhanced automation scheduling.
- More configurable mouse and keyboard actions.
- Improved activity analytics and reporting.
- Expanded Excel automation capabilities.
- Enhanced dashboard design and user experience.

---

**Developed with Python | Desktop Automation | Excel Automation**
