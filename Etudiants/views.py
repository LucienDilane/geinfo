from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth import login, update_session_auth_hash
from datetime import timedelta
import os

from .forms import LoginForm, ModifierPhotoProfilForm,ChangerMotDePasseForm
from chat.models import Message
from .models import Etudiant

# Create your views here.
def connexion_etudiant(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)

            if request.POST.get('remember_me'):  # La case à cocher "remember_me" n'est pas dans votre HTML fourni, mais si vous l'ajoutez plus tard, ce code fonctionnera.
                request.session.set_expiry(timedelta(weeks=2))
            else:
                request.session.set_expiry(0)

            return redirect('profil')  # Assurez-vous que l'URL 'profil' est bien configurée sans arguments si elle n'en prend pas.
    else:
        form = LoginForm()

    return render(request, 'Etudiants/connexion.html', {'form': form})
@login_required  # S'assurer que l'utilisateur est connecté pour voir son profil
def profil(request):
     current_user_etudiant = request.user  # Accéder à l'objet Etudiant lié à l'utilisateur connecté

     # Initialiser une liste pour stocker les étudiants contactés et leur dernier message
     contacted_etudiants_info = {}

     # Messages envoyés par l'étudiant courant
     sent_messages = Message.objects.filter(sender_id=current_user_etudiant)
     for message in sent_messages:
         other_etudiant = message.receiver
         if other_etudiant.id != current_user_etudiant.id:  # Évite de se lister soi-même
             if other_etudiant.id not in contacted_etudiants_info or \
                     message.timestamp > contacted_etudiants_info[other_etudiant.id]['last_message_timestamp']:
                 contacted_etudiants_info[other_etudiant.id] = {
                     'etudiant': other_etudiant,
                     'last_message_timestamp': message.timestamp
                 }

     # Messages reçus par l'étudiant courant
     received_messages = Message.objects.filter(receiver=current_user_etudiant)
     for message in received_messages:
         other_etudiant = message.sender
         if other_etudiant.id != current_user_etudiant.id:  # Évite de se lister soi-même
             if other_etudiant.id not in contacted_etudiants_info or \
                     message.timestamp > contacted_etudiants_info[other_etudiant.id]['last_message_timestamp']:
                 contacted_etudiants_info[other_etudiant.id] = {
                     'etudiant': other_etudiant,
                     'last_message_timestamp': message.timestamp
                 }

     # Convertir le dictionnaire en liste et trier par la date du dernier message
     sorted_contacted_etudiants = sorted(
         contacted_etudiants_info.values(),
         key=lambda x: x['last_message_timestamp'],
         reverse=True
     )

     # Récupérer les 5 dernières personnes (objets Etudiant)
     last_5_contacts = [item['etudiant'] for item in sorted_contacted_etudiants[:5]]

     context = {
         'etudiant': current_user_etudiant,  # C'est l'étudiant dont on affiche le profil
         'last_5_contacts': last_5_contacts,
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
      show_modal = True
      old_password=request.POST.get('old_password')
      new_password1=request.POST.get('new_password1')
      new_password2=request.POST.get('new_password2')

      etudiant=Etudiant.objects.get(id=request.user.id)

      if etudiant.password==make_password(old_password):
          if new_password1==new_password2:
              etudiant.password=make_password(new_password1)
              etudiant.save()

              return redirect('connexion')
          else:
              text1="Les mots de passe ne coincident pas""Les mots de passe ne coincident pas"
              return render(request,"Etudiants/profil.html",{"show":show_modal,"text1":text1})
      else:
          text2="Mot de passe incorrect""Mot de passe incorrect"
          return render(request,"Etudiants/profil.html",{"show":show_modal,"text2":text2})

    else:
        return render(request,"Etudiants/profil.html")

