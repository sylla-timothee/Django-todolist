# 🌅 Django Todo-List — Édition Crépuscule

Une application Web de gestion de tâches (Todo-List) robuste, sécurisée et élégante, développée avec le framework **Django** et habillée avec **Tailwind CSS**. Ce projet a été conçu dans un cadre académique pour démontrer la maîtrise d'un CRUD complet, d'un système d'authentification utilisateur étanche et de l'extension de modèles.

---

## 🚀 Fonctionnalités majeures

* **Authentification complète :** Inscription automatique, connexion et déconnexion sécurisées des utilisateurs.
* **Espace privé hermétique :** Chaque utilisateur possède sa propre liste de tâches, invisible pour les autres membres.
* **CRUD Complet (Task Management) :** Création, lecture, modification du statut et suppression définitive des tâches.
* **Gestion de profil (Avatar) :** Possibilité pour l'utilisateur de téléverser une image de profil personnalisée stockée de manière sécurisée.
* **Interface Crépuscule :** Design moderne, fluide et responsive utilisant Tailwind CSS avec une palette de couleurs chaleureuses (beige et orangé chatoyant).

---

## 🛠️ Prérequis & Installation

Pour déployer et lancer ce projet sur votre machine locale, suivez le protocole ci-dessous :

### 1. Cloner le projet : 
```
git clone [https://github.com/VOTRE-NOM-UTILISATEUR/Django-todolist.git](https://github.com/VOTRE-NOM-UTILISATEUR/Django-todolist.git)
cd Django-todolist bash
```
2. Créer et activer l'environnement virtuel
```
python3 -m venv env
source env/bin/activate
```
4. Installer les dépendances (Django & Pillow)
```
pip install django Pillow
```
6. Appliquer les migrations de la base de données
```
python manage.py makemigrations
python manage.py migrate
```

🎯 Lancement de l'application
Pour démarrer le générateur et lancer le serveur de développement local, exécutez la commande suivante dans votre terminal :

```
python manage.py runserver
```
Une fois le serveur actif, ouvrez votre navigateur et rendez-vous à l'adresse suivante :
👉 http://127.0.0.1:8000/

🛡️ Accès Administrateur (Optionnel)
Pour accéder à l'interface d'administration native de Django (/admin), vous pouvez générer un super-utilisateur avec la commande :
```
python manage.py createsuperuser
```
