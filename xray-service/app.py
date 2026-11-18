import io
import os

import numpy as np
from flask import Flask, request, jsonify
from keras.models import load_model
from PIL import Image

app = Flask(__name__)

# Download the model file first (see README) or point MODEL_PATH to it.
MODEL_PATH = os.environ.get("MODEL_PATH", "xception_model_finetuned.h5")
model = load_model(MODEL_PATH)

def prepare_image(image):
    img = Image.open(io.BytesIO(image)).convert('RGB')
    img = img.resize((256, 256))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "Dosya yüklenmedi!"}), 400

    file = request.files['file'].read()
    img_array = prepare_image(file)

    predictions = model.predict(img_array)
    confidence = float(predictions[0][0])

    result = "Pneumonia" if confidence > 0.5 else "Normal"

    return jsonify({
        "result": result,
        "HastalikOrani": confidence
    })

if __name__ == '__main__':
    # Local use only. Set FLASK_DEBUG=1 to enable debug mode.
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1", host='127.0.0.1', port=5002)
