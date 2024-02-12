"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py
from django.urls import path
from blog.views import telecharger_fichier_source, telechargement_success, view_transactions
from blog.views import DateHeureAPI, HomeView, interface, modifier_transaction
from blog.views import dashboard, transactionView
from django.urls import path
from dashapp.views import dash_view, dash_view_rules, add_row, modify_row, dashboard_view, add_row_rule, modify_row_rule, dashboard_view_rule



urlpatterns = [

    path('', interface, name='interface'),
    path('rules/', dashboard_view_rule, name='index'),
    path('add-row_rule/', add_row_rule, name='add_row_rules'),
    path('modify-row_rule/', modify_row_rule, name='modify_row_rules'),
    path('add_row/', add_row, name='add_row'),
    path('modify_row/', modify_row, name='modify_row'),
    path('modify_condition/', dashboard_view, name='dashboard'),
    path('dashboard/', dashboard, name='dashboard2'),
    #path('add_row/', ajouter_ligne, name='add_lignes'),
    path('levanti_run', telecharger_fichier_source, name='telecharger_fichier_source'),
    path('database/', transactionView, name='view_transaction'),
    path('telechargement_success/', telechargement_success, name='telechargement_success'),
    path('modifier_transaction/<int:transaction_id>/', modifier_transaction, name='modifier_transaction')

]

