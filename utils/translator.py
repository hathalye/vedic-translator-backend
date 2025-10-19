from transformers import MarianMTModel, MarianTokenizer
from unidecode import unidecode

# Load MarianMT model for Hindi → English
hi_to_en_model_name = "Helsinki-NLP/opus-mt-hi-en"
hi_to_en_tokenizer = MarianTokenizer.from_pretrained(hi_to_en_model_name)
hi_to_en_model = MarianMTModel.from_pretrained(hi_to_en_model_name)

def translate_text(text, mode="gist", target_lang="en"):
    """
    Translate or transliterate input text.
    Modes:
      - "transliterate": convert Devanagari/Hindi text to Latin letters
      - "literal": literal-ish translation using MarianMT
      - "gist": simpler/gist translation using MarianMT
    """
    if mode == "transliterate":
        # Basic transliteration using unidecode
        return unidecode(text)
    
    elif mode in ["literal", "gist"]:
        # Use MarianMT for translation
        inputs = hi_to_en_tokenizer(text, return_tensors="pt", truncation=True)
        translated = hi_to_en_model.generate(
            **inputs,
            max_length=512,
            num_beams=4,
            do_sample=False
        )
        output = hi_to_en_tokenizer.decode(translated[0], skip_special_tokens=True)

        if mode == "gist":
            # Optional: shorten for gist (simplify sentences)
            # For now, just return the same output; can improve later
            return output
        else:
            return output
    
    else:
        return text  # fallback: return input if mode unknown
