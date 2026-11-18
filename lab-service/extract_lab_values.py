import pdfplumber
import re

def get_value(text, pattern):
    match = re.search(pattern, text)
    if match:
        return float(match.group(1).replace(",", "."))
    return None

def extract_lab_values(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages])

    return {
        "blood_glucose_level": get_value(text, r"Glukoz.*?(\d{2,4}[,\.]?\d*)"),
        "HbA1c_level": get_value(text, r"Glike hemoglobin.*?(\d{1,2}[,\.]?\d*)"),
        "cholesterol": get_value(text, r"Kolesterol.*?(\d{2,3}[,\.]?\d*)"),
        "triglyceride": get_value(text, r"Trigliserid.*?(\d{2,3}[,\.]?\d*)"),
        "HDL": get_value(text, r"HDL.*?(\d{2,3}[,\.]?\d*)"),
        "LDL": get_value(text, r"LDL.*?(\d{2,3}[,\.]?\d*)"),
        "CRP": get_value(text, r"C[\s\-]?reaktif[\s\-]?protein.*?\(?CRP\)?\s*(\d{1,3}[,\.]?\d*)"),
        "Calcium": get_value(text, r"Kalsiyum.*?(\d{2,3}[,\.]?\d*)"),
        "Potassium": get_value(text, r"Potasyum(?:\s*\(K\))?.*?(\d{1,2}[,\.]?\d*)"),
        "Creatinine": get_value(text, r"Kreatinin.*?(\d{2,3}[,\.]?\d*)"),
        "Sodium": get_value(text, r"Sodyum.*?(\d{2,3}[,\.]?\d*)"),
        "Urea": get_value(text, r"Üre.*?(\d{2,3}[,\.]?\d*)")
    }
