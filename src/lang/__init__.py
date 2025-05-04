from lang.en import text_values as en_val
from lang.tl import text_values as tag_val
from lang.ceb import text_values as ceb_val
from lang.ja import text_values as jp_val
from lang.es import text_values as span_val

def get_text_values(language):
    match language:
        case "English":
            return en_val
        case "Tagalog":
            return tag_val
        case "Cebuano":
            return ceb_val
        case "Japanese":
            return jp_val
        case "Spanish":
            return span_val
        case "French":
            return span_val # TEMPORARY
        case "Mandarin":
            return span_val # TEMPORARY
        case "Brainrot":
            return span_val # TEMPORARY