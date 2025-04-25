from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.conf import settings
import os
import uuid  # Pour générer des noms de fichiers uniques
from datetime import timedelta
from Etudiants.models import Etudiant
from .forms import LoginForm,ModifierPhotoProfilForm


# Create your views here.
def accueil(request):
    return render(request,'geinfo/accueil.html',{"info":"INFO"})

def connexion(request):
    return render(request,'geinfo/connexion.html',{"con":"yes"})
def connexion_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            if request.POST.get('remember_me'):
                # Définir une durée de vie de session plus longue (par exemple, 2 semaines)
                request.session.set_expiry(timedelta(weeks=2))
            else:
                # Définir une durée de vie de session par défaut (fermeture du navigateur)
                request.session.set_expiry(0)
            # Rediriger l'utilisateur après la connexion
            return redirect('profil')
    else:
        form = LoginForm()
    return render(request, 'geinfo/connexion.html', {'form': form})

def infos(request):
    return render(request, 'geinfo/ginfo.html',{'welcome':"INFO"})


def error_404(request, exception):
    return render(request,"geinfo/404.html",status=404)
@login_required
def profil(request):
    try:
        etudiant = request.user
    except Etudiant.DoesNotExist:

        etudiant = None

    context = {
        'etudiant': etudiant,
    }
    return render(request, 'geinfo/profil.html', context)



def admin(request):
    # Le code de vue protégée ici
    return render(request,'geinfo/admin.html',{"yes":"yep"})


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
            return render(request, 'geinfo/admin.html')

        try:
            annee_entree = int(annee_entree)
        except ValueError:
            messages.error(request, "L'année d'entrée doit être un nombre.")
            return render(request, 'geinfo/admin.html') # Assure-toi que le chemin est correct

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
        return redirect('accueil') # Assure-toi que l'URL est correctement nommée dans ton urls.py
    else:
        # Si la requête n'est pas POST, afficher le formulaire HTML
        return render(request, 'geinfo/admin.html')


def modifier_photo_profil(request):
    if request.method == 'POST':
        form = ModifierPhotoProfilForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.cleaned_data["profile"]
            etudiant = request.user

            if photo:
                # Générer un nom de fichier unique pour éviter les collisions
                nom_fichier, extension = os.path.splitext(photo.name)
                nom_fichier_unique = f'{etudiant.matricule}_{uuid.uuid4().hex}{extension}'

                # Construire le chemin de destination dans le dossier static
                chemin_destination_static = os.path.join(settings.BASE_DIR, 'geinfo', 'static', 'geinfo', 'img',
                                                         'profils', nom_fichier_unique)

                # S'assurer que le dossier de destination existe
                os.makedirs(os.path.join(settings.BASE_DIR, 'geinfo', 'static', 'geinfo', 'img', 'profils'),
                            exist_ok=True)

                # Écrire le fichier sur le disque
                with open(chemin_destination_static, 'wb+') as destination:
                    for chunk in photo.chunks():
                        destination.write(chunk)

                # Enregistrer uniquement le nom du fichier dans la base de données
                etudiant.profil = nom_fichier_unique
                etudiant.save()
                return redirect('profil')  # Rediriger vers l'espace utilisateur après succès
            else:
                # Si aucun fichier n'a été choisi, ne rien faire et rediriger
                return redirect('profil')
        else:
            # Si le formulaire n'est pas valide, afficher les erreurs
            return render(request, 'geinfo/profil.html', {'form': form})
    else:
        # Si la requête est GET, afficher le formulaire vide
        form = ModifierPhotoProfilForm()
        return render(request, 'geinfo/profil.html', {'form': form})