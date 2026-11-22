
import threading
import time
import shutil
import re

from pathlib import Path
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

import pyautogui
import pyperclip
import pygetwindow as gw
from openpyxl import load_workbook

from excel_automation import ExcelAutomation


class ExcelLiveController:

    def __init__(self, on_progress=None, on_status=None):
        self.excel = ExcelAutomation()

        self.on_progress = on_progress
        self.on_status = on_status

        self.records = []
        self.running = False
        self.paused = False

        self.thread = None
        self.stop_event = threading.Event()
        self.plan = None

        self.typing_delay = 0.12
        self.start_delay = 10
        self.backup_path = None

        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.15

    def load_source(self, file_path):
        count = self.excel.load_source(file_path)
        self.records = self.excel.get_data()
        self.plan = None
        return count

    def prepare(self, destination_path):
        self.plan = self.excel.prepare_live_transfer(
            destination_path
        )
        return self.plan

    def start(self, destination_path, plan=None):
        if not self.records:
            raise ValueError("Load a source workbook first.")

        if self.running:
            return

        if plan is None:
            plan = self.prepare(destination_path)

        if (
            Path(destination_path).resolve()
            != Path(plan["destination_path"]).resolve()
        ):
            raise ValueError(
                "The prepared transfer plan does not match "
                "the selected destination."
            )

        # Create a separate backup before entering any data.
        destination = Path(destination_path)
        timestamp = time.strftime("%Y%m%d_%H%M%S")

        self.backup_path = destination.with_name(
            f"{destination.stem}_backup_{timestamp}"
            f"{destination.suffix}"
        )

        shutil.copy2(destination, self.backup_path)

        self.plan = plan
        self.stop_event.clear()
        self.paused = False
        self.running = True

        self.thread = threading.Thread(
            target=self._typing_loop,
            daemon=True
        )
        self.thread.start()

    def pause(self):
        if self.running:
            self.paused = True
            self._status("Automation paused.")

    def resume(self):
        if self.running:
            self.paused = False
            self._status("Automation resumed.")

    def stop(self):
        if self.running:
            self.stop_event.set()
            self.paused = False
            self._status(
                "Stopping after the current safe step..."
            )

    def _status(self, message):
        if self.on_status:
            self.on_status(message)

    def _progress(self, completed, total):
        if self.on_progress:
            self.on_progress(completed, total)

    def _wait_if_paused(self):
        while self.paused and not self.stop_event.is_set():
            time.sleep(0.1)

    def _check_active_workbook(self):
        active_title = gw.getActiveWindowTitle() or ""
        expected_name = Path(
            self.plan["destination_path"]
        ).name

        if expected_name.lower() not in active_title.lower():
            raise RuntimeError(
                "The selected destination workbook is not the "
                "active window.\n\n"
                f"Expected: {expected_name}\n"
                f"Active window: {active_title or 'Unknown'}\n\n"
                "Activate the correct Excel workbook and start again."
            )

    @staticmethod
    def _clipboard_text(value):
        if value is None:
            return ""

        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")

        if isinstance(value, date):
            return value.isoformat()

        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"

        if isinstance(value, str):
            text = value.replace("\r\n", " ")
            text = text.replace("\r", " ")
            text = text.replace("\n", " ")
            text = text.replace("\t", " ")

            # Preserve leading-zero identifiers as text.
            if re.fullmatch(r"0\d+", text):
                return "'" + text

            # Prevent text from being interpreted as a formula.
            if text.startswith(("=", "+", "-", "@")):
                return "'" + text

            return text

        return str(value)

    def _go_to_cell(self, column_letter, row_number):
        sheet_name = self.plan["destination_sheet"]
        safe_sheet_name = sheet_name.replace("'", "''")

        address = (
            f"'{safe_sheet_name}'!"
            f"{column_letter}{row_number}"
        )

        pyautogui.hotkey("ctrl", "g")
        time.sleep(0.35)

        pyperclip.copy(address)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")

        time.sleep(0.25)

    def _enter_value(self, value):
        if value is None or value == "":
            return False

        text = self._clipboard_text(value)

        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")

        time.sleep(self.typing_delay)
        return True

    @staticmethod
    def _values_equal(expected, actual):
        if expected is None or expected == "":
            return actual is None or actual == ""

        if isinstance(expected, datetime):
            if isinstance(actual, datetime):
                return expected == actual
            return str(actual) == expected.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        if isinstance(expected, date):
            if isinstance(actual, datetime):
                return actual.date() == expected
            return (
                actual == expected
                or str(actual) == expected.isoformat()
            )

        if isinstance(expected, bool):
            return actual is expected

        if isinstance(expected, (int, float, Decimal)):
            try:
                return (
                    Decimal(str(expected))
                    == Decimal(str(actual))
                )
            except (InvalidOperation, TypeError):
                return False

        expected_text = str(expected).strip()
        actual_text = (
            "" if actual is None else str(actual).strip()
        )

        if expected_text == actual_text:
            return True

        # Excel can convert numeric-looking text into a number.
        try:
            return (
                Decimal(expected_text)
                == Decimal(actual_text)
            )
        except (InvalidOperation, TypeError):
            return False

    def _verify_entries(
        self,
        destination_path,
        sheet_name,
        start_row,
        matches,
        entered_records
    ):
        workbook = load_workbook(
            destination_path,
            read_only=True,
            data_only=False
        )

        errors = []
        verified = 0

        try:
            if sheet_name not in workbook.sheetnames:
                return 0, [
                    "The destination worksheet was not found."
                ]

            sheet = workbook[sheet_name]

            for record_index, record in enumerate(
                entered_records
            ):
                row_number = start_row + record_index

                for match in matches:
                    source_header = match["source_header"]
                    expected = record.get(source_header)

                    if expected is None or expected == "":
                        continue

                    address = (
                        f"{match['destination_letter']}"
                        f"{row_number}"
                    )

                    actual = sheet[address].value

                    if self._values_equal(expected, actual):
                        verified += 1
                    else:
                        errors.append(
                            f"{address} "
                            f"({match['destination_header']}): "
                            f"expected {expected!r}, "
                            f"found {actual!r}"
                        )

        finally:
            workbook.close()

        return verified, errors

    def _typing_loop(self):
        completed = 0
        entered_records = []
        touched_destination = False
        partial_record = False

        plan = self.plan
        matches = plan["matches"]
        start_row = plan["start_row"]
        total = len(self.records)
        destination_path = plan["destination_path"]

        try:
            self._status(
                f"Backup created: {self.backup_path}. "
                f"Activate {Path(destination_path).name}. "
                f"Starting in {self.start_delay} seconds."
            )

            for remaining in range(self.start_delay, 0, -1):
                if self.stop_event.is_set():
                    break

                self._wait_if_paused()

                if self.stop_event.is_set():
                    break

                self._status(
                    f"Keep the destination Excel workbook "
                    f"in the foreground. Starting in "
                    f"{remaining} seconds..."
                )

                time.sleep(1)

            for record_index, record in enumerate(self.records):
                if self.stop_event.is_set():
                    break

                self._wait_if_paused()

                if self.stop_event.is_set():
                    break

                self._check_active_workbook()

                row_number = start_row + record_index
                record_finished = True

                for match in matches:
                    self._wait_if_paused()

                    if self.stop_event.is_set():
                        record_finished = False
                        break

                    self._check_active_workbook()

                    value = record.get(match["source_header"])

                    self._go_to_cell(
                        match["destination_letter"],
                        row_number
                    )

                    if self._enter_value(value):
                        touched_destination = True

                if not record_finished:
                    partial_record = True
                    break

                completed += 1
                entered_records.append(record.copy())

                self._progress(completed, total)

                self._status(
                    f"Entered record {completed} of {total}."
                )

                time.sleep(0.2)

            # Save only when Excel is still the active destination.
            if touched_destination:
                self._check_active_workbook()

                self._status(
                    "Saving destination workbook..."
                )

                pyautogui.hotkey("ctrl", "s")
                time.sleep(2)

                self._status(
                    "Verifying entered records..."
                )

                verified, errors = self._verify_entries(
                    destination_path,
                    plan["destination_sheet"],
                    start_row,
                    matches,
                    entered_records
                )

                if errors:
                    preview = "; ".join(errors[:8])

                    self._status(
                        f"Verification found {len(errors)} "
                        f"problem(s). {verified} cells verified. "
                        f"Details: {preview}"
                    )

                else:
                    result = (
                        f"{'Stopped' if self.stop_event.is_set() else 'Completed'}: "
                        f"{completed}/{total} records entered. "
                        f"{verified} cells verified. "
                    )

                    if partial_record:
                        result += (
                            "The last row may be partially completed. "
                        )

                    result += (
                        "Unmatched destination headings left blank: "
                        + (
                            ", ".join(
                                plan["unmatched_destination"]
                            )
                            if plan["unmatched_destination"]
                            else "None"
                        )
                        + ". "
                    )

                    result += (
                        "Unused source headings: "
                        + (
                            ", ".join(plan["unmatched_source"])
                            if plan["unmatched_source"]
                            else "None"
                        )
                        + ". "
                    )

                    result += (
                        f"Backup: {self.backup_path}"
                    )

                    self._status(result)

            else:
                self._status(
                    "No destination values were entered."
                )

        except pyautogui.FailSafeException:
            self._status(
                "Emergency stop activated. Check the destination "
                "workbook and save any entries already made."
            )

        except Exception as error:
            self._status(
                f"Excel automation error: {error}"
            )

            if touched_destination:
                self._status(
                    "Some cells may already contain data. "
                    "Check Excel and save manually if necessary. "
                    f"Backup: {self.backup_path}"
                )

        finally:
            self.running = False
            self.paused = False
            self.stop_event.clear()
