import pandas as pd
import joblib

model = joblib.load("model.pkl")  # Daha önce eğitilmiş modeli yükle

def predict_diabetes(glucose, hba1c):
    df = pd.DataFrame([[glucose, hba1c]], columns=["blood_glucose_level", "HbA1c_level"])
    prediction = model.predict(df)[0]
    return int(prediction)
