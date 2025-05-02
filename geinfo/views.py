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
from .forms import LoginForm,ModifierPhotoProfilForm,ChangerMotDePasseForm


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



def register(request):
    # Le code de vue protégée ici
    return render(request,'geinfo/enregistrer.html',{"yes":"yep"})

@login_required
def admin(request):
    etudiants=Etudiant.objects.all()
    return render(request,"geinfo/admin.html", {"etudiants":etudiants})

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


def modifier_photo_profil(request):
    etudiant = get_object_or_404(Etudiant,matricule=request.user.matricule)  # Utilisez matricule pour identifier l'étudiant

    if request.method == 'POST':
        form = ModifierPhotoProfilForm(request.POST, request.FILES)
        if form.is_valid():
            profile_picture = form.cleaned_data['photo']
            if profile_picture:
                chemin_destination = os.path.join(settings.BASE_DIR, 'geinfo', 'static', 'geinfo', 'img', 'profils')
                nom_fichier = f"{etudiant.matricule}_{profile_picture.name}"  # Utilisez le matricule pour le nom du fichier
                chemin_fichier_destination = os.path.join(chemin_destination, nom_fichier)

                os.makedirs(chemin_destination, exist_ok=True)

                try:
                    with open(chemin_fichier_destination, 'wb+') as destination:
                        for chunk in profile_picture.chunks():
                            destination.write(chunk)

                    etudiant.profil = nom_fichier  # Enregistrez le nom du fichier dans le champ 'profil'
                    etudiant.save()
                    return redirect('profil')  # Remplacez par le nom de votre vue de profil

                except Exception as e:
                    form.add_error('profile_picture',f"Une erreur est survenue lors de l'enregistrement de l'image : {e}")

        return render(request, 'geinfo/profil.html', {'form': form})

    else:
        form = ModifierPhotoProfilForm()
        return render(request, 'geinfo/profil.html', {'form': form})

def changer_mot_de_passe(request):
    if request.method == 'POST':
        form = ChangerMotDePasseForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été changé avec succès !')
            return redirect('profil')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = ChangerMotDePasseForm(request.user)
    return render(request, 'geinfo/profil.html', {'form': form})

def delete(request,id):
    etudiant=get_object_or_404(Etudiant,id=id)
    etudiant.delete()
    return redirect("admin")

def modifier_etudiant(request,id):
    etudiant=get_object_or_404(Etudiant,id=id)
    return render(request,"geinfo/modifier.html",{"etudiant":etudiant})
