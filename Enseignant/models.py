from django.db import models

# Create your models here.

class Enseignant(models.Model):
    nom_teacher= models.CharField(max_length=30,verbose_name="nom Enseignant")
    prenom_teacher= models.CharField(max_length=30)
    grade= models.CharField(max_length=10)
    discipline= models.CharField(max_length=15)