from django.contrib import admin

from .models import Locataire

@admin.register(Locataire)
class LocataireAdmin(admin.ModelAdmin):
    list_display = ('nom','prenom','adresse','telephone')
    list_editable = ('adresse',)


