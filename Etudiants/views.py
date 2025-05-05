from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from django.contrib.auth import login, update_session_auth_hash
from datetime import timedelta
import os

from .forms import LoginForm,ModifierPhotoProfilForm,ChangerMotDePasseForm
from .models import Etudiant

# Create your views here.
def connexion_etudiant(request):
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
    return render(request, 'Etudiants/connexion.html', {'form': form})

@login_required
def profil(request):
    try:
        etudiant = request.user
    except Etudiant.DoesNotExist:

        etudiant = None

    context = {
        'etudiant': etudiant,
    }
    return render(request, 'Etudiants/profil.html', context)


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

        return render(request, 'Etudiants/profil.html', {'form': form})

    else:
        form = ModifierPhotoProfilForm()
        return render(request, 'Etudiants/profil.html', {'form': form})

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
    return render(request, 'Etudiants/profil.html', {'form': form})