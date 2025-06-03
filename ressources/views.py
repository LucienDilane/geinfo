# ressources_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ressource, CategorieRessource
from .forms import RessourceUploadForm
import os
import logging

logger = logging.getLogger(__name__)

# NOTE: La fonction create_initial_categories() et son appel via signals.py
# restent les mêmes et sont essentiels pour que les catégories existent en DB.
# Je ne les répète pas ici pour ne pas alourdir la réponse, mais ils sont nécessaires.

@login_required
def ressources(request):
    if request.method == 'POST':
        form = RessourceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            ressource = form.save(commit=False)
            ressource.auteur = request.user
            
            if not ressource.titre:
                file_name_without_extension = os.path.splitext(ressource.fichier.name)[0]
                ressource.titre = file_name_without_extension

            file_extension = ressource.get_file_extension()
            assigned_category_obj = None 

            if file_extension:
                for category in CategorieRessource.objects.all():
                    if file_extension in category.get_extensions_list():
                        assigned_category_obj = category
                        break

            if assigned_category_obj is None:
                try:
                    assigned_category_obj = CategorieRessource.objects.get(nom="Autres")
                except CategorieRessource.DoesNotExist:
                    logger.warning("La catégorie 'Autres' n'a pas été trouvée, ressource non catégorisée.")
                    assigned_category_obj = None

            ressource.categorie = assigned_category_obj
            ressource.save()

            return redirect('ressources')
    else:
        form = RessourceUploadForm()

    # --- Préparation des données pour l'affichage : Nouvelle approche ---
    # Créons une liste où chaque élément est un dictionnaire représentant une catégorie
    # et contenant ses informations et ses ressources.
    
    categories_data = [] # Cette liste remplacera `resources_by_category` et `sorted_category_names`

    # D'abord, récupérons toutes les catégories existantes de la base de données
    all_db_categories = list(CategorieRessource.objects.all().order_by('nom'))

    # Assurons-nous que la catégorie "Autres" est bien présente et traitée à part si elle existe.
    other_category_obj = None
    try:
        other_category_obj = CategorieRessource.objects.get(nom="Autres")
        # Retirons "Autres" de la liste temporaire pour la traiter à la fin
        if other_category_obj in all_db_categories:
            all_db_categories.remove(other_category_obj)
    except CategorieRessource.DoesNotExist:
        logger.warning("La catégorie 'Autres' n'existe pas en DB. Assurez-vous que create_initial_categories() a été exécuté.")
        # On peut laisser `other_category_obj` à None, et la section "Autres" sera traitée avec les `isnull=True`

    # Traitons les catégories "normales"
    for category in all_db_categories:
        resources = Ressource.objects.filter(categorie=category).order_by('-date_creation')
        categories_data.append({
            'name': category.nom,
            'resources': resources
        })
    
    # Traitons la catégorie "Autres" ou les ressources non classées
    resources_for_other = Ressource.objects.filter(categorie__isnull=True).order_by('-date_creation')
    if other_category_obj: # Si la catégorie "Autres" existe en DB
        # Inclure les ressources explicitement liées à la catégorie "Autres"
        resources_for_other = resources_for_other | Ressource.objects.filter(categorie=other_category_obj).order_by('-date_creation')
    
    # Évite les doublons si une ressource est déjà liée à "Autres" et aussi isnull=True
    resources_for_other = resources_for_other.distinct()

    categories_data.append({
        'name': 'Autres',
        'resources': resources_for_other
    })

    context = {
        'form': form,
        'categories_data': categories_data, # Nouveau nom pour la variable passée au template
    }
    return render(request, 'geinfo/ressources.html', context)