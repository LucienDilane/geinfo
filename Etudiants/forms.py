from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm

class LoginForm(forms.Form):
    # CHANGEMENT ICI : Les noms des champs correspondent maintenant à ceux de votre HTML
    matricule = forms.CharField(max_length=150, label='Matricule')
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')

    def clean(self):
        # Récupérez les données avec les NOUVEAUX NOMS de champs
        matricule = self.cleaned_data.get('matricule')
        password = self.cleaned_data.get('password')

        if matricule and password:
            # Tente d'authentifier l'utilisateur
            # Assurez-vous que votre backend d'authentification utilise 'matricule' comme nom d'utilisateur
            # Si votre backend d'authentification Django utilise toujours 'username',
            # il faudra le mapper ici ou ajuster le backend d'auth.
            # Supposons que 'matricule' correspond au 'username' de l'utilisateur Django.
            user = authenticate(username=matricule, password=password)

            if user is not None:
                if user.is_superuser:
                    # Ne pas laisser les superutilisateurs se connecter via ce formulaire
                    raise forms.ValidationError("Matricule ou mot de passe incorrect.")
                elif user.is_active:
                    self.cleaned_data['user'] = user
                else:
                    raise forms.ValidationError("Ce compte est désactivé.")
            else:
                raise forms.ValidationError("Matricule ou mot de passe incorrect.")
        return self.cleaned_data
class ModifierPhotoProfilForm(forms.Form):
    photo = forms.ImageField(
        label='profiletof',
        required=False  # La photo n'est pas obligatoire
    )

class ChangerMotDePasseForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le mot de passe actuel'})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nouveau de passe'})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer le nouveau de passe'})
    )

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        # Vous pouvez personnaliser l'ordre ici si nécessaire
        self.fields['old_password'].label = "Ancien mot de passe" # Définir le label ici
        self.fields['new_password1'].label = "Nouveau mot de passe"
        self.fields['new_password2'].label = "Confirmer le nouveau mot de passe"