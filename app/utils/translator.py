from googletrans import Translator

# Initialize the translator once
translator = Translator()

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """Translates text using the googletrans library."""
    if not text:
        return ""
        
    try:
        # The library automatically detects the source if not specified,
        # but being explicit (src=source_lang) is more reliable.
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        return translation.text
    except Exception as e:
        print(f"Google Translate error: {e}")
        # Fallback to returning the original text if translation fails
        return text

print(translate_text("രജിസ്ട്രേഷൻ പൂർത്തിയായി","ml","en"))
