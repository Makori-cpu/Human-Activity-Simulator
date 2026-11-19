
import pyautogui
import time
import random
from excel_automation import ExcelAutomation


class ExcelLiveTyper:

    def __init__(self):
        self.excel = ExcelAutomation()
        self.typing_delay = 0.08

    def load_data(self, file_path):
        records = self.excel.load_source(file_path)
        print(f"Loaded {len(records)} records.")
        return records

    def type_records(self, records):
        print("Starting Excel data entry in 5 seconds...")
        print("Make sure Excel is open and cell A2 is selected.")

        time.sleep(5)

        for record in records:

            values = [
                record.get("Name", ""),
                record.get("Salary", ""),
                record.get("Department", "")
            ]

            for value in values:
                pyautogui.write(str(value), interval=self.typing_delay)
                pyautogui.press("tab")

            pyautogui.press("enter")

            time.sleep(random.uniform(0.5, 1.2))

        print("Excel data entry completed!")


if __name__ == "__main__":

    typer = ExcelLiveTyper()

    records = typer.load_data("source_data.xlsx")

    typer.type_records(records)
