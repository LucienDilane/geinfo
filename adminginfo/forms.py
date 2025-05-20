from django import forms
from django.contrib.auth import authenticate

class LoginAdminForm(forms.Form):
    username = forms.CharField(max_length=150, label='username')
    password = forms.CharField(widget=forms.PasswordInput, label='password')



class Announcement(forms.Form):
    titre = forms.CharField(max_length=255, label="title")
    content = forms.CharField(widget=forms.Textarea, required=False, label="content")
    fichier = forms.FileField(label="join")

