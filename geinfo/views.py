from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils import timezone
from datetime import timedelta

from .forms import LoginForm


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
    context={"user":request.user}
    return render(request,"geinfo/profil.html",context)


@login_required
def admin(request):
    # Le code de vue protégée ici
    return (request,"geinfo/admin.html")



