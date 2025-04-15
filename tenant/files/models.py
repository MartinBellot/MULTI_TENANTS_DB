from django.db import models
from django.utils import timezone

class File(models.Model):
    original_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='uploaded_files/')  
    upload_date = models.DateTimeField(default=timezone.now)
    iv = models.CharField(max_length=64, blank=True, null=True, help_text="Vecteur d'initialisation")
    file_hash = models.CharField(max_length=1200, blank=True, null=True, help_text="Hash du fichier")

    def __str__(self):
        return self.original_name or str(self.pk)

    @property
    def is_encrypted(self):
        return bool(self.iv)

class FileKeyword(models.Model):
    file = models.ForeignKey(File, related_name='keywords', on_delete=models.CASCADE)
    token = models.CharField(max_length=256, db_index=True, help_text="Token généré (HMAC)")

    def __str__(self):
        return f"{self.file} - Token: {self.token}"