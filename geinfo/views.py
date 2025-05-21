from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static

import json

from Etudiants.models import Etudiant






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
    return render(request,'adminginfo/enregistrer.html',{"yes":"yep"})


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

# Vue API pour lister tous les étudiants
def etudiants_list_api(request):
    etudiants_queryset = Etudiant.objects.all()
    data = []
    for etudiant in etudiants_queryset:
        data.append({
            'matricule': etudiant.matricule,
            'nom': etudiant.nom,
            'prenom': etudiant.prenom,
            'filiere': etudiant.filiere,
            'annee': etudiant.annee,
            'niveau': etudiant.niveau,
            'profil': get_profile_url(etudiant.profil), # Utiliser la fonction utilitaire
        })
    return JsonResponse(data, safe=False)

# Vue API pour obtenir les détails d'un seul étudiant
def etudiant_detail_api(request, matricule):
    etudiant = get_object_or_404(Etudiant, matricule=matricule)
    data = {
        'matricule': etudiant.matricule,
        'nom': etudiant.nom,
        'prenom': etudiant.prenom,
        'annee': etudiant.annee,
        'niveau': etudiant.niveau,
        'filiere': etudiant.filiere,
        'profil': get_profile_url(etudiant.profil), # Utiliser la fonction utilitaire
        # Excluez le mot de passe ici
    }
    return JsonResponse(data)

# Vue API pour mettre à jour les informations d'un étudiant (aucun changement ici pour le profil)
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

def modifier_etudiant(request,id):
    etudiant=get_object_or_404(Etudiant,id=id)
    return render(request,"geinfo/modifier.html",{"etudiant":etudiant})

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
