# forum/templatetags/my_filters.py

from django import template

register = template.Library()

@register.filter
def first_word_capitalized(value):
    """
    Retourne le premier mot d'une chaîne de caractères, avec sa première lettre en majuscule.
    Si la chaîne est vide ou ne contient pas d'espace, elle est traitée comme un seul mot.
    """
    if not isinstance(value, str):
        return value # Retourne la valeur telle quelle si ce n'est pas une chaîne

    if not value:
        return value # Retourne une chaîne vide si elle est vide

    # 1. Extraire le premier mot
    parts = value.split(' ', 1) # Divise la chaîne au maximum une fois
    first_word = parts[0]

    # 2. Mettre en majuscule seulement la première lettre de ce premier mot
    if first_word: # S'assurer que le premier mot n'est pas vide
        return first_word[0].upper() + first_word[1:]
    return "" # Retourne vide si le premier mot est vide (ex: chaîne "   autre")

# Tu peux garder d'autres filtres ici si tu en as besoin, par exemple:
# @register.filter
# def capitalize_first_letter(value):
#     # ... (code précédent pour tout le texte) ...