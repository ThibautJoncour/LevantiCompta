from django.db import models

# Create your models here.
# models.py
from django.db import models
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

os.path.join(BASE_DIR, 'blog')

class FichierSource(models.Model):

    fichier = models.FileField(upload_to=os.path.join(BASE_DIR, 'project/telecharger'))

class FichierRegle(models.Model):
    fichier = models.FileField(upload_to=os.path.join(BASE_DIR, 'project/telecharger'))

class Transaction2(models.Model):
    
    vcTradeId = models.IntegerField()
    Société = models.CharField(max_length=50)
    Etablissement = models.CharField(max_length=50)
    Journal = models.CharField(max_length=50)
    DatePiece = models.CharField(max_length=50)
    ReferencePiece = models.CharField(max_length=50)
    CompteGeneral = models.CharField(max_length=50)
    LibelleEcriture = models.CharField(max_length=255)
    Sens = models.CharField(max_length=1)
    Montant = models.DecimalField(max_digits=15, decimal_places=2)
    Devise = models.CharField(max_length=3)
    Quantity = models.IntegerField(null=True)
    TypePiece = models.CharField(max_length=50)
    Tiers = models.CharField(max_length=50,null=True)

    def __str__(self):
        return f"{self.vcTradeId} - {self.Societe} - {self.ReferencePiece}"
    

class Regle(models.Model):
    statut = models.CharField(max_length=255)
    cre = models.CharField(max_length=255)
    portfolio = models.CharField(max_length=255)
    event_type = models.CharField(max_length=255)
    event_sub_type = models.CharField(max_length=255)
    process_type = models.CharField(max_length=255)
    trade_type = models.CharField(max_length=255)
    first_trade_type = models.CharField(max_length=255)
    second_trade_type = models.CharField(max_length=255)
    buy_sell = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    societe = models.CharField(max_length=255)
    etablissement = models.CharField(max_length=255)
    journal = models.CharField(max_length=255)
    date_piece = models.CharField(max_length=255)
    reference_piece = models.CharField(max_length=255)
    compte_general = models.CharField(max_length=255)
    libelle_ecriture = models.CharField(max_length=255)
    sens = models.CharField(max_length=255)
    montant = models.CharField(max_length=255)
    devise = models.CharField(max_length=255)
    quantite = models.CharField(max_length=255)
    type_piece = models.CharField(max_length=255)
    tiers = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.statut} - {self.cre} - {self.portfolio} - {self.event_type} - {self.event_sub_type}"
    # models.py


from django.db import models

