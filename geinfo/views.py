from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.conf import settings
import os
import uuid  # Pour générer des noms de fichiers uniques
from datetime import timedelta
from Etudiants.models import Etudiant



# Create your views here.
def accueil(request):
    return render(request,'geinfo/accueil.html',{"info":"INFO"})

def connexion(request):
    return render(request,'Etudiants/connexion.html',{"con":"yes"})

def infos(request):
    return render(request, 'geinfo/ginfo.html',{'welcome':"INFO"})


def error_404(request, exception):
    return render(request,"geinfo/404.html",status=404)

def register(request):
    # Le code de vue protégée ici
    return render(request,'geinfo/enregistrer.html',{"yes":"yep"})


def admin(request):
    return render(request,"adminginfo/login.html")

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
            return render(request, 'geinfo/enregistrer.html')

        try:
            annee_entree = int(annee_entree)
        except ValueError:
            messages.error(request, "L'année d'entrée doit être un nombre.")
            return render(request, 'geinfo/enregistrer.html') # Assure-toi que le chemin est correct

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
        return redirect('admin') # Assure-toi que l'URL est correctement nommée dans ton urls.py
    else:
        # Si la requête n'est pas POST, afficher le formulaire HTML
        return render(request, 'geinfo/enregistrer.html')




def delete(request,id):
    etudiant=get_object_or_404(Etudiant,id=id)
    etudiant.delete()
    return redirect("admin")

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
