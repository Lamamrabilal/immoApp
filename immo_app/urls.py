

from django.urls import path


from .views import immo_appHome,ListeLocatairesView, LocataireCreateView, LocataireUpdateView, LocataireDeleteView

app_name = 'immo_app'

urlpatterns = [

    path('', immo_appHome.as_view(), name='immo_app'),
    path('locataire/', ListeLocatairesView.as_view(), name='locataire'),
    path('create/', LocataireCreateView, name='create'),

    path('immo_app/<slug:slug>/edit/', LocataireUpdateView.as_view(), name='update-edit'),
    path('immo_app/<slug:slug>/delete', LocataireDeleteView.as_view(), name='delete'),
]


