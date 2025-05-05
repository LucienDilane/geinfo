from django.shortcuts import render,redirect
from django.contrib.auth import login

from .forms import LoginForm
from .models import Admin
# Create your views here.

def login_admin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            # Rediriger l'utilisateur après la connexion
            return redirect('administration')
    else:
        form = LoginForm()
    return render(request, 'adminginfo/login.html', {'form': form})