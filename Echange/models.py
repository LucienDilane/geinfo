from django.db import models

from Etudiants.models import Etudiant

# Create your models here.

class Message(models.Model):
    sender=models.ForeignKey(Etudiant, on_delete=models.DO_NOTHING,related_name="envoie")
    receiver=models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="reception")
    corps=models.TextField(max_length="300", verbose_name="message")
    date_envoie=models.DateTimeField(auto_now_add=True)
    lu=models.BooleanField(default=False)

