from flask import Flask, render_template
import pdfplumber
import os
import re

app = Flask(__name__)

# Adjust this path to point to your actual PDF with data.
pdf_path = os.path.join(
    os.path.expanduser("~"),
    "OneDrive - Harvard University",
    "CPREPORT",
    "executive_summary.pdf"
)

def remove_commas(s):
    """Remove commas from a string (e.g. '6,561' -> '6561')."""
    return s.replace(",", "")

def extract_int(s):
    """Extract the first integer in a string."""
    s = remove_commas(s)
    match = re.search(r"\d+", s)
    return int(match.group()) if match else 0

def extract_float(s):
    """Extract the first floating-point number in a string."""
    s = remove_commas(s)
    match = re.search(r"[\d.]+", s)
    return float(match.group()) if match else 0.0

def extract_report_text(path):
    """Extract all text from the PDF, concatenating each page."""
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
    return text

def parse_report_data(text):
    """
    Extract summary metrics and composition data from PDF text.
    The daily totals chart/slider are removed completely.
    """
    data = {
        "report_period": "",
        "days_in_period": 0,
        "active_users": 0,
        "active_printers": 0,
        "total_pages": 0,
        "total_sheets": 0,
        "total_jobs": 0,
        "pages_per_day": 0,
        "sheets_per_day": 0,
        "trees_consumed": 0.0,
        "co2_produced": 0.0,
        "env_bulb_hours": 0.0,
        "grayscale_pct": 0.0,
        "color_pct": 0.0,
        "grayscale_count": 0,
        "color_count": 0,
        "duplex_pct": 0.0,
        "simplex_pct": 0.0,
        "duplex_count": 0,
        "simplex_count": 0,
        "scan_count": 0,
        "copy_count": 0,
        "print_count": 0,
        "fax_count": 0
    }

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # Extract date range
    for line in lines:
        if re.search(r"\w+ \d{1,2}, \d{4} to \w+ \d{1,2}, \d{4}", line):
            data["report_period"] = line
            break

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("Days in period:"):
            data["days_in_period"] = extract_int(line.split(":", 1)[1])
        elif line.startswith("Active Users:"):
            data["active_users"] = extract_int(line.split(":", 1)[1])
        elif line.startswith("Active Printers:"):
            data["active_printers"] = extract_int(line.split(":", 1)[1])
        elif line.startswith("Total Printed Pages:"):
            data["total_pages"] = extract_int(line.split(":", 1)[1])
        elif line.startswith("Total Printed Sheets:"):
            data["total_sheets"] = extract_int(line.split(":", 1)[1])
        elif line.startswith("Total Jobs:"):
            data["total_jobs"] = extract_int(line.split(":", 1)[1])
        elif line.startswith("Pages per day:"):
            data["pages_per_day"] = extract_int(line.split(":", 1)[1])
        elif line.startswith("Sheets per day:"):
            data["sheets_per_day"] = extract_int(line.split(":", 1)[1])
        elif line.startswith("Grayscale:"):
            after = line.split("Grayscale:", 1)[1].strip()
            match_pct = re.search(r"([\d.]+)%", after)
            if match_pct:
                data["grayscale_pct"] = float(match_pct.group(1))
            match_num = re.search(r"\b(\d+)\b", after)
            if match_num:
                data["grayscale_count"] = int(remove_commas(match_num.group(1)))
        elif line.startswith("Color:"):
            after = line.split("Color:", 1)[1].strip()
            match_pct = re.search(r"([\d.]+)%", after)
            if match_pct:
                data["color_pct"] = float(match_pct.group(1))
            match_num = re.search(r"\b(\d+)\b", after)
            if match_num:
                data["color_count"] = int(remove_commas(match_num.group(1)))
        elif line.startswith("Duplex:"):
            after = line.split("Duplex:", 1)[1].strip()
            match_pct = re.search(r"([\d.]+)%", after)
            if match_pct:
                data["duplex_pct"] = float(match_pct.group(1))
        elif line.startswith("Simplex:"):
            after = line.split("Simplex:", 1)[1].strip()
            match_pct = re.search(r"([\d.]+)%", after)
            if match_pct:
                data["simplex_pct"] = float(match_pct.group(1))
        elif line.startswith("Scan:"):
            data["scan_count"] = extract_int(line.split("Scan:", 1)[1])
        elif line.startswith("Copy:"):
            data["copy_count"] = extract_int(line.split("Copy:", 1)[1])
        elif line.startswith("Print:"):
            data["print_count"] = extract_int(line.split("Print:", 1)[1])
        elif line.startswith("Fax:"):
            data["fax_count"] = extract_int(line.split("Fax:", 1)[1])
        elif "trees" in line.lower():
            data["trees_consumed"] = extract_float(line)
        elif "grams" in line.lower() or "kg" in line.lower():
            data["co2_produced"] = extract_float(line)
        elif "hours" in line.lower():
            data["env_bulb_hours"] = extract_float(line)
        i += 1

    return data

@app.route("/")
def dashboard():
    # Extract text from PDF
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += (page.extract_text() or "") + "\n"
    print("==== PDF TEXT START ====")
    print(full_text)
    print("==== PDF TEXT END ====")

    data = parse_report_data(full_text)
    print("No daily totals or line chart in this version.")

    # Prepare composition data for the charts
    color_labels = ["Grayscale", "Color"]
    color_values = [data["grayscale_pct"], data["color_pct"]]
    duplex_labels = ["Duplex", "Simplex"]
    duplex_values = [data["duplex_pct"], data["simplex_pct"]]
    job_labels = ["Scan", "Copy", "Print", "Fax"]
    job_counts = [data["scan_count"], data["copy_count"], data["print_count"], data["fax_count"]]

    return render_template(
        "index.html",
        data=data,
        color_labels=color_labels,
        color_values=color_values,
        duplex_labels=duplex_labels,
        duplex_values=duplex_values,
        job_labels=job_labels,
        job_counts=job_counts
    )

if __name__ == "__main__":
    app.run(debug=True)
