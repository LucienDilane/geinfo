from django.db import models

# Create your models here.
class Etudiant(models.Model):
    matricule=models.CharField(verbose_name="Matricule",max_length=8, unique=True)
    nom= models.CharField(max_length=30,verbose_name="Nom Etudiant")
    prenom= models.CharField(max_length=30,verbose_name="Prenom Etudiant")
    filiere= models.CharField(max_length=3, verbose_name="Filiere")
    niveau= models.IntegerField(verbose_name="Niveau")
    inscrit= models.IntegerField(verbose_name="Annee d'entree")
    statut= models.CharField(max_length=10, verbose_name="statut")
    avatar= models.CharField(max_length=20,verbose_name="profil")
    password=models.CharField(max_length=20,verbose_name="mdp Etudiant")

    def __str__(self):
        return {
                    "nom":self.nom,
                    "prenom":self.prenom,
                    "matricule":self.matricule,
                    "filiere":self.filiere,
                    "niveau":self.niveau,
                    "avatar":self.avatar,
                    "inscrit":self.inscrit
                 }
    
      
    