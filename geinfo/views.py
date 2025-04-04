from django.shortcuts import render
from datetime import datetime

# Create your views here.

def connexion(request):
    return render(request, 'geinfo/connexion.html',{'date':datetime.now()})

def infos(request):
    return render(request, 'geinfo/ginfo.html',{'welcome':"INFO"})

def accueil(request):
    return render(request,'geinfo/accueil.html',{"info":"INFO"})

def error_404(request, exception):
    return render(request,"geinfo/404.html",status=404)