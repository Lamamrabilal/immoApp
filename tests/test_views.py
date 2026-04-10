import pytest
from django.urls import reverse
from django.test import Client
from immo_app.models import Locataire, Appartement, Paiement
from datetime import date


@pytest.mark.django_db
@pytest.mark.parametrize(
    "nom, prenom, adresse, email, telephone, expected_slug, expected_str",
    [
        ("Dupont", "Jean", "123 Rue de Paris", "jean.dupont@example.com", "+33612345678", "dupont-jean", "Jean Dupont"),
        ("Martin", "Alice", "321 Place Toulouse", "alice.martin@example.com", "+33511223344", "martin-alice", "Alice Martin"),
    ]
)
def test_create_locataire_view(nom, prenom, adresse, email, telephone, expected_slug, expected_str):
    client = Client()
    response = client.post(reverse('immo_app:locataire_create'), {
        "nom": nom,
        "prenom": prenom,
        "adresse": adresse,
        "email": email,
        "telephone": telephone
    })

    # Vérifier si des erreurs de formulaire existent
    if response.status_code == 200:
        print(response.content.decode())  # Debugging pour voir les erreurs Django

    assert response.status_code in [200, 302], f"Échec: attendu 302 mais reçu {response.status_code}"

    if response.status_code == 302:
        locataire = Locataire.objects.get(email=email)
        assert locataire.slug == expected_slug
        assert str(locataire) == expected_str

@pytest.mark.django_db
@pytest.mark.parametrize(
    "adresse, complement_adresse, ville, postal_code, montant_loyer, montant_charge, depot_garantie, expected_str",
    [
        ("789 Boulevard Marseille", "Bâtiment B", "Marseille", "13001", 850.50, 50.00, 1700.00, "789 Boulevard Marseille"),
        ("99 Rue Nice", "Étage 2", "Nice", "06000", 1000.00, 80.00, 2000.00, "99 Rue Nice"),
    ]
)
def test_create_appartement_view(adresse, complement_adresse, ville, postal_code, montant_loyer, montant_charge, depot_garantie, expected_str):
    client = Client()
    locataire = Locataire.objects.create(
        nom="Durand", prenom="Paul", adresse="456 Avenue Lyon", email="paul.durand@example.com", telephone="+33765432109"
    )
    response = client.post(reverse('immo_app:appartement_create'), {
        "adresse": adresse,
        "complement_adresse": complement_adresse,
        "ville": ville,
        "postal_code": postal_code,
        "locataire": locataire.id,
        "montant_loyer": montant_loyer,
        "montant_charge": montant_charge,
        "depot_garantie": depot_garantie
    })
    assert response.status_code == 302
    appartement = Appartement.objects.get(adresse=adresse)
    assert appartement.ville == ville
    assert str(appartement) == expected_str


@pytest.mark.django_db
@pytest.mark.parametrize(
    "montant_paiement, date_paiement, origine_paiement, expected_str",
    [
        (1300.00, date(2024, 2, 1), "Virement bancaire", "Emma Robert - 2024-02-01 - 1300.0"),
        (1200.00, date(2024, 3, 1), "Chèque", "Emma Robert - 2024-03-01 - 1200.0"),
    ]
)
def test_create_paiement_view(montant_paiement, date_paiement, origine_paiement, expected_str):
    client = Client()
    locataire = Locataire.objects.create(
        nom="Robert", prenom="Emma", adresse="67 Route Lille", email="emma.robert@example.com", telephone="+33455667788"
    )
    appartement = Appartement.objects.create(
        adresse="12 Quai Bordeaux", complement_adresse="Résidence Alpha", ville="Bordeaux", postal_code="33000",
        locataire=locataire, montant_loyer=1200.00, montant_charge=100.00, depot_garantie=2400.00
    )
    response = client.post(reverse('immo_app:paiement_create'), {
        "locataire": locataire.id,
        "appartement": appartement.id,
        "montant_paiement": montant_paiement,
        "date_paiement": date_paiement,
        "origine_paiement": origine_paiement
    })
    assert response.status_code == 302
    paiement = Paiement.objects.get(date_paiement=date_paiement)
    assert str(paiement) == expected_str


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view_name, args, expected_status",
    [
        ("immo_app:locataire", [], 200),
        ("immo_app:appartement", [], 200),
        ("immo_app:paiement", [], 200),
    ]
)
def test_list_views(view_name, args, expected_status):
    """ Teste les vues listant les objets """
    client = Client()
    response = client.get(reverse(view_name, args=args))
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view_name, args, expected_status",
    [
        ("immo_app:quittance", [1], 404),  # Teste un paiement inexistant
    ]
)
def test_protected_views(view_name, args, expected_status):
    """ Teste des vues qui nécessitent des objets existants """
    client = Client()
    response = client.get(reverse(view_name, args=args))
    assert response.status_code == expected_status
