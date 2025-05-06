from lang.en import text_values as en_val
from lang.tl import text_values as tl_val
from lang.ceb import text_values as ceb_val
from lang.ja import text_values as ja_val
from lang.es import text_values as es_val
from lang.fr import text_values as fr_val 
from lang.zh import text_values as zh_val 

def get_text_values(language):
    match language:
        case "English":
            return en_val
        case "Tagalog":
            return tl_val
        case "Cebuano":
            return ceb_val
        case "Japanese":
            return ja_val
        case "Spanish":
            return es_val
        case "French":
            return fr_val
        case "Mandarin":
            return zh_val 
