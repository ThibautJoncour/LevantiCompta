
# forms.py
from django import forms
from .models import FichierSource
from .models import FichierRegle
from django import forms
from .models import Transaction2


class FichierSourceForm(forms.ModelForm):
    class Meta:
        model = FichierSource
        fields = ['fichier']

class FichierRegleForm(forms.ModelForm):
    class Meta:
        model = FichierRegle
        fields = ['fichier']

# forms.py
from django import forms








class VotreFormulaire(forms.Form):
    # Ajoutez d'autres champs au besoin
    chemin_output = forms.CharField(max_length=255, label='Chemin du dossier output')


# Ajoutez ceci dans votre fichier forms.py

from django import forms
from .models import Transaction2

class Transaction2Form(forms.ModelForm):
    class Meta:
        model = Transaction2
        fields = '__all__'
