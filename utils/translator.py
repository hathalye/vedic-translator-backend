# translator.py
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

def detect_script(text):
    """Detects whether text is in Devanagari or Latin script."""
    return "sa" if any('\u0900' <= c <= '\u097F' for c in text) else "en"

def translate_text(text, mode="gist", target_lang="en"):
    """
    Translates or transliterates text.
    Modes:
      - "transliterate": Convert between Devanagari and Latin (ITRANS)
      - "literal": Direct translation
      - "gist": Looser translation (currently same engine)
    target_lang: 'en' (English), 'hi' (Hindi)
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
            if source_lang == "sa":
                source_lang = "hi"  # Sanskrit closest proxy

            translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
            return translated
        except Exception as e:
            return f"Translation error: {str(e)}"

    return text
