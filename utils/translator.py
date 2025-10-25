# translator.py
from googletrans import Translator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# Initialize translator
translator = Translator()

def translate_text(text, mode="gist", target_lang="en"):
    """
    Translate or transliterate input text.
    Modes:
      - "transliterate": convert Devanagari/Hindi/Sanskrit text to Latin letters
      - "literal": direct translation using Google Translate
      - "gist": simpler/gist translation using Google Translate
    """
    if mode == "transliterate":
        # Proper Devanagari -> Latin transliteration
        return transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)

    elif mode in ["literal", "gist"]:
        # Use Google Translate
        try:
            translated = translator.translate(text, src='hi', dest=target_lang)
            return translated.text
        except Exception as e:
            return f"Translation error: {str(e)}"

    else:
        # fallback: return input if mode unknown
        return text
