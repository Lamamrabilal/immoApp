from django.views.generic import ListView

from models import Locataire

class immo_appHome(ListView):
    model = Locataire
    context_object_name = 'immo_app'
