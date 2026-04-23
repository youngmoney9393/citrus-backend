from fastapi import FastAPI, UploadFile
import shutil, os
from db import get_connection
from utils import get_exif_date, get_weather
from model import predict

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/predict")
async def predict_api(file: UploadFile):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    date = get_exif_date(file_path)
    weather = get_weather()
    disease, confidence = predict(file_path)

    conn = get_connection()
    with conn.cursor() as cur:
        sql = """
        INSERT INTO diagnoses 
        (diagnosis_date, disease_name, confidence, temperature, humidity, weather, image_path)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        cur.execute(sql, (
            date,
            disease,
            confidence,
            weather["temp"],
            weather["humidity"],
            weather["weather"],
            file_path
        ))
    conn.commit()
    conn.close()

    return {
        "disease": disease,
        "confidence": confidence,
        "date": date,
        "weather": weather,
        "image_path": file_path
    }