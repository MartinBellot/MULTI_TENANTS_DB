# files/forms.py
from django import forms
from .models import File
from .utils import generate_token
from .models import FileKeyword

class FileUploadForm(forms.ModelForm):
    keywords = forms.CharField(
        required=False,
        help_text="Entrez des mots-clés séparés par des espaces."
    )

    class Meta:
        model = File
        exclude = ('original_name', 'file_path', 'upload_date')

    def save(self, commit=True):
        instance = super().save(commit=commit)
        # Gérer les mots-clés
        kw_string = self.cleaned_data.get('keywords', '')
        if kw_string:
            kw_list = kw_string.split()
            for kw in kw_list:
                token = generate_token(kw)
                FileKeyword.objects.create(file=instance, token=token)
        return instance


class FileSearchForm(forms.Form):
    query = forms.CharField(
        required=True,
        help_text="Tapez un mot-clé pour rechercher"
    )