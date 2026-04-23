from PIL import Image, ExifTags
from datetime import datetime
import requests
from config import WEATHER_API_KEY, LAT, LON

def get_exif_date(image_path):
    try:
        image = Image.open(image_path)
        exif = image._getexif()
        if exif:
            for tag, value in exif.items():
                if ExifTags.TAGS.get(tag) == "DateTimeOriginal":
                    return value
    except:
        pass
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={WEATHER_API_KEY}&units=metric&lang=ja"
    res = requests.get(url).json()

    return {
        "temp": res["main"]["temp"],
        "humidity": res["main"]["humidity"],
        "weather": res["weather"][0]["description"]
    }