# devapps/forms.py
from django import forms
from oauth2_provider.models import Application

class ApplicationRegistrationForm(forms.ModelForm):
    class Meta:
        model = Application
        # Champs que l'utilisateur développeur peut renseigner
        fields = ['name', 'client_type', 'authorization_grant_type', 'redirect_uris']
        widgets = {
            'redirect_uris': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Entrez des URLs de redirection séparées par des espaces'
            }),
        }