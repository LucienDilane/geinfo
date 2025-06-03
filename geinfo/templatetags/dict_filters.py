# ressources_app/templatetags/dict_filters.py

from django import template

# Instancie un objet Template.Library pour enregistrer tes filtres
register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Permet d'accéder à un élément d'un dictionnaire par sa clé dans un template Django.

    Utilisation dans un template:
    {% load dict_filters %}
    ...
    {% for category_name in sorted_category_names %}
        {% with resources=resources_by_category|get_item:category_name %}
            {# Ici, 'resources' contiendra la liste des ressources pour cette category_name #}
            ...
        {% endwith %}
    {% endfor %}
    """
    if isinstance(dictionary, dict): # Vérifie si l'objet est bien un dictionnaire
        return dictionary.get(key)
    return None # Retourne None si ce n'est pas un dictionnaire ou si la clé n'existe pas