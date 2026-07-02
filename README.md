# 🌅 Django Todo-List

Une application Web de gestion de tâches (Todo-List) robuste, sécurisée et élégante, développée avec le framework **Django** et habillée avec **Tailwind CSS**. Ce projet a été conçu dans un cadre personnel pour démontrer la maîtrise d'un CRUD complet, d'un système d'authentification utilisateur étanche et de l'extension de modèles.

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
## 🎯 Lancement de l'application (Via Docker Compose)

Plus besoin d'installer Python ou des dépendances localement. Lancez simplement l'application dans son conteneur isolé avec :

```bash
docker compose up --build -d
```
Une fois le serveur actif, ouvrez votre navigateur et rendez-vous à l'adresse suivante :
👉 http://127.0.0.1:8000/

🛡️ Accès Administrateur (Optionnel)
Pour accéder à l'interface d'administration native de Django (/admin), vous pouvez générer un super-utilisateur avec la commande :
```
python manage.py createsuperuser
```
