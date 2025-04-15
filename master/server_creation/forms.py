from django import forms

class ServerCreationForm(forms.Form):
    name = forms.CharField(
        label="Nom du serveur",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Un identifiant unique pour votre serveur Tenant."
    )
    port = forms.IntegerField(
        label="Port d'exposition",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Le port sur lequel le serveur sera accessible (ex: 8001, 8002, etc.)."
    )
    superuser_username = forms.CharField(
        label="Nom d'utilisateur (superuser)",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Le nom d'utilisateur pour le superutilisateur du container Tenant."
    )
    superuser_email = forms.EmailField(
        label="Email (superuser)",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        help_text="L'adresse email du superutilisateur."
    )
    superuser_password = forms.CharField(
        label="Mot de passe (superuser)",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Le mot de passe pour le superutilisateur."
    )