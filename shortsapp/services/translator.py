from googletrans import Translator

def translate_to_english(text : str):
    translator = Translator()
    result = translator.translate(text, src='ko', dest='en')
    return result.text