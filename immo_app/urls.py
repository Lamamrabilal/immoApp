

from django.urls import path
from django.conf.urls.static import static
from .views import immo_appHome, ListeLocatairesView, LocataireCreateView, LocataireUpdateView, LocataireDeleteView, \
    AppartementListView, AppartementCreateView, AppartementUpdateView, AppartementDeleteView, ContratLocataireListView, \
    ContratLocataireCreateView, ContratLocataireDeleteView, ContratLocataireUpdateView, Etat_lieuxListView, \
    PaiementListView, QuittanceDetailView, EtatLieuxCreateView, EtatLieuxUpdateView, EtatDeleteLieuxView, \
    PaiementCreateView, PaiementUpdateView, PaiementDeleteView, QuittanceLoyerView

app_name = 'immo_app'


urlpatterns = [

    path('', immo_appHome.as_view(), name='immo_app'),
    path('login/', PaiementListView.as_view(), name='login'),
    path('locataire/', ListeLocatairesView.as_view(), name='locataire'),
    path('locataire_create/', LocataireCreateView.as_view() , name='locataire_create'),
    path('immo_app/<int:pk>/locataire_update/', LocataireUpdateView.as_view(), name='locataire_update'),
    path('immo_app/<int:pk>/locaatire_delete', LocataireDeleteView.as_view(), name='locataire_delete'),

    path('appartement/', AppartementListView.as_view(), name='appartement'),
    path('appartement_create/', AppartementCreateView.as_view(), name='appartement_create'),
    path('immo_app/<int:pk>/appartement_update/', AppartementUpdateView.as_view(), name='appartement_update'),
    path('immo_app/<int:pk>/appartement_delete/', AppartementDeleteView.as_view(), name='appartement_delete'),

    path('contrat_locataire/', ContratLocataireListView.as_view(), name='contrat_locataire'),
    path('contrat_locataire_create/', ContratLocataireCreateView.as_view(), name='contrat_locataire_create'),
    path('immo_app/<int:pk>/contrat_locataire_update/', ContratLocataireUpdateView.as_view(), name='contrat_locataire_update'),
    path('immo_app/<int:pk>/contrat_locataire_delete/', ContratLocataireDeleteView.as_view(), name='contrat_locataire_delete'),

    path('etat_lieux/', Etat_lieuxListView.as_view(), name='etat_lieux'),
    path('etat_lieux_create/', EtatLieuxCreateView.as_view(), name='etat_lieux_create'),
    path('immo_app/<int:pk>/etat_lieux_update/', EtatLieuxUpdateView.as_view(), name='etat_lieux_update'),
    path('<int:pk>/etat_lieux_delete/', EtatDeleteLieuxView.as_view(), name='etat_lieux_delete'),



    path('paiement/', PaiementListView.as_view(), name='paiement'),
    path('paiement_create/', PaiementCreateView.as_view(), name='paiement_create'),
    path('immo_app/<int:pk>/paiement_update/', PaiementUpdateView.as_view(), name='paiement_update'),
    path('immo_app/<int:pk>/paiement_delete/', PaiementDeleteView.as_view(), name='paiement_delete'),
    path('<int:pk>/quittance/', QuittanceLoyerView.as_view(), name='quittance'),
]






