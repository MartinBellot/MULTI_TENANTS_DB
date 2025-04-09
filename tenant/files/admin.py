# files/admin.py
from django.contrib import admin
from .models import File, FileKeyword

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_name', 'upload_date')

@admin.register(FileKeyword)
class FileKeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'token')