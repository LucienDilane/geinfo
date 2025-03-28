from django.shortcuts import render
from datetime import datetime

# Create your views here.

def accueil(request):
    return render(request, 'geinfo/accueil.html',{'date':datetime.now()})

def infos(request):
    return render(request, 'geinfo/ginfo.html',{'welcome':"INFO"})