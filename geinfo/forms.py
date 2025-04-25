from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    identifiant = forms.CharField(max_length=150, label='identifiant')
    motdepasse = forms.CharField(widget=forms.PasswordInput, label='motdepasse')

    def clean(self):
        identifiant = self.cleaned_data.get('identifiant')
        motdepasse = self.cleaned_data.get('motdepasse')

        if identifiant and motdepasse:
            user = authenticate(username=identifiant, password=motdepasse)
            if user is not None:
                if user.is_superuser:
                    raise forms.ValidationError("Identifiant ou mot de passe incorrect.")
                elif user.is_active:
                    self.cleaned_data['user'] = user
                else:
                    raise forms.ValidationError("Ce compte est désactivé.")
            else:
                raise forms.ValidationError("Identifiant ou mot de passe incorrect.")
        return self.cleaned_data

class ModifierPhotoProfilForm(forms.Form):
    photo = forms.ImageField(
        label='profiletof',
        required=False  # La photo n'est pas obligatoire
    )

