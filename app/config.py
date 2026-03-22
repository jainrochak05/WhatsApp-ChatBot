# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")
    
    # Twilio
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
    
    # Google Gemini AI
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # OpenWeatherMap API
    #OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

    # LibreTranslate API (Free, public instance)
    #LIBRETRANSLATE_URL = "https://libretranslate.de/translate"
