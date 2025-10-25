# translator.py
from googletrans import Translator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

translator = Translator()

def translate_text(text, mode="gist", target_lang="en"):
    """
    Translate or transliterate text.
    Modes:
      - "transliterate": Devanagari <-> Latin (ITRANS)
      - "literal": word-for-word translation using Google Translate
      - "gist": simplified translation using Google Translate
    target_lang: 'en', 'hi', or 'sa' (Sanskrit)
    """
    if mode == "transliterate":
        # Detect if input is Latin letters or Devanagari
        if any('\u0900' <= c <= '\u097F' for c in text):
            # Contains Devanagari → Latin
            return transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)
        else:
            # Assume Latin → Devanagari
            return transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)

    elif mode in ["literal", "gist"]:
        try:
            # auto-detect source language
            translated = translator.translate(text, dest=target_lang)
            return translated.text
        except Exception as e:
            return f"Translation error: {str(e)}"

    else:
        return text
