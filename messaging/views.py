from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Etudiants.models import Etudiant
# Create your views here.



@login_required
def contact_list(request):
    # Si tes contacts sont les autres utilisateurs :
    contacts = Etudiant.objects.exclude(id=request.user.id)
    # Si tu as un modèle Contact :
    # contacts = Contact.objects.filter(user=request.user)
    return render(request, 'messaging/list_etudiants.html', {'contacts': contacts})