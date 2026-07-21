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

Le projet est prêt pour un hébergement type Render/Railway/Heroku :

- `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS` sont lus depuis des variables d'environnement
  (`lamo_site/settings.py`) — par défaut `DEBUG=True` en local, sans rien à configurer ;
- `DATABASE_URL` est supporté (`dj-database-url`) pour brancher une base PostgreSQL ;
  sans cette variable, l'application utilise SQLite ;
- les fichiers statiques sont servis directement par l'application via **WhiteNoise**
  (pas besoin de serveur web séparé) ;
- `gunicorn` est utilisé comme serveur d'application (`gunicorn lamo_site.wsgi:application`) ;
- `build.sh` installe les dépendances, exécute `collectstatic`, `migrate`, `seed_lamo`
  et `ensure_admin` (crée/actualise le compte admin à partir de `DJANGO_SUPERUSER_USERNAME`
  / `_EMAIL` / `_PASSWORD` si ces variables sont définies).

### Déployé sur Render (plan gratuit)

Le site est hébergé sur Render. **Sur le plan gratuit, le disque n'est pas persistant** :
la base SQLite et les identifiants admin sont régénérés à chaque build à partir de
`seed_lamo` (données du flyer) — toute modification faite depuis `/admin/` entre deux
déploiements peut donc être perdue au redémarrage du service. Pour un usage en production
avec du contenu éditorial durable, brancher une base PostgreSQL (variable `DATABASE_URL`,
disponible aussi en plan gratuit sur Render) est recommandé.
