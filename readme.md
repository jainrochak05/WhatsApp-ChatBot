
# 🌾 Krishi Sakhi - Multilingual WhatsApp Farmer Assistant

Krishi Sakhi is an intelligent, multilingual WhatsApp chatbot designed to assist farmers in Kerala, India. Built with Python and Flask, it leverages Google Gemini AI to provide actionable advice on crop management, pest control, soil health, and government schemes. The bot seamlessly translates between Malayalam and English, ensuring accessibility for local farmers.

## ✨ Features

* **Multilingual Support**: Automatically detects Malayalam input, translates it to English for AI processing, and translates the response back to Malayalam using `googletrans`.
* **AI-Powered Responses**: Uses Google's Gemini 1.5 Flash model to generate context-aware, practical agricultural advice.
* **Guided Onboarding**: New users are guided through a simple registration flow to collect their Name, Location, and Primary Crop (e.g., Paddy, Coconut) before interacting with the AI.
* **Conversation Memory**: Stores chat history in MongoDB to maintain context across ongoing conversations.
* **WhatsApp Integration**: Built on top of the Twilio Messaging API for seamless integration with WhatsApp.

## 🛠️ Tech Stack

* **Backend**: Python, Flask
* **AI/LLM**: Google Generative AI (Gemini 1.5 Flash)
* **Database**: MongoDB (PyMongo)
* **Messaging**: Twilio WhatsApp API
* **Translation**: Googletrans

## 🚀 Getting Started

### Prerequisites
* Python 3.8+
* MongoDB database (Local or Atlas URI)
* Twilio Account (with a WhatsApp sandbox/approved number)
* Google Gemini API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/whatsapp-chatbot.git](https://github.com/yourusername/whatsapp-chatbot.git)
   cd whatsapp-chatbot
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirement.txt
   ```

3. **Environment Setup:**
   Create a `.env` file in the root directory and add the following credentials:
   ```env
   MONGO_URI=your_mongodb_connection_string
   DB_NAME=krishi_sakhi_db
   
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_WHATSAPP_NUMBER=your_twilio_whatsapp_number
   
   GEMINI_API_KEY=your_google_gemini_api_key
   ```

### Running the Application

1. **Start the Flask server:**
   ```bash
   python app/app.py
   ```
   The application will run locally on `http://localhost:5000`.

2. **Expose the local server:**
   Use a tool like [ngrok](https://ngrok.com/) to expose your local port to the internet so Twilio can reach your webhook.
   ```bash
   ngrok http 5000
   ```

3. **Configure Twilio:**
   Go to your Twilio WhatsApp Sandbox settings and set the **"When a message comes in"** webhook URL to:
   `https://<your-ngrok-url>.ngrok.io/webhook`

## 📂 Project Structure

```text
whatsapp-chatbot/
│
├── app/
│   ├── app.py                 # Main Flask application and webhook router
│   ├── config.py              # Environment variable configurations
│   └── utils/
│       ├── database.py        # MongoDB connection and CRUD operations
│       ├── gemini_ai.py       # Google Gemini AI prompt structure and logic
│       ├── translator.py      # Googletrans integration for English/Malayalam
│       └── weather.py         # (WIP) Weather data integration
│
├── requirement.txt            # Python dependencies
└── .env                       # Secrets and API keys (not in version control)
```

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License
This project is licensed under the MIT License.
```

Would you like me to draft a `.gitignore` file to go with this repository?
