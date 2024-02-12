# dashapp/views.py
from django.shortcuts import render

# dashboard/views.py
from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import os


import webbrowser
#run_dash_app()

#webbrowser.open('http://127.0.0.1:8051/')
#webbrowser.open('http://127.0.0.1:8050/')

# Run the app



import subprocess
import webbrowser




def dash_view_rules(request):
    # Lancer le script Dash
    subprocess.Popen(["python", "dashapp/dash_rules.py"])

    # Ouvrir le navigateur
    webbrowser.open_new_tab("http://127.0.0.1:8000/Condition/")  # Assurez-vous que le port utilisé par Dash est correct

    return HttpResponse('dash lancé')


def dash_view(request):
    # Lancer le script Dash
    subprocess.Popen(["python", "dashapp/dash_condition.py"])

    # Ouvrir le navigateur
    #webbrowser.open_new_tab("http://127.0.0.1:8000/Condition/")  # Assurez-vous que le port utilisé par Dash est correct

    return HttpResponse('dash lancé')



# Dans le fichier views.py de votre application Django
# Your GestionDataFrame class and other imports here...
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash import dash_table 
import pandas as pd
import sqlite3
from dash import dash, callback, Output, Input, State
import webbrowser
import os
from django.conf import settings
from pathlib import Path
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import sqlite3
from pathlib import Path
import webbrowser

couleur_bleue = '#00B5E2'
couleur_noire = '#2D2926'
styles = {
    'backgroundColor': couleur_bleue,  # Couleur bleue pour le fond de l'en-tête
    'color': couleur_noire  # Couleur noire pour le texte dans l'en-tête
}
# Your GestionDataFrame class
class GestionDataFrame:
    def __init__(self, db_path, requete):
        self.db_path = db_path
        self.requete = requete
        self.charger_donnees()


    def charger_donnees(self):
        conn = sqlite3.connect(self.db_path)
        self.df = pd.read_sql_query(self.requete, conn)
        conn.close()

    def ajouter_ligne(self, nouvelle_ligne):
        self.df = pd.concat([self.df, pd.DataFrame([nouvelle_ligne])], ignore_index=True)

    def modifier_ligne(self, regle, modifications):
        mask = self.df['Rule'] == regle
        self.df.loc[mask, list(modifications.keys())] = list(modifications.values())

    def enregistrer_dans_sqlite(self, db_path):
        conn = sqlite3.connect(db_path)
        self.df.to_sql('Dash', conn, if_exists='replace', index=False)

    def enregistrer_dans_sqlite_rules(self, db_path):
        conn = sqlite3.connect(db_path)
        self.df.to_sql('Rules', conn, if_exists='replace', index=False)


from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import sqlite3
from pathlib import Path
from django.http import HttpResponse, HttpResponseRedirect

couleur_bleue = '#00B5E2'
couleur_noire = '#2D2926'

# Votre classe GestionDataFrame et les autres imports ici...


    # Les méthodes restantes de GestionDataFrame ici...


BASE_DIR = Path(__file__).resolve().parent.parent
path = BASE_DIR/"db.sqlite3"
query_condition = "SELECT * FROM Dash;"
gestion_df1 = GestionDataFrame(path, query_condition)

def dashboard_view(request):
    # Charger le fichier HTML
    template_name = 'blog/dash.html'

    # Rendre le fichier HTML en tant que réponse
    return render(request, template_name, {
        'couleur_bleue': couleur_bleue,
        'couleur_noire': couleur_noire,
        'data': gestion_df1.df.to_html()
    })

def add_row(request):
    if request.method == 'POST':
        new_row_rule = request.POST.get('new_row_rule')
        gestion_df1.ajouter_ligne({'Rule': new_row_rule})
        gestion_df1.enregistrer_dans_sqlite(path)
        return HttpResponseRedirect('/modify_condition/')

def modify_row(request):
    
    if request.method == 'POST':
        modify_row_rule1 = request.POST.get('modify_row_rule')
        modify_row_column1 = request.POST.get('modify_row_column')
        modify_row_value1 = request.POST.get('modify_row_value')
        gestion_df1.modifier_ligne(modify_row_rule1, {modify_row_column1: modify_row_value1})
        gestion_df1.enregistrer_dans_sqlite(path)  # Enregistrer dans SQLite
        return HttpResponseRedirect("/modify_condition/")

from django.shortcuts import render
from pathlib import Path
import pandas as pd
import sqlite3

# Your GestionDataFrame class and other imports here...

couleur_bleue = '#00B5E2'
couleur_noire = '#2D2926'

BASE_DIR = Path(__file__).resolve().parent.parent
path1 = BASE_DIR / "db.sqlite3"
query_rules = "SELECT * FROM Rules;"
gestion_df = GestionDataFrame(path, query_rules)
# view.py

from django.shortcuts import render
from django.http import JsonResponse

# Vos imports et la création de l'objet GestionDataFrame ici...


def add_row_rule(request):
    if request.method == 'POST':
        new_row_rule = request.POST.get('new_row_rule')
        gestion_df.ajouter_ligne({'Rule': new_row_rule})
        gestion_df.enregistrer_dans_sqlite_rules(path1)
        return HttpResponseRedirect('/rules/')

def modify_row_rule(request):
    if request.method == 'POST':
        modify_row_rule = request.POST.get('modify_row_rule')
        modify_row_column = request.POST.get('modify_row_column')
        modify_row_value = request.POST.get('modify_row_value')
        gestion_df.modifier_ligne(modify_row_rule, {modify_row_column: modify_row_value})
        gestion_df.enregistrer_dans_sqlite_rules(path1)  # Enregistrer dans SQLite
        return HttpResponseRedirect("/rules/")



def dashboard_view_rule(request):
    # Charger le fichier HTML
    template_name = 'blog/dash_rule.html'
    # Rendre le fichier HTML en tant que réponse
    return render(request, template_name, {
        'data': gestion_df.df.to_html(),
        'columns': gestion_df.df.columns
    })

