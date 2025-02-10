from django.db import models

# Create your models here.
class Etudiant(models.Model):
    matricule=models.CharField(verbose_name="Matricule",max_length=8, unique=True)
    nom= models.CharField(max_length=30,verbose_name="Nom Etudiant")
    prenom= models.CharField(max_length=30,verbose_name="Prenom Etudiant")
    filiere= models.CharField(max_length=3, verbose_name="Filiere")
    niveau= models.IntegerField(verbose_name="Niveau")
    inscrit= models.IntegerField(verbose_name="Annee d'entree")
    password=models.CharField(max_length=20,verbose_name="mdp Etudiant")
    
      
    