from django.shortcuts import render
from django.http import HttpResponse

def accueil(request):
    text="<h1>BIENVENUE SUR LA PLATEFORME GINFO</h1> <p>Echangez avec les autres</p>"
    return HttpResponse(text)
# Create your views here.
