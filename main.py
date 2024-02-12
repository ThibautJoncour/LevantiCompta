import subprocess
import webbrowser
import subprocess

# Commande pour installer les dépendances à partir de requirements.txt
install_command = "pip install -r requirements.txt"

try:
    # Exécutez la commande pour installer les dépendances
    subprocess.check_call(install_command, shell=True)
    print("Toutes les dépendances ont été installées avec succès.")
except subprocess.CalledProcessError as e:
    print(f"Une erreur s'est produite lors de l'installation des dépendances : {e}")
except Exception as e:
    print(f"Une erreur inattendue s'est produite : {e}")
    
# Exécutez le serveur Django en arrière-plan
subprocess.Popen(['python', 'manage.py', 'runserver'])
subprocess.Popen(['python', 'dashapp/dash_condition.py'])
subprocess.Popen(['python', 'dashapp/dash_rules.py'])

# Ouvrez la page du serveur dans le navigateur par défaut
webbrowser.open('http://127.0.0.1:8000/')
