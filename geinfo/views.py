from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static

import json

from Etudiants.models import Etudiant
from forum.models import Forum






# Create your views here.
def accueil(request):
    return render(request,'geinfo/index.html',{"info":"INFO"})

def connexion(request):
    return render(request,'Etudiants/connexion.html',{"con":"yes"})

def infos(request):
    return render(request, 'geinfo/ginfo.html',{'welcome':"INFO"})


def error_404(request, exception):
    return render(request,"geinfo/404.html",status=404)

def register(request):
    # Le code de vue protégée ici
    return render(request,'adminginfo/enregistrer.html')


def admin(request):
    return render(request,"adminginfo/login.html")

def administration(request):
    return render(request,"adminginfo/dashboard.html")

def etudiants_list_api(request):
    etudiants = Etudiant.objects.all().values('matricule', 'nom', 'prenom', 'filiere', 'annee', 'profil', 'niveau')
    # Pour chaque étudiant, assurez-vous que 'profil' est un chemin absolu si nécessaire
    # Ou que Django puisse servir les fichiers statiques correctement.
    # Ex: si profil est un chemin relatif à MEDIA_ROOT, vous devrez peut-être le préfixer.
    # Ici, nous supposons qu'il s'agit d'une URL directe ou d'un chemin statique déjà accessible.
    data = list(etudiants)
    return JsonResponse(data, safe=False)

# Fonction utilitaire pour obtenir l'URL complète du profil
def get_profile_url(profile_filename):
    if profile_filename:
        # Construit le chemin relatif dans le dossier static
        # Assurez-vous que 'geinfo' est le nom de votre application
        static_path = f"geinfo/img/profils/{profile_filename}"
        return static(static_path)
    return static("geinfo/img/user.jpg") # Chemin vers votre image de profil par défaut

def forum_profil_url(forum_profil):
    if forum_profil:
        static_path=f"geinfo/img/forums/{forum_profil}"
        return static(static_path)
    return static("geinfo/img/user.jpg")

# Vue API pour lister tous les étudiants
@csrf_exempt
def etudiants_list_api(request):
    if request.method == 'GET':
        etudiants = Etudiant.objects.all()
        data = [{
            'id': etudiant.id,  # <-- Assurez-vous que ceci est présent et correct
            'matricule': etudiant.matricule,
            'nom': etudiant.nom,
            'prenom': etudiant.prenom,
            'filiere': etudiant.filiere,
            'annee': etudiant.annee,
            'niveau': etudiant.niveau,
            'profil': get_profile_url(etudiant.profil) if etudiant.profil else ''
        } for etudiant in etudiants]
        return JsonResponse(data, safe=False)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

# Vue API pour obtenir les détails d'un seul étudiant
def etudiant_detail_api(request, id):
    etudiant = get_object_or_404(Etudiant, id=id)


    forums_data = []
    for forum in etudiant.forums.all(): # Accéder aux forums via le related_name 'forums' de Etudiant
        forums_data.append({
            'id': forum.id,
            'nom': forum.nom,
            'description': forum.description,
            'profil': forum_profil_url(forum.profil),
            'createur_nom': forum.createur.get_full_name() if forum.createur else "N/A" # Nom du créateur
        })

    data = {
        'id':etudiant.id,
        'matricule': etudiant.matricule,
        'nom': etudiant.nom,
        'prenom': etudiant.prenom,
        'annee': etudiant.annee,
        'niveau': etudiant.niveau,
        'filiere': etudiant.filiere,
        'profil': get_profile_url(etudiant.profil), # Utiliser la fonction utilitaire
        'forums': forums_data,  # Inclut les détails des forums
        # Excluez le mot de passe ici
    }
    return JsonResponse(data)

# Vue API pour mettre à jour les informations d'un étudiant (aucun changement ici pour le profil)
@csrf_exempt
def etudiant_detail_update_delete_api(request, id): # Accepte 'id'
    etudiant = get_object_or_404(Etudiant, id=id) # Utilise id pour la recherche

    if request.method == 'GET':
        data = {
            'id': etudiant.id, # Assurez-vous d'inclure l'ID dans la réponse
            'matricule': etudiant.matricule, # Le matricule reste affiché
            'nom': etudiant.nom,
            'prenom': etudiant.prenom,
            'filiere': etudiant.filiere,
            'annee': etudiant.annee,
            'niveau': etudiant.niveau,
            'profil': etudiant.profil.url if etudiant.profil else '',
            'forums': [{'id': f.id, 'nom': f.nom, 'description': f.description, 'createur_nom': f.createur.nom + ' ' + f.createur.prenom if hasattr(f, 'createur') and f.createur else 'N/A'} for f in etudiant.forums.all()]
        }
        return JsonResponse(data)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Données JSON invalides"}, status=400)

        etudiant.nom = data.get('nom', etudiant.nom)
        etudiant.prenom = data.get('prenom', etudiant.prenom)
        etudiant.filiere = data.get('filiere', etudiant.filiere)
        etudiant.annee = data.get('annee', etudiant.annee)
        etudiant.niveau = data.get('niveau', etudiant.niveau)
        etudiant.matricule=data.get('matricule', etudiant.matricule)
        # Ne pas modifier l'ID via cette API si ce sont des identifiants métier stables
        etudiant.save()
        return JsonResponse({"message": "Étudiant mis à jour avec succès !"})

    elif request.method == 'DELETE':
        etudiant.delete()
        return JsonResponse({"message": "Étudiant supprimé avec succès !"}, status=204)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)


@csrf_exempt
def create_forum_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Données JSON invalides"}, status=400)

        nom = data.get('nom')
        description = data.get('description')
        createur_id = data.get('createur_id') # Récupère l'ID du créateur

        if not nom:
            return JsonResponse({"error": "Le nom du forum est requis."}, status=400)

        forum = Forum(nom=nom, description=description)

        if createur_id:
            try:
                createur_etudiant = Etudiant.objects.get(id=createur_id) # Recherche par ID
                forum.createur = createur_etudiant # Assigner l'objet Etudiant
            except Etudiant.DoesNotExist:
                return JsonResponse({"error": "L'ID du créateur spécifié n'existe pas."}, status=400)

        forum.save() # Sauvegarde le forum

        # Si vous avez un ManyToManyField 'membres', ajoutez le créateur
        if createur_id and hasattr(forum, 'membres'):
             forum.membres.add(createur_etudiant)


        return JsonResponse({"message": "Forum créé avec succès!", "id": forum.id, "nom": forum.nom}, status=201)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
def enregistrement_etudiant(request):
    if request.method == 'POST':
        matricule = request.POST.get('matricule')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        annee_entree = request.POST.get('annee')
        niveau = request.POST.get('niveau')
        filiere = request.POST.get('filiere')
        mot_de_passe_clair = request.POST.get('password')

        # Effectuer des validations supplémentaires ici si nécessaire
        if not matricule or not nom or not prenom or not annee_entree or not niveau or not filiere or not mot_de_passe_clair:
            messages.error(request, 'Tous les champs sont obligatoires.')
            return render(request, 'adminginfo/enregistrer.html')

        try:
            annee_entree = int(annee_entree)
        except ValueError:
            messages.error(request, "L'année d'entrée doit être un nombre.")
            return render(request, 'adminginfo/enregistrer.html') # Assure-toi que le chemin est correct

        # Hasher le mot de passe avant de l'enregistrer
        mot_de_passe_hash = make_password(mot_de_passe_clair)

        # Créer une instance du modèle Etudiant et enregistrer les données
        etudiant = Etudiant(
            matricule=matricule,
            nom=nom,
            prenom=prenom,
            annee=annee_entree,
            niveau=niveau,
            filiere=filiere,
            password=mot_de_passe_hash
        )
        etudiant.save()

        messages.success(request, 'Étudiant enregistré avec succès !')
        return redirect('interface') # Assure-toi que l'URL est correctement nommée dans ton urls.py
    else:
        # Si la requête n'est pas POST, afficher le formulaire HTML
        return render(request, 'adminginfo/enregistrer.html')




def delete(request,id):
    etudiant=get_object_or_404(Etudiant,id=id)
    etudiant.delete()
    return redirect("interface")


def verif(filiere):
    fililieres=("Licence 1", "Licence 2", "Licence 3","Master 1", "Master 2")
    if filiere in fililieres:
        return True
    else: return False
def update(request,id):
    etudiant=get_object_or_404(Etudiant, id=id)
    if request.method == 'POST':
        matricule = request.POST.get('matricule')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        annee_entree = request.POST.get('annee')
        niveau = request.POST.get('niveau')
        filiere = request.POST.get('filiere')

        # Effectuer des validations supplémentaires ici si nécessaire
        if not matricule or not nom or not prenom or not annee_entree or not niveau or not filiere:
            messages.error(request, 'Tous les champs sont obligatoires.')
            return render(request, 'geinfo/modifier.html')
        if filiere !='II' and filiere !='TIC':
            messages.error(request,"Seuls II et TIC sont valides")
            return render(request,'geinfo/modifier.html')

        if  not verif(filiere):
            messages.error(request,"Entrez un niveau valide")
            return render(request,'geinfo/modifier.html')
        try:
            annee_entree = int(annee_entree)
        except ValueError:
            messages.error(request, "L'année d'entrée doit être un nombre.")
            return render(request, 'geinfo/modifier.html') # Assure-toi que le chemin est correct

        # Modifier l'instance du modèle Etudiant et enregistrer les données
        etudiant.matricule=matricule
        etudiant.nom=nom
        etudiant.prenom=prenom
        etudiant.annee=annee_entree
        etudiant.filiere=filiere
        etudiant.niveau=niveau

        try:
            etudiant.save()
            messages.success(request, "Les informations de l'étudiant ont été mises à jour avec succès.")
            return redirect('admin')  # Redirigez vers la liste des étudiants
        except Exception as e:
            messages.error(request, f"Une erreur s'est produite lors de la mise à jour : {e}")

    else:
        # Si la requête n'est pas POST, afficher le formulaire HTML

        return render(request, 'geinfo/modifier.html',{"etudiant":etudiant})

# Nouvelle Vue API pour créer un forum
@csrf_exempt
def create_forum_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nom = data.get('nom')
            description = data.get('description')
            # Le créateur sera l'étudiant actuellement sélectionné ou connecté.
            # Pour l'exemple, nous allons le lier à l'étudiant actuellement affiché.
            # Dans un vrai système, ce serait l'utilisateur connecté (request.user).
            matricule_createur = data.get('createur_matricule') # Envoyé depuis le frontend

            if not nom:
                return JsonResponse({'error': 'Le nom du forum est obligatoire.'}, status=400)

            try:
                # Tente de trouver l'étudiant créateur par son matricule
                createur_etudiant = None
                if matricule_createur:
                    createur_etudiant = get_object_or_404(Etudiant, matricule=matricule_createur)

                forum = Forum.objects.create(
                    nom=nom,
                    description=description,
                    createur=createur_etudiant
                )
                return JsonResponse({'message': 'Forum créé avec succès !', 'id': forum.id, 'nom': forum.nom}, status=201)
            except Exception as e:
                return JsonResponse({'error': f'Erreur lors de la création du forum: {str(e)}'}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données JSON invalides.'}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée.'}, status=405)


# Vue API pour mettre à jour les informations d'un étudiant (inchangée pour cette tâche)
@csrf_exempt
def etudiant_update_api(request, matricule):
    if request.method == 'POST':
        etudiant = get_object_or_404(Etudiant, matricule=matricule)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        etudiant.nom = data.get('nom', etudiant.nom)
        etudiant.prenom = data.get('prenom', etudiant.prenom)
        etudiant.annee = data.get('annee', etudiant.annee)
        etudiant.niveau = data.get('niveau', etudiant.niveau)
        etudiant.filiere = data.get('filiere', etudiant.filiere)

        etudiant.save()
        return JsonResponse({'message': 'Etudiant mis à jour avec succès', 'matricule': etudiant.matricule})
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)