# translator.py
from googletrans import Translator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

translator = Translator()

def detect_script(text):
    """Rudimentary check: returns 'sa' if Devanagari, else 'en'."""
    return "sa" if any('\u0900' <= c <= '\u097F' for c in text) else "en"


def translate_text(text, mode="gist", target_lang="en"):
    """
    Translates or transliterates text.
    Modes:
      - "transliterate": Convert between Devanagari and Latin (ITRANS)
      - "literal": More direct translation
      - "gist": Freer translation (same model, but can adjust later)
    target_lang: 'en' (English), 'hi' (Hindi), or 'sa' (Sanskrit)
    """

    if not text.strip():
        return ""

    # Transliteration
    if mode == "transliterate":
        if any('\u0900' <= c <= '\u097F' for c in text):
            # Devanagari → Latin
            return transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)
        else:
            # Latin → Devanagari
            return transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)

    # Translation
    elif mode in ["literal", "gist"]:
        try:
            source_lang = detect_script(text)

            # Special handling for Sanskrit and Hindi (Google uses 'sa' for Sanskrit)
            if source_lang == "sa":
                source_lang = "hi"  # Google Translate doesn’t have direct Sanskrit, but Hindi is close

            # Translate using explicit source & target
            translated = translator.translate(text, src=source_lang, dest=target_lang)
            return translated.text

        except Exception as e:
            return f"Translation error: {str(e)}"

    return text
