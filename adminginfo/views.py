import os
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from django.utils.text import slugify # Pour nettoyer les noms de fichiers
from django.contrib import messages

from .forms import LoginAdminForm, Announcement
from .models import Admin
from django.contrib.auth.hashers import make_password



# Create your views here.

def login_admin(request):
    if request.method == 'POST':
        form = LoginAdminForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                admin = Admin.objects.get(username=username)
                if admin.check_password(password):
                    # Authentification réussie !
                    # À ce stade, vous devez gérer la session du Admin.
                    # Puisque vous ne voulez pas utiliser django.contrib.auth,
                    # vous devrez créer votre propre mécanisme de session.
                    # La méthode la plus simple est d'utiliser les sessions de Django
                    # mais avec une clé différente, ou de créer un jeton simple.

                    # Option 1: Utiliser les sessions de Django (recommandé pour la simplicité)
                    # sans interférer avec django.contrib.auth.
                    # Nous stockons simplement l'ID du Admin dans la session.
                    request.session['admin_id'] = admin.id
                    messages.success(request, f'Bienvenue, {admin.username} !')
                    return redirect('interface')  # Redirigez vers le tableau de bord du Admin
                else:
                    messages.error(request, 'Mot de passe incorrect.')
            except Admin.DoesNotExist:
                messages.error(request, ' Admin introuvable.')
    else:
        form = LoginAdminForm()
    return render(request, 'Admin/login.html', {'form': form})
#def annonce(request):
