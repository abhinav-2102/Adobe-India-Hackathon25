import os
import re
from PyPDF2 import PdfReader
from langdetect import detect
from transformers import MarianMTModel, MarianTokenizer

LANG_TO_MARIAN = {
    "ar": "ar-en",    "bn": "bn-en",    "zh": "zh-en",    "zh-TW": "zh-TW-en",
    "da": "da-en",    "nl": "nl-en",    "fr": "fr-en",    "de": "de-en",
    "el": "el-en",    "hi": "hi-en",    "id": "id-en",    "ga": "ga-en",
    "it": "it-en",    "he": "he-en",    "ja": "ja-en",    "ko": "ko-en",
    "ne": "ne-en",    "no": "no-en",    "fa": "fa-en",    "pl": "pl-en",
    "pt": "pt-en",    "ro": "ro-en",    "ru": "ru-en",    "es": "es-en",
    "sv": "sv-en",    "tl": "tl-en",    "ta": "ta-en",    "te": "te-en",
    "th": "th-en",    "tr": "tr-en",    "uk": "uk-en",    "vi": "vi-en"
}

def translate_text(text, source_lang, target_lang='en'):
    """Translate text using MarianMT; handles splitting long text into chunks."""
    source_code = LANG_TO_MARIAN.get(source_lang, f"{source_lang}-{target_lang}")
    try:
        model_name = f"Helsinki-NLP/opus-mt-{source_code}"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)

        # Split text into chunks of ~400 tokens (leave buffer from 512 limit)
        max_length = 400
        input_texts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
        translated_texts = []

        for chunk in input_texts:
            inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=512, padding="max_length")
            translated = model.generate(**inputs)
            translated_texts.append(tokenizer.decode(translated[0], skip_special_tokens=True))

        return " ".join(translated_texts).strip()
    except Exception as e:
        print(f"Translation failed ({source_lang}): {str(e)[:100]}... Using original text as fallback.")
        return text

def extract_sections(pdf_path, translate_always=True):
    """Extract section headings and page text from a PDF, optionally translating to English."""
    reader = PdfReader(pdf_path)
    full_text = []

    for i, page in enumerate(reader.pages):
        full_text.append({"text": page.extract_text() or "", "page": i})

    language = 'en'
    for item in full_text:
        if item["text"] and len(item["text"]) > 50:
            try:
                language = detect(item["text"][:1000])
            except:
                language = 'en'
            break

    sections = []
    for item in full_text:
        text = item["text"].strip()
        if not text:
            continue

        if translate_always and language != 'en':
            text = translate_text(text, language, 'en')

        lines = text.replace('\r', '').split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if (line.istitle() or line.isupper() or (line.endswith(':') and len(line.split()) < 8 and len(line) < 40)):
                sections.append({
                    "title": line,
                    "page": item["page"],
                    "text": text
                })
                break

    return {
        "sections": sections,
        "language": language,
        "translated": (language != 'en' and translate_always)
    }
