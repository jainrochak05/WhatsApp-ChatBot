
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import traceback

from config import Config
from utils.database import db_manager
from utils.translator import translate_text
# from utils.weather import get_weather_data
from utils.gemini_ai import get_ai_response

app = Flask(__name__)

# --- Onboarding Configuration ---
ONBOARDING_STEPS = {
    # (Onboarding steps remain the same)
    "name": {
        "question_ml": "നിങ്ങളുടെ പേര് എന്താണ്?",
        "question_en": "What is your name?",
        "next_step": "location"
    },
    "location": {
        "question_ml": "നിങ്ങളുടെ സ്ഥലം/ഗ്രാമം എവിടെയാണ്?",
        "question_en": "What is your location/village?",
        "next_step": "primary_crop"
    },
    "primary_crop": {
        "question_ml": "നിങ്ങളുടെ പ്രധാന വിള എന്താണ്? (ഉദാ: നെല്ല്, തെങ്ങ്)",
        "question_en": "What is your main crop? (e.g., Paddy, Coconut)",
        "next_step": "completed"
    }
}

@app.route("/")
def health_check():
    return "Malayalam Farmer AI Chatbot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    twiml_response = MessagingResponse()
    
    try:
        incoming_msg = request.values.get("Body", "").strip()
        from_number_no_prefix = request.values.get("From", "").split("whatsapp:")[-1]

        farmer = db_manager.get_farmer(from_number_no_prefix)
        
        if not farmer:
            farmer = db_manager.create_farmer(from_number_no_prefix)
            welcome_msg = f"🌾 കർഷക AI സഹായിയിലേക്ക് സ്വാഗതം!\nWelcome to the AI Farming Assistant!\n\n"
            first_question = ONBOARDING_STEPS["name"]
            response_msg = f"{welcome_msg}{first_question['question_ml']}\n{first_question['question_en']}"
        
        elif not farmer.get("onboarding_completed", False):
            # (Onboarding logic remains the same)
            current_step = farmer.get("onboarding_step", "name")
            db_manager.update_farmer(from_number_no_prefix, {current_step: incoming_msg})
            next_step_key = ONBOARDING_STEPS[current_step]["next_step"]
            
            if next_step_key == "completed":
                db_manager.update_farmer(from_number_no_prefix, {"onboarding_completed": True, "onboarding_step": None})
                response_msg = "✅ രജിസ്ട്രേഷൻ പൂർത്തിയായി!\nRegistration complete!\n\nഇനി നിങ്ങൾക്ക് കൃഷിയുമായി ബന്ധപ്പെട്ട എന്ത് സംശയങ്ങളും ചോദിക്കാം.\nYou can now ask me anything related to farming."
            else:
                next_question = ONBOARDING_STEPS[next_step_key]
                db_manager.update_farmer(from_number_no_prefix, {"onboarding_step": next_step_key})
                response_msg = f"✅ സംരക്ഷിച്ചു! / Saved!\n\n{next_question['question_ml']}\n{next_question['question_en']}"

        else:
            # --- THIS IS THE MAIN CHANGE ---
            # 1. Fetch recent conversation history
            history = db_manager.get_conversation_history(from_number_no_prefix)
            
            # 2. Translate and get weather (as before)
            is_malayalam = any(0x0D00 <= ord(char) <= 0x0D7F for char in incoming_msg)
            english_message = translate_text(incoming_msg, "ml", "en") if is_malayalam else incoming_msg
            # weather_info = get_weather_data(farmer["location"]) if farmer.get("location") else None

            # 3. Get AI response, now with history
            ai_response_en = get_ai_response(
                english_message,
                farmer,
                conversation_history=history, # Pass the history here
                # weather_data=weather_info
            )
            
            # 4. Translate response back if needed
            response_msg = translate_text(ai_response_en, "en", "ml") if is_malayalam else ai_response_en

            # 5. Save the new turn to the conversation history
            db_manager.save_conversation(from_number_no_prefix, "user", incoming_msg)
            db_manager.save_conversation(from_number_no_prefix, "assistant", response_msg)

        twiml_response.message(response_msg)

    except Exception as e:
        traceback.print_exc()
        response_msg = "Sorry, a technical error occurred. The issue has been logged."
        twiml_response.message(response_msg)

    return str(twiml_response)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
