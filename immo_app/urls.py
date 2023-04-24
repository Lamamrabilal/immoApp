

from django.urls import path
from .views import immo_appHome, home,locataire

app_name = 'immo_app'

urlpatterns = [
    path('', home, name='home'),
    path('locataire/', locataire, name='locataire'),
    path('immo_app/', immo_appHome.as_view(),name='immo_app'),
]


