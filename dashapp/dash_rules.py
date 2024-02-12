


from pathlib import Path
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
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

# Sample data
BASE_DIR = Path(__file__).resolve().parent.parent
path = BASE_DIR/"db.sqlite3"
query_rules = "SELECT * FROM Rules;"
gestion_df = GestionDataFrame(path, query_rules)

app = dash.Dash(__name__, url_base_pathname='/rules/')

# Define app layout
app.layout = html.Div([
    html.H1("Gestion de la règle", style={'backgroundColor': couleur_bleue, 'color': couleur_noire}),

    # Add row interface
    html.H3("Ajouter une ligne"),
    dcc.Input(id='new-row-rule', type='text', placeholder='Rule'),
    html.Button('Ajouter Ligne', id='add-row-button'),
    
    # Modify row interface
    html.H3("Modifier une ligne"),
    dcc.Input(id='modify-row-rule', type='text', placeholder='Rule'),
    dcc.Dropdown(
        id='modify-row-column-dropdown',
        options=[{'label': col, 'value': col} for col in gestion_df.df.columns],
        placeholder='Select Column to Modify'
    ),
    dcc.Input(id='modify-row-value', type='text', placeholder='New Value'),
    html.Button('Modifier Ligne', id='modify-row-button'),
    
    # Save to SQLite button
    html.H3("Enregistrer dans SQLite"),
    html.Button('Enregistrer dans SQLite', id='save-sqlite-button'),
    
    # Display the DataFrame as a table
    html.H3("DataFrame"),
    dash_table.DataTable(
        id='data-table',
        columns=[{'name': col, 'id': col} for col in gestion_df.df.columns],
        data=gestion_df.df.to_dict('records')
    )
])

# Define callback to update dataframe display
@app.callback(Output('data-table', 'data'),
              [Input('add-row-button', 'n_clicks'),
               Input('modify-row-button', 'n_clicks'),
               Input('save-sqlite-button', 'n_clicks')],
              [dash.dependencies.State('new-row-rule', 'value'),
               dash.dependencies.State('modify-row-rule', 'value'),
               dash.dependencies.State('modify-row-column-dropdown', 'value'),
               dash.dependencies.State('modify-row-value', 'value')])
def update_dataframes(add_clicks, modify_clicks, save_sqlite_clicks, new_rule, modify_rule, modify_column, modify_value):
    ctx = dash.callback_context
    triggered_id = ctx.triggered_id if ctx.triggered_id else 'No clicks yet'
    
    if triggered_id == 'add-row-button' and add_clicks:
        nouvelle_ligne = {'Rule': new_rule}
        gestion_df.ajouter_ligne(nouvelle_ligne)
    
    if triggered_id == 'modify-row-button' and modify_clicks:
        modifications = {modify_column: modify_value}
        gestion_df.modifier_ligne(modify_rule, modifications)
    
    if triggered_id == 'save-sqlite-button' and save_sqlite_clicks:
        gestion_df.enregistrer_dans_sqlite_rules(path)
    
    # Return updated table data
    table_data = gestion_df.df.to_dict('records')
    
    return table_data


# Run the app
app.run('127.0.0.1', 8060, use_debugger=True)



