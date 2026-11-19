
from openpyxl import Workbook
from excel_automation import ExcelAutomation
from pathlib import Path

folder = Path(__file__).parent

# Create sample source workbook
source = Workbook()
source_sheet = source.active
source_sheet.title = "Employee Data"

source_sheet.append(["Name", "Department", "Salary"])
source_sheet.append(["Esther", "ICT", 45000])
source_sheet.append(["John", "Finance", 38000])
source_sheet.append(["Mary", "HR", 42000])

source.save(folder / "source_data.xlsx")
source.close()

# Create destination template
template = Workbook()
template_sheet = template.active
template_sheet.title = "Employee Records"

template_sheet.append(["Name", "Salary", "Department"])

template.save(folder / "excel_template.xlsx")
template.close()

# Run Excel automation
excel = ExcelAutomation()

records = excel.load_source(folder / "source_data.xlsx")

print("Source data loaded:")
for record in records:
    print(record)

completed = excel.fill_template(
    folder / "excel_template.xlsx",
    folder / "completed_data.xlsx"
)

print("\nExcel automation completed!")
print("Records transferred:", completed)
print("Output: completed_data.xlsx")
