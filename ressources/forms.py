from django import forms
from .models import Ressource, CategorieRessource # Gardons CategorieRessource

class RessourceUploadForm(forms.ModelForm):
    # Champ pour afficher la catégorie déterminée par JS (non lié au modèle)
    # Il sera en lecture seule et ne sera pas sauvegardé directement
    categorie_sugeree = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'placeholder': 'Catégorie détectée automatiquement'}),
        label="Catégorie détectée"
    )

    class Meta:
        model = Ressource
        # N'incluez PAS 'categorie' de votre modèle Ressource dans les champs du formulaire ici.
        # Nous allons le gérer manuellement dans la vue.
        fields = ['titre', 'fichier']
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder': 'Titre de la ressource (optionnel)', 'class': 'form-control'}),
            'fichier': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    # Garde ta validation personnalisée du fichier
    def clean_fichier(self):
        fichier = self.cleaned_data.get('fichier')
        if not fichier:
            raise forms.ValidationError("Veuillez sélectionner un fichier à télécharger.")

        allowed_extensions = ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'txt', 'csv', 'zip']
        ext = fichier.name.split('.')[-1].lower()
        if ext not in allowed_extensions:
            raise forms.ValidationError(
                f"L'extension de fichier '{ext}' n'est pas autorisée. Les extensions permises sont : "
                f"{', '.join(allowed_extensions)}."
            )
        
        max_upload_size = 20 * 1024 * 1024 # Exemple: 20 MB max
        if fichier.size > max_upload_size:
            raise forms.ValidationError(
                f"Le fichier est trop volumineux ({fichier.size / (1024*1024):.2f} MB). "
                f"La taille maximale autorisée est de {max_upload_size / (1024*1024):.0f} MB."
            )

        return fichier