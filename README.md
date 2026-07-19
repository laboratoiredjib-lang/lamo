# Site web du LAMO

Application Django du **Laboratoire d'Analyse, de Modélisation et d'Optimisation (LAMO)**,
unité de recherche du Centre de Recherche en Mathématiques et Numérique (CRMN) de
l'Université de Djibouti.

Tout le contenu (équipes, thématiques, membres, doctorants, chercheurs associés,
partenaires, actualités, coordonnées) est géré depuis l'**administration Django**,
sans avoir besoin de toucher au code.

## Stack technique

- Python 3.13 / Django 6.0
- SQLite en développement (facilement remplaçable par PostgreSQL en production)
- Aucun framework front externe : CSS et JS maison, sans dépendance à builder

## Démarrage rapide

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt

python manage.py migrate
python manage.py seed_lamo     # charge les données réelles du laboratoire (équipes, membres, partenaires...)
python manage.py runserver
```

Le site est alors disponible sur http://127.0.0.1:8000/

## Administration

Un compte administrateur a été créé :

- URL : http://127.0.0.1:8000/admin/
- Identifiant : `admin`
- Mot de passe : `lamo2026`

**Changez ce mot de passe dès la première connexion** (`python manage.py changepassword admin`).

Depuis l'admin, vous pouvez :

- éditer le profil du laboratoire (présentation, adresse, emails, logo) ;
- ajouter/modifier les équipes et thématiques de recherche ;
- gérer les membres permanents, doctorants et chercheurs associés ;
- ajouter des partenaires (avec leur logo) ;
- publier des actualités.

## Organisation du projet

```
lamo_site/          configuration du projet Django (settings, urls)
lab/                 application principale
  models.py          modèles de données (LabProfile, ResearchTeam, ResearchTheme,
                      PermanentMember, Doctorant, AssociateResearcher, Partner, News)
  views.py / urls.py  pages du site
  templates/lab/      gabarits HTML
  static/lab/         CSS et JS
  management/commands/seed_lamo.py   charge les données réelles du flyer LAMO
seed_media/          logos sources utilisés par la commande seed_lamo
```

## Illustrations

Le bandeau mathématique affiché sur chaque page (`lab/templates/lab/_hero_illustration.html`) et
le motif de réseau (`lab/static/lab/img/network-motif.svg`) sont des créations originales en SVG,
inspirées des thématiques de recherche du LAMO (systèmes dynamiques, probabilités, réseaux,
optimisation, statistique) et de la palette du logo. Aucune image externe n'est utilisée.

## Déploiement en production

Avant mise en ligne, penser à :

- définir `DEBUG = False` et une vraie valeur secrète pour `SECRET_KEY` (variable d'environnement) ;
- renseigner `ALLOWED_HOSTS` avec le nom de domaine réel ;
- passer sur une base PostgreSQL ;
- exécuter `python manage.py collectstatic` et servir `staticfiles/` via le serveur web ;
- servir le dossier `media/` (logos, photos) via le serveur web ou un stockage objet.
