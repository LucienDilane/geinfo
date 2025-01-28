from django.db import models

# Create your models here.
class Etudiant(models.Model):
    matricule=models.CharField(max_length=8, unique=True)
    nom= models.Charfield(max_length=30)
      
    