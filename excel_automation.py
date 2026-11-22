
from pathlib import Path
from difflib import SequenceMatcher
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import re


class ExcelAutomation:

    HEADER_ALIASES = {
        "name": {
            "name", "full name", "employee name", "staff name",
            "worker name", "person name"
        },
        "salary": {
            "salary", "monthly salary", "basic salary", "pay",
            "monthly pay", "gross pay", "gross salary",
            "gross monthly remuneration", "monthly remuneration",
            "base pay", "wage", "compensation", "earnings"
        },
        "department": {
            "department", "dept", "division", "business unit",
            "section", "team"
        },
        "employee id": {
            "employee id", "staff id", "worker id", "id",
            "employee number", "staff number", "personnel number"
        },
        "email": {
            "email", "email address", "e-mail", "work email"
        },
        "phone": {
            "phone", "phone number", "mobile", "mobile number",
            "telephone", "contact number"
        },
        "date of birth": {
            "date of birth", "dob", "birth date"
        },
        "job title": {
            "job title", "position", "role", "designation"
        },
        "address": {
            "address", "home address", "residential address"
        },
    }

    def __init__(self):
        self.source_file = None
        self.source_headers = []
        self.data = []

    @staticmethod
    def clean_header(header):
        if header is None:
            return ""

        text = str(header).strip().lower()
        text = re.sub(r"[_\-./]+", " ", text)
        text = re.sub(r"[^a-z0-9 ]+", "", text)
        return " ".join(text.split())

    def normalize_header(self, header):
        cleaned = self.clean_header(header)

        if not cleaned:
            return ""

        for canonical, aliases in self.HEADER_ALIASES.items():
            all_names = {canonical}
            all_names.update(aliases)

            if cleaned in {
                self.clean_header(name) for name in all_names
            }:
                return canonical

        return cleaned

    def load_source(self, file_path):
        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(
                f"Source workbook not found: {path}"
            )

        workbook = load_workbook(
            path,
            data_only=True,
            read_only=True
        )

        try:
            sheet = workbook.active

            headers = next(
                sheet.iter_rows(
                    min_row=1,
                    max_row=1,
                    values_only=True
                ),
                ()
            )

            if not headers or all(
                h is None or str(h).strip() == ""
                for h in headers
            ):
                raise ValueError(
                    "The source workbook has no headings in row 1."
                )

            cleaned_headers = []
            seen = set()

            for header in headers:
                value = (
                    str(header).strip()
                    if header is not None else None
                )

                if value:
                    normalized = self.normalize_header(value)

                    if normalized in seen:
                        raise ValueError(
                            "Duplicate or equivalent source heading: "
                            f"{value}"
                        )

                    seen.add(normalized)

                cleaned_headers.append(value)

            records = []

            for row in sheet.iter_rows(
                min_row=2,
                values_only=True
            ):
                if all(value is None for value in row):
                    continue

                record = {}

                for index, header in enumerate(cleaned_headers):
                    if header and index < len(row):
                        record[header] = row[index]

                records.append(record)

            self.source_file = path
            self.source_headers = cleaned_headers
            self.data = records

        finally:
            workbook.close()

        return len(self.data)

    def match_headers(self, destination_headers):
        source_map = {}

        for header in self.source_headers:
            if header:
                normalized = self.normalize_header(header)
                source_map.setdefault(normalized, []).append(header)

        matches = []
        unmatched_destination = []
        ambiguous = []
        used_source = set()

        for column_number, raw_header in enumerate(
            destination_headers,
            start=1
        ):
            if raw_header is None:
                continue

            destination_header = str(raw_header).strip()

            if not destination_header:
                continue

            normalized = self.normalize_header(destination_header)
            candidates = source_map.get(normalized, [])

            if len(candidates) == 1:
                source_header = candidates[0]

                if source_header in used_source:
                    ambiguous.append({
                        "destination": destination_header,
                        "candidates": [source_header],
                        "reason": "Source heading already matched."
                    })
                    continue

                matches.append({
                    "source_header": source_header,
                    "destination_header": destination_header,
                    "destination_column": column_number,
                    "destination_letter": get_column_letter(
                        column_number
                    ),
                    "match_type": "exact or synonym",
                    "confidence": 1.0
                })

                used_source.add(source_header)
                continue

            if len(candidates) > 1:
                ambiguous.append({
                    "destination": destination_header,
                    "candidates": candidates,
                    "reason": "Multiple equivalent source headings."
                })
                continue

            # Fuzzy matching for small spelling differences.
            scored = []

            for source_header in self.source_headers:
                if not source_header or source_header in used_source:
                    continue

                source_normalized = self.normalize_header(
                    source_header
                )

                score = SequenceMatcher(
                    None,
                    normalized,
                    source_normalized
                ).ratio()

                scored.append((score, source_header))

            scored.sort(reverse=True)

            if scored and scored[0][0] >= 0.88:
                best_score, best_header = scored[0]

                second_score = (
                    scored[1][0] if len(scored) > 1 else 0
                )

                if best_score - second_score < 0.08:
                    ambiguous.append({
                        "destination": destination_header,
                        "candidates": [
                            item[1] for item in scored
                            if best_score - item[0] < 0.08
                        ],
                        "reason": "Several headings are similarly close."
                    })
                    continue

                matches.append({
                    "source_header": best_header,
                    "destination_header": destination_header,
                    "destination_column": column_number,
                    "destination_letter": get_column_letter(
                        column_number
                    ),
                    "match_type": "fuzzy",
                    "confidence": round(best_score, 3)
                })

                used_source.add(best_header)

            else:
                unmatched_destination.append(destination_header)

        unmatched_source = [
            header for header in self.source_headers
            if header and header not in used_source
        ]

        return (
            matches,
            unmatched_destination,
            unmatched_source,
            ambiguous
        )

    def prepare_live_transfer(self, destination_path):
        if not self.data:
            raise ValueError("Load a source workbook first.")

        destination = Path(destination_path)

        if not destination.is_file():
            raise FileNotFoundError(
                "Destination Excel workbook not found."
            )

        if (
            self.source_file
            and self.source_file.resolve() == destination.resolve()
        ):
            raise ValueError(
                "Source and destination must be different workbooks."
            )

        workbook = load_workbook(
            destination,
            read_only=True,
            data_only=True
        )

        try:
            sheet = workbook.active

            destination_headers = next(
                sheet.iter_rows(
                    min_row=1,
                    max_row=1,
                    values_only=True
                ),
                ()
            )

            if not destination_headers or all(
                h is None or str(h).strip() == ""
                for h in destination_headers
            ):
                raise ValueError(
                    "Destination headings must be in row 1."
                )

            (
                matches,
                unmatched_destination,
                unmatched_source,
                ambiguous
            ) = self.match_headers(destination_headers)

            if ambiguous:
                details = "\n".join(
                    f"{item['destination']}: "
                    f"{', '.join(item['candidates'])}"
                    for item in ambiguous
                )

                raise ValueError(
                    "Ambiguous column headings detected. "
                    "No data has been entered.\n\n" + details
                )

            if not matches:
                raise ValueError(
                    "No matching headings were found. "
                    "No data has been entered."
                )

            destination_columns = [
                index
                for index, header in enumerate(
                    destination_headers,
                    start=1
                )
                if header is not None and str(header).strip()
            ]

            last_data_row = 1

            for row_number, row in enumerate(
                sheet.iter_rows(
                    min_row=2,
                    max_col=max(destination_columns),
                    values_only=True
                ),
                start=2
            ):
                if any(
                    row[column - 1] is not None
                    and row[column - 1] != ""
                    for column in destination_columns
                    if column - 1 < len(row)
                ):
                    last_data_row = row_number

            return {
                "matches": matches,
                "unmatched_destination": unmatched_destination,
                "unmatched_source": unmatched_source,
                "ambiguous": ambiguous,
                "start_row": last_data_row + 1,
                "total_records": len(self.data),
                "destination_sheet": sheet.title,
                "destination_path": str(destination.resolve())
            }

        finally:
            workbook.close()

    def get_record_count(self):
        return len(self.data)

    def get_data(self):
        return self.data
    
    def write_to_destination(self, destination_path, progress_callback=None):
        """
        Write matched source records into the destination Excel workbook.
        Existing destination records are preserved.
        """

        from openpyxl import load_workbook

        if not self.data:
            raise ValueError("No source data loaded. Load the source workbook first.")

        # Get the existing column matches and next available row.
        transfer = self.prepare_live_transfer(destination_path)

        matches = transfer["matches"]
        start_row = transfer["start_row"]
        total_records = len(self.data)

        workbook = load_workbook(destination_path)

        try:
            sheet = workbook[transfer["destination_sheet"]]

            # Write every source record into its matched destination column.
            for record_index, record in enumerate(self.data):

                destination_row = start_row + record_index

                for match in matches:
                    source_header = match["source_header"]
                    destination_column = match["destination_column"]

                    value = record.get(source_header)

                    sheet.cell(
                        row=destination_row,
                        column=destination_column
                    ).value = value

                # Report progress after each completed record.
                if progress_callback:
                    progress_callback(record_index + 1, total_records)

            # Save the actual destination workbook.
            workbook.save(destination_path)

        finally:
            workbook.close()

        return {
            "success": True,
            "records_written": total_records,
            "start_row": start_row,
            "end_row": start_row + total_records - 1,
            "columns_matched": len(matches),
            "unmatched_destination": transfer["unmatched_destination"],
            "unmatched_source": transfer["unmatched_source"],
            "destination_path": str(destination_path)
        }

