# Harvard Crimson Print Dashboard

A Flask-based web application that reads and parses an executive summary PDF report from a specified OneDrive folder, then displays the extracted data in a modern, responsive dashboard. The dashboard is designed with a Harvard-inspired theme, featuring Harvard Crimson accents and a clean, responsive layout using Bootstrap. It includes interactive visualizations and a slider to adjust the time frame for daily totals.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Development Guidelines](#development-guidelines)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [References](#references)

## Features

- **Dynamic PDF Parsing:** Uses [pdfplumber](https://github.com/jsvine/pdfplumber) with a flexible parser built on regular expressions to extract key metrics from a multi-page PDF.
- **Interactive Visualizations:** Utilizes [Chart.js](https://www.chartjs.org/) to render:
  - A line chart for daily totals with a slider to adjust the displayed number of days.
  - Three pie/doughnut charts (Color Composition, Duplex Composition, Job Type Composition) arranged side by side.
- **Responsive Layout:** Built with [Bootstrap 5](https://getbootstrap.com/docs/5.3/getting-started/introduction/) for a mobile-friendly, grid-based design.
- **Harvard-Inspired Theme:** Incorporates Harvard Crimson (#A51C30) accents in the navbar and section titles.

## Project Structure

```
/CP
├── app.py                  # Flask application and PDF parsing logic
├── requirements.txt        # Python dependencies – Flask, pdfplumber, etc.
├── README.md               # This file
└── templates
    └── index.html          # Main HTML template with inline CSS and JavaScript
```

## Prerequisites

- **Python 3.8+**
- **pip** (Python package installer)
- A valid PDF file (named `executive_summary.pdf`) containing real report data located at:
  ```
  ~/OneDrive - Harvard University/CPREPORT/executive_summary.pdf
  ```


## Configuration

- **PDF File Path:**  
  Update the `pdf_path` variable in `app.py` if your PDF file is located elsewhere. For example:

  ```python
  pdf_path = os.path.join(
      os.path.expanduser("~"),
      "OneDrive - Harvard University",
      "CPREPORT",
      "executive_summary.pdf"
  )
  ```

- **Content Security Policy (CSP):**  
  The `index.html` file includes a relaxed CSP meta tag for development purposes (allowing inline scripts and `eval`). For production, consider moving inline scripts to external files and tightening your CSP.

## Development Guidelines

- **PDF Parsing:**  
  The `parse_report_data` function in `app.py` uses regular expressions to extract data. The full PDF text is printed to the console for debugging—review it and adjust the parser if the PDF layout changes.

- **Front-End Development:**  
  The dashboard currently uses inline CSS and JavaScript for simplicity. For a more scalable architecture, consider moving scripts to external files (e.g., under a `static/js` folder).

- **Interactivity:**  
  The daily totals chart features a range slider (`<input type="range">`) that dynamically adjusts the time frame displayed. Modify the `updateDailyChart` function in `index.html` if you want to change its behavior.

- **Responsive Layout:**  
  The layout uses Bootstrap’s grid system to ensure that metrics, charts, and tables display well on different devices.

## Troubleshooting

- **No Data Displayed:**  
  Verify that your PDF contains valid (non-zero) report data. Check the console output to see if the parser is extracting the expected text.

- **Chart or CSP Issues:**  
  If Chart.js fails to load or you see CSP warnings, ensure the `<meta>` tag in `index.html` is correctly set. In production, move inline scripts to external files and update the CSP accordingly.

- **File Path Issues:**  
  Confirm that the `pdf_path` in `app.py` correctly points to your PDF file.

## Future Improvements

- **Enhanced PDF Parsing:**  
  Improve the parser to handle multiple report formats or dynamically changing layouts.
- **Data Caching:**  
  Cache parsed data to avoid reprocessing the PDF on every request, improving performance.
- **Advanced Filtering:**  
  Add date pickers, dropdown filters, or additional sliders for finer control over the displayed data.
- **User Authentication:**  
  Implement authentication if the data is sensitive.
- **Unit and Integration Testing:**  
  Write tests for the PDF parsing logic and Flask routes to ensure stability as the project evolves.
- **Deployment:**  
  Configure a production-ready WSGI server (e.g., Gunicorn) and secure your CSP and other settings for live deployment.

## Further Docs

- [Flask Documentation](https://flask.palletsprojects.com/)
- [pdfplumber Documentation](https://github.com/jsvine/pdfplumber)
- [Chart.js Documentation](https://www.chartjs.org/docs/latest/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/)

