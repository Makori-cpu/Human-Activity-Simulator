
from openpyxl import load_workbook, Workbook
from pathlib import Path


class ExcelAutomation:

    def __init__(self):
        self.source_file = None
        self.template_file = None
        self.data = []

    def load_source(self, file_path):
        """Read records from a source Excel workbook."""

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError("Source Excel file not found.")

        workbook = load_workbook(file_path, data_only=True)
        sheet = workbook.active

        headers = [
            cell.value for cell in sheet[1]
        ]

        if not headers or all(header is None for header in headers):
            raise ValueError("The source spreadsheet has no headers.")

        self.data = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if all(value is None for value in row):
                continue

            record = {
                headers[index]: value
                for index, value in enumerate(row[:len(headers)])
                if headers[index] is not None
            }

            self.data.append(record)

        self.source_file = file_path

        workbook.close()

        return self.data

    def fill_template(self, template_path, output_path):
        """Transfer matching columns into a separate Excel workbook."""

        if not self.data:
            raise ValueError("Load source data before filling the template.")

        template_path = Path(template_path)
        output_path = Path(output_path)

        if not template_path.exists():
            raise FileNotFoundError("Template Excel file not found.")

        if template_path.resolve() == output_path.resolve():
            raise ValueError("Output must be a separate file.")

        workbook = load_workbook(template_path)
        sheet = workbook.active

        template_headers = [
            cell.value for cell in sheet[1]
        ]

        if not template_headers or all(
            header is None for header in template_headers
        ):
            raise ValueError("The template has no column headers.")

        completed = 0

        for record in self.data:
            next_row = sheet.max_row + 1

            for column_number, header in enumerate(
                template_headers, start=1
            ):
                if header is not None:
                    sheet.cell(
                        row=next_row,
                        column=column_number
                    ).value = record.get(header)

            completed += 1

        output_path.parent.mkdir(parents=True, exist_ok=True)

        workbook.save(output_path)
        workbook.close()

        return completed

    def get_record_count(self):
        return len(self.data)

    def get_data(self):
        return self.data
