from django import forms
from django.contrib.auth import authenticate



class LoginForm(forms.Form):
    identifiant = forms.CharField(max_length=150, label='username')
    motdepasse = forms.CharField(widget=forms.PasswordInput, label='password')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    self.cleaned_data['user'] = user
                else:
                    raise forms.ValidationError("Ce compte est désactivé.")
            else:
                raise forms.ValidationError("Nom d'utilisateur ou mot de passe incorrect.")
        return self.cleaned_data
