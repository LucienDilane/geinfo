from django.contrib import admin
from .models import Message, Publication, Commentaire
# Register your models here.

admin.site.register(Message)
admin.site.register(Publication)
admin.site.register(Commentaire)