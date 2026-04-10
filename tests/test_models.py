import pytest
from django.core.exceptions import ValidationError
from immo_app.models import Locataire, Appartement, ContratLocataire, Paiement, EtatLieux, FraisAgence
from datetime import date, timedelta


@pytest.mark.django_db
@pytest.mark.parametrize(
    "nom, prenom, adresse, email, telephone, expected_slug, expected_str",
    [
        ("Dupont", "Jean", "123 Rue de Paris", "jean.dupont@example.com", "+33612345678", "dupont-jean", "Jean Dupont"),
        ("Martin", "Alice", "321 Place Toulouse", "alice.martin@example.com", "+33511223344", "martin-alice", "Alice Martin"),
    ]
)
def test_locataire_create(nom, prenom, adresse, email, telephone, expected_slug, expected_str):
    locataire = Locataire.objects.create(
        nom=nom, prenom=prenom, adresse=adresse, email=email, telephone=telephone
    )
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
def test_create_appartement(adresse, complement_adresse, ville, postal_code, montant_loyer, montant_charge, depot_garantie, expected_str):
    locataire = Locataire.objects.create(
        nom="Durand", prenom="Paul", adresse="456 Avenue Lyon", email="paul.durand@example.com", telephone="+33765432109"
    )
    appartement = Appartement.objects.create(
        adresse=adresse,
        complement_adresse=complement_adresse,
        ville=ville,
        postal_code=postal_code,
        locataire=locataire,
        montant_loyer=montant_loyer,
        montant_charge=montant_charge,
        depot_garantie=depot_garantie
    )
    assert appartement.ville == ville
    assert str(appartement) == expected_str


@pytest.mark.django_db
@pytest.mark.parametrize(
    "nom_agence, date_entree, date_sortie, expected_str",
    [
        ("Agence Immo Plus", date(2023, 5, 1), date(2024, 5, 1), "Agence Immo Plus"),
        ("Agence Horizon", date(2023, 7, 1), date(2024, 7, 1), "Agence Horizon"),
    ]
)
def test_create_contrat_locataire(nom_agence, date_entree, date_sortie, expected_str):
    locataire = Locataire.objects.create(
        nom="Martin", prenom="Alice", adresse="321 Place Toulouse", email="alice.martin@example.com", telephone="+33511223344"
    )
    appartement = Appartement.objects.create(
        adresse="99 Rue Nice", complement_adresse="Étage 2", ville="Nice", postal_code="06000",
        locataire=locataire, montant_loyer=1000.00, montant_charge=80.00, depot_garantie=2000.00
    )
    contrat = ContratLocataire.objects.create(
        nom_agence=nom_agence,
        locataire=locataire,
        appartement=appartement,
        date_entree=date_entree,
        date_sortie=date_sortie,
        duree_contrat=timedelta(days=365)
    )
    assert str(contrat) == expected_str


@pytest.mark.django_db
@pytest.mark.parametrize(
    "montant_paiement, date_paiement, origine_paiement, expected_str",
    [
        (1300.00, date(2024, 2, 1), "Virement bancaire", "Emma Robert - 2024-02-01 - 1300.0"),
        (1200.00, date(2024, 3, 1), "Chèque", "Emma Robert - 2024-03-01 - 1200.0"),
    ]
)
def test_create_paiement(montant_paiement, date_paiement, origine_paiement, expected_str):
    locataire = Locataire.objects.create(
        nom="Robert", prenom="Emma", adresse="67 Route Lille", email="emma.robert@example.com", telephone="+33455667788"
    )
    appartement = Appartement.objects.create(
        adresse="12 Quai Bordeaux", complement_adresse="Résidence Alpha", ville="Bordeaux", postal_code="33000",
        locataire=locataire, montant_loyer=1200.00, montant_charge=100.00, depot_garantie=2400.00
    )
    paiement = Paiement.objects.create(
        locataire=locataire,
        appartement=appartement,
        montant_paiement=montant_paiement,
        date_paiement=date_paiement,
        origine_paiement=origine_paiement
    )
    assert str(paiement) == expected_str


@pytest.mark.django_db
@pytest.mark.parametrize(
    "date_entree, date_sortie, montant_solde, expected_substr",
    [
        (date(2023, 3, 15), date(2024, 3, 15), 0.00, "EtatLieux"),
        (date(2023, 4, 1), date(2024, 4, 1), 50.00, "EtatLieux"),
    ]
)
def test_create_etat_lieux(date_entree, date_sortie, montant_solde, expected_substr):
    locataire = Locataire.objects.create(
        nom="Lemoine", prenom="Sophie", adresse="88 Rue Lille", email="sophie.lemoine@example.com", telephone="+33988997766"
    )
    appartement = Appartement.objects.create(
        adresse="45 Boulevard Lyon", complement_adresse="Bâtiment C", ville="Lyon", postal_code="69001",
        locataire=locataire, montant_loyer=950.00, montant_charge=60.00, depot_garantie=1900.00
    )
    etat_lieux = EtatLieux.objects.create(
        locataire=locataire,
        appartement=appartement,
        date_entree=date_entree,
        date_sortie=date_sortie,
        montant_solde=montant_solde
    )
    assert expected_substr in str(etat_lieux)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "nom_agence, frais, expected_frais",
    [
        ("Agence Horizon", 10, 10),
        ("Agence Immo Plus", 15, 15),
    ]
)
def test_create_frais_agence(nom_agence, frais, expected_frais):
    locataire = Locataire.objects.create(
        nom="Garcia", prenom="Lucas", adresse="91 Avenue Toulouse", email="lucas.garcia@example.com", telephone="+33677889911"
    )
    appartement = Appartement.objects.create(
        adresse="50 Rue Marseille", complement_adresse="Résidence Delta", ville="Marseille", postal_code="13002",
        locataire=locataire, montant_loyer=1100.00, montant_charge=70.00, depot_garantie=2200.00
    )
    contrat = ContratLocataire.objects.create(
        nom_agence=nom_agence,
        locataire=locataire,
        appartement=appartement,
        date_entree=date(2023, 7, 1),
        date_sortie=date(2024, 7, 1),
        duree_contrat=timedelta(days=365)
    )
    frais_agence = FraisAgence.objects.create(
        agence=contrat,
        frais=frais
    )
    assert frais_agence.frais == expected_frais
