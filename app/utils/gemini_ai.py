import google.generativeai as genai
from config import Config

try:
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    print(" Gemini AI model initialized.")
except Exception as e:
    model = None
    print(f" Failed to initialize Gemini AI: {e}")

def get_ai_response(user_message: str, farmer_profile: dict, conversation_history: list = None, weather_data: dict = None) -> str:
    """Generates an AI response using a structured prompt with conversation history."""
    if not model:
        return "Sorry, the AI service is currently unavailable."

    system_prompt = """
    You are a friendly and helpful agricultural assistant for farmers in Kerala, India.
    your name is krishi sakhi
    Your goal is to provide simple, practical, and actionable advice.
    - Keep your answers concise and easy to understand.
    - If asked about weather, use the provided weather data.
    - Always be encouraging and supportive.
    - Your knowledge base includes crop management, pest control, soil health, and government schemes for Kerala.
    """

    prompt = f"{system_prompt}\n\n"
    prompt += f"--- Farmer Information ---\n"
    prompt += f"Name: {farmer_profile.get('name', 'N/A')}\n"
    prompt += f"Location: {farmer_profile.get('location', 'N/A')}, Kerala\n"
    prompt += f"Primary Crop: {farmer_profile.get('primary_crop', 'N/A')}\n\n"

    # if weather_data:
    #     temp = weather_data.get('main', {}).get('temp', 'N/A')
    #     condition = weather_data.get('weather', [{}])[0].get('description', 'N/A')
    #     prompt += f"--- Current Weather in {farmer_profile.get('location')} ---\n"
    #     prompt += f"Temperature: {temp}°C\n"
    #     prompt += f"Condition: {condition}\n\n"
    
    if conversation_history:
        prompt += "--- Recent Conversation History ---\n"
        for message in conversation_history:
            role = "Farmer" if message.get('role') == 'user' else "Assistant"
            prompt += f"{role}: {message.get('content', '')}\n"
        prompt += "\n"
    
    prompt += f"--- Farmer's New Question ---\n"
    prompt += f"{user_message}\n\n"
    prompt += f"--- Your Answer ---\n"

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini AI error: {e}")
        return "I'm having trouble connecting to my knowledge base. Please try again in a moment."