import enum
from google.cloud import translate

#enum of languages
class Languages(enum.Enum):
    English = 'en'
    Arabic = 'ar'
    Hebrew = 'he'
    Russian = 'ru'
    Amharic = 'am'
    Spanish = 'es'
    French = 'fr'

# Instantiates a client
translate_client = translate.Client()


def translate_to_hebrew(search_text):
    search_text_translation = translate_client.translate(search_text, target_language='he')
    return '{}'.format(search_text_translation['translatedText'])


def from_hebrew_to_target(result_text, target):
    search_result_translation = translate_client.translate(result_text, target_language=target)
    return '{}'.format(search_result_translation['translatedText'])


text1 = 'Hello, world!'
translation = translate_to_hebrew(text1)
print(translation)
translation = from_hebrew_to_target(translation, 'en')
print(translation)

