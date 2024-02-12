from typing import Any
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from datetime import date, datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import Transaction2
from .forms import Transaction2Form

# Create your views here.
# views.py
from django.db import transaction
from django.shortcuts import render, redirect
from .forms import FichierSourceForm
from .forms import FichierRegleForm
from .Compta import utiliser_fichier_source, utiliser_deuxieme_script, insert_sql, call_fichier1, call_fichier2
from django.views.generic import TemplateView
from blog.models import Transaction2
import pandas as pd

from django.shortcuts import render
from django.db import connection
import pandas as pd

from django.shortcuts import render
from django.db import connection
import pandas as pd


# myapp/views.py
from django.shortcuts import render


from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection

def transactionView(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM TransactionOutput;")
        data = cursor.fetchall()

    # Vous pouvez adapter cette partie en fonction du nombre de colonnes dans votre table
    columns = [desc[0] for desc in cursor.description]
    context = {'columns': columns, 'data': data}
    
    return render(request, 'blog/view_transactions.html', context)

def dashboard(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Dash INNER JOIN Rules ON Dash.Rule = Rules.Rule;")
        data = cursor.fetchall()

    # Vous pouvez adapter cette partie en fonction du nombre de colonnes dans votre table
    columns = [desc[0] for desc in cursor.description]


    context = {'columns': columns, 'data': data}
    
    return render(request, 'blog/dashboard.html', context)







def votre_vue(request):
    # Exécutez votre requête SQL ici
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM regles")
        results = cursor.fetchall()

    # Convertissez les résultats en un DataFrame
    dataframe_regles = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])

    # Ajoutez le DataFrame au contexte
    context = {'dataframe_regles': dataframe_regles}

    # Passez le contexte au template
    return render(request, 'blog/telechargement_template.html', context)


def telecharger_fichier_source(request):
    if request.method == 'POST':
        form = FichierSourceForm(request.POST, request.FILES)

        dataframe = None  # Initialize dataframe variable

        if form.is_valid():
            instance = form.save()
            chemin_fichier_source = instance.fichier.path

            if 'bouton_lancer' in request.POST:
                script_choice = request.POST.get('script_choice', 'event')  # Default to 'event' if not provided

                if script_choice == 'event':
                    dataframe = utiliser_fichier_source(chemin_fichier_source)
                    insert_sql(dataframe)
                elif script_choice == 'liquid':
                    dataframe = utiliser_deuxieme_script(chemin_fichier_source)
                    insert_sql(dataframe)
                
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM regles")
                results = cursor.fetchall()
                dataframe_regles = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])

            context = {'form': form, 'dataframe_html': dataframe.to_html(), 'dataframe_regles': dataframe_regles.to_html()}
            
            return render(request, 'blog/telechargement_template.html', context)

        elif 'bouton_lancer_fichier' in request.POST:
            # Si le bouton "Lancer le fichier" est cliqué, appelez la fonction sans utiliser le formulaire
            call_fichier1()
            return redirect("telecharger_fichier_source")



            # Faites quelque chose avec le DataFrame, par exemple, imprimez les premières lignes
    else:
        form = FichierSourceForm()
        
    context_autre_vue = votre_vue(request)
    context = {'form': form,'dataframe_regles': context_autre_vue.get('dataframe')}

    return render(request, 'blog/telechargement_template.html', context)
# views.py dans votre application Django


def importer_donnees(request):
    # Étape 3 : Lire les données depuis Excel
    data_frame = pd.read_excel(utiliser_deuxieme_script(chemin_fichier_source))

    # Étape 4 : Utiliser les modèles Django pour enregistrer les données dans la base de données
    for index, row in data_frame.iterrows():
        transaction_instance = Transaction2(
            vcTradeId=row['vcTradeId'],
            Societe=row['Société'],
            Etablissement=row['Etablissement'],
            Journal=row['Journal'],
            DatePiece=row['Date de pièce'],
            ReferencePiece=row['Référence pièce'],
            CompteGeneral=row['Compte général'],
            LibelleEcriture=row['Libellé écriture'],
            Sens=row['Sens'],
            Montant=row['Montant'],
            Devise=row['Devise'],
            Quantite=row['Quantité'],
            TypePiece=row['Type de pièce'],
            Tiers=row['Tiers']
        )
        transaction_instance.save()

    return render(request, 'import_success.html')

def interface(request):
    return render(request, "blog/interface.html", context={"date": datetime.today()})
# views.py

def view_transactions(request):
    transactions = Transaction2.objects.all()
    return render(request, 'blog/view_transactions.html', {'transactions': transactions})


from .models import Regle
# views.py
from django.shortcuts import render, redirect





# dans views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class DateHeureAPI(APIView):
    def get(self, request):
        data = {
            'date': date.today(),
            'heure': datetime.now().strftime('%H:%M:%S'),
        }
        return Response(data, status=status.HTTP_200_OK)
def index(request):
    return render(request, 'blog/index.html')


def modifier_transaction(request, transaction_id=None):
    if request.method == 'GET' and transaction_id is None:
        # Si aucun transaction_id n'est fourni dans la requête GET, redirigez l'utilisateur vers la page principale
        return redirect('nom_de_votre_vue_liste_transactions')

    transaction = get_object_or_404(Transaction2, id=transaction_id)

    if request.method == 'POST':
        form = Transaction2Form(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('view_transaction')
    else:
        form = Transaction2Form(instance=transaction)

    return render(request, 'blog/modifier_transaction.html', {'form': form})





class HomeView(TemplateView):
    template_name="blog/interface.html"
    title = "Default"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["title"] = self.title
        context["date"] = datetime.today()
        return context







def ma_vue_success(request):
    return HttpResponse("success_template")  # Assurez-vous de créer ce modèle

def telechargement_success1(request):
    # Vous pouvez personnaliser le contenu de la réponse ici
    contenu_response = "Téléchargement réussi !"

    # Créez une réponse HTTP avec le contenu spécifié
    response = HttpResponse(contenu_response)

    # Vous pouvez également ajouter des en-têtes HTTP ou d'autres paramètres à la réponse si nécessaire
    # Exemple : response['X-Header'] = 'Valeur'

    return response

def telechargement_success(request):
    return render(request, "blog/interface.html", context={"date": datetime.today()})
# views.py
