from presentation.states.dark_mode_state import DarkModeScheme
from presentation.states.accent_color_state import AccentColors

from data.color_values.sora_light import color_values as sora_light
from data.color_values.sora_dark import color_values as sora_dark
from data.color_values.sakura_light import color_values as sakura_light
from data.color_values.sakura_dark import color_values as sakura_dark
from data.color_values.suna_light import color_values as suna_light
from data.color_values.suna_dark import color_values as suna_dark
from data.color_values.cha_light import color_values as cha_light
from data.color_values.cha_dark import color_values as cha_dark
from data.color_values.nori_light import color_values as nori_light
from data.color_values.nori_dark import color_values as nori_dark
from data.color_values.kaki_light import color_values as kaki_light
from data.color_values.kaki_dark import color_values as kaki_dark

def get_accented_light_mode(accent: AccentColors):
    match accent:
        case AccentColors.SORA:
            return sora_light
        case AccentColors.SAKURA:
            return sakura_light
        case AccentColors.SUNA:
            return suna_light
        case AccentColors.CHA:
            return cha_light
        case AccentColors.NORI:
            return nori_light
        case AccentColors.KAKI:
            return kaki_light

def get_accented_dark_mode(accent: AccentColors):
    match accent:
        case AccentColors.SORA:
            return sora_dark
        case AccentColors.SAKURA:
            return sakura_dark
        case AccentColors.SUNA:
            return suna_dark
        case AccentColors.CHA:
            return cha_dark
        case AccentColors.NORI:
            return nori_dark
        case AccentColors.KAKI:
            return kaki_dark

def get_colors(scheme: DarkModeScheme, accent: AccentColors):
    match scheme:
        case DarkModeScheme.LIGHT:
            return get_accented_light_mode(accent)
        case DarkModeScheme.DARK:
            return get_accented_dark_mode(accent)