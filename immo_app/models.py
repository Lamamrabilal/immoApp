
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

telephone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')

class Locataire(models.Model):
    nom = models.CharField(max_length=50, unique=True, verbose_name='nom')
    prenom = models.CharField(max_length=50, unique=True, verbose_name='prenom')
    adresse = models.CharField(max_length=50, unique=True, verbose_name='adresse')
    email = models.EmailField(max_length=30, blank=False)
    telephone = models.CharField(max_length=13, validators=[telephone_regex], blank=False)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # génère un slug à partir du nom et du prénom du locataire
        self.slug = slugify(f"{self.nom} {self.prenom}")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['nom']
        verbose_name = "Locataire"

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def get_absolute_url(self):
        return reverse('immo_app:locataire')


class Appartement(models.Model):
    adresse = models.CharField(max_length=255, unique=True)
    complement_adresse = models.CharField(max_length=255, unique=True)
    ville = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=5, validators=[RegexValidator('^[0-9]{5}$', ('Invalid code postale'))])
    locataire = models.ForeignKey(Locataire, on_delete=models.SET_NULL, null=True, blank=False)
    montant_loyer = models.DecimalField(max_digits=10, decimal_places=2)
    montant_charge = models.DecimalField(max_digits=10, decimal_places=2)
    depot_garantie = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['adresse']
        verbose_name = 'Appartement'

    def __str__(self):
        return self.adresse

    def get_absolute_url(self):
        return reverse('immo_app:appartement')


class ContratLocataire(models.Model):
    nom_agence = models.CharField(max_length=50, unique=True, verbose_name='agence')
    locataire = models.ForeignKey( Locataire, on_delete=models.SET_NULL, null=True, blank=False)
    appartement = models.ForeignKey(Appartement, on_delete=models.SET_NULL, null=True, blank=True)
    date_entree = models.DateField(blank=False)
    date_sortie = models.DateField(blank=False)
    duree_contrat = models.DurationField(null=True, blank=True)

    class Meta:
        ordering = ['-duree_contrat']
        verbose_name = 'Contrat_locataire'

    def __str__(self):
        return self.nom_agence

    def get_absolute_url(self):
        return reverse('immo_app:contrat_locataire')


class Paiement(models.Model):
    locataire = models.ForeignKey( Locataire,on_delete=models.SET_NULL, null=True, blank=False)
    appartement = models.ForeignKey(Appartement, on_delete=models.SET_NULL, null=True, blank=True)
    montant_paiement = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField(blank=False)
    origine_paiement = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['-date_paiement']
        verbose_name = 'Paiement'

    def __str__(self):
        return f"{self.locataire} - {self.date_paiement} - {self.montant_paiement}"

    def get_absolute_url(self):
        return reverse('immo_app:paiement')




class EtatLieux(models.Model):
    locataire = models.ForeignKey(Locataire,on_delete=models.SET_NULL,null= True, blank=False)
    appartement = models.ForeignKey(Appartement, on_delete=models.SET_NULL, null=True, blank=False)
    date_entree = models.DateField(blank=False)
    date_sortie = models.DateField(blank=False)
    montant_solde = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Etat_lieux'


    def __str__(self):
        return f"EtatLieux #{self.id} ({self.locataire.nom} {self.locataire.prenom})"

    def get_absolute_url(self):
        return reverse('immo_app:etat_lieux')


class FraisAgence (models.Model):
     agence= models.ForeignKey( ContratLocataire, on_delete=models.SET_NULL, null=True, blank=False)
     frais = models.IntegerField( default= '8')

     def nom_agence(self):
         nom_agence = self.agence.adresse_set.first()
         return nom_agence

     def __str__(self):
         return self.agence