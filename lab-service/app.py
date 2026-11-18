import os

from flask import Flask, request, jsonify
from extract_lab_values import extract_lab_values
from predict_diabetes import predict_diabetes

app = Flask(__name__)

@app.route("/analyze-pdf", methods=["POST"])
def analyze_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "PDF dosyası eksik"}), 400

    file = request.files['file']
    mode = request.form.get("type")  # "diabetes" veya "labs"

    try:
        lab_values = extract_lab_values(file)
        lab_values = {k: v for k, v in lab_values.items() if v is not None}

        glucose = lab_values.get("blood_glucose_level")
        hba1c = lab_values.get("HbA1c_level")

        if mode == "diabetes":
            if glucose is not None and hba1c is not None:
                prediction = predict_diabetes(glucose, hba1c)
                return jsonify({"diabetes_prediction": prediction})
            else:
                return jsonify({"error": "Glukoz ve HbA1c verisi eksik."}), 422

        elif mode == "labs":
            return jsonify({"lab_values": lab_values})

        else:
            return jsonify({"error": "Geçersiz istek türü. 'type' parametresi 'diabetes' veya 'labs' olmalı."}), 400

    except Exception as e:
        return jsonify({"error": f"Hata oluştu: {str(e)}"}), 500

if __name__ == "__main__":
    # Local use only. Set FLASK_DEBUG=1 to enable debug mode.
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1", port=5001)
