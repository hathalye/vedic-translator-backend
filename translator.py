import requests
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

def transliterate_text(text):
    # transliterate from English letters to Devanagari
    return transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)

def translate_literal(text, target_lang):
    # LibreTranslate word-by-word
    words = text.split()
    translated_words = []
    for w in words:
        resp = requests.post("https://libretranslate.com/translate", json={
            "q": w,
            "source": "auto",
            "target": target_lang
        })
        if resp.ok:
            translated_words.append(resp.json().get('translatedText', w))
        else:
            translated_words.append(w)
    return " ".join(translated_words)

def translate_gist(text, target_lang):
    resp = requests.post("https://libretranslate.com/translate", json={
        "q": text,
        "source": "auto",
        "target": target_lang
    })
    if resp.ok:
        return resp.json().get('translatedText', text)
    return text
