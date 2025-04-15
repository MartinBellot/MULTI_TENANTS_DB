# server_creation/admin.py
from django.contrib import admin
from .models import TenantServer

@admin.register(TenantServer)
class TenantServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'port', 'client_id', 'deployed_at')
    search_fields = ('name', 'ip_address', 'client_id')