from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from lab.models import (
    Activity,
    AssociateResearcher,
    Doctorant,
    Habilitation,
    LabProfile,
    Partner,
    PermanentMember,
    Publication,
    ResearchProject,
    ResearchTeam,
    ResearchTheme,
)

SEED_MEDIA = Path(__file__).resolve().parent.parent.parent.parent / "seed_media"


def attach_image(instance, field_name, filename):
    path = SEED_MEDIA / filename
    if not path.exists():
        return
    field = getattr(instance, field_name)
    if field:
        return
    with open(path, "rb") as fh:
        field.save(filename, File(fh), save=True)


class Command(BaseCommand):
    help = "Charge les données réelles du LAMO (profil, équipes, membres, activités, partenaires)."

    def handle(self, *args, **options):
        self.seed_profile()
        team_dyn, team_sto = self.seed_teams()
        self.seed_themes(team_dyn, team_sto)
        self.seed_permanent_members(team_dyn, team_sto)
        self.seed_doctorants()
        self.seed_associates()
        self.seed_activities()
        self.seed_partners()
        self.seed_publications()
        self.seed_research_projects()
        self.seed_habilitations()
        self.stdout.write(self.style.SUCCESS("Données du LAMO chargées avec succès."))

    def seed_profile(self):
        profile = LabProfile.load()
        profile.name = "Laboratoire d'Analyse, de Modélisation et d'Optimisation"
        profile.acronym = "LAMO"
        profile.affiliation = (
            "Centre de Recherche en Mathématiques et Numérique (CRMN), Université de Djibouti"
        )
        profile.mission = (
            "Le Laboratoire d’Analyse, de Modélisation et d’Optimisation (LAMO) est une unité de "
            "recherche affiliée au Centre de Recherche en Mathématiques et Numérique (CRMN) de "
            "l’Université de Djibouti. Il a pour mission de développer des approches en mathématiques "
            "appliquées, statistique, optimisation, simulation numérique et science des données pour "
            "répondre à des problématiques scientifiques, technologiques et socio-économiques."
        )
        profile.presentation_extra = (
            "Le laboratoire regroupe des enseignants-chercheurs, des doctorants, des étudiants en "
            "master et des chercheurs associés autour de projets interdisciplinaires couvrant la "
            "modélisation mathématique, les systèmes dynamiques, les processus stochastiques, "
            "l’analyse de données, l’intelligence artificielle, les méthodes numériques et l’aide à "
            "la décision.\n\n"
            "Ses travaux s’appliquent à des domaines variés tels que la santé publique, les "
            "transports, l’environnement, l’énergie, l’économie et la gestion des risques, "
            "contribuant au développement de solutions innovantes adaptées aux défis de Djibouti et "
            "de la région.\n\n"
            "Le LAMO développe des collaborations avec des centres de recherche, des organismes "
            "publics et des partenaires internationaux, favorisant la recherche collaborative, la "
            "formation et la valorisation des résultats scientifiques."
        )
        profile.teams_intro = (
            "Le Laboratoire d’Analyse, de Modélisation et d’Optimisation (LAMO) est structuré autour "
            "de deux équipes de recherche complémentaires, favorisant les collaborations "
            "interdisciplinaires ainsi que le développement de projets à fort impact scientifique et "
            "socio-économique."
        )
        profile.teams_conclusion = (
            "Les recherches menées au sein des deux équipes du LAMO sont complémentaires et couvrent "
            "un large spectre des mathématiques fondamentales et appliquées. Elles associent le "
            "développement de modèles mathématiques, l’analyse des systèmes dynamiques, le contrôle "
            "optimal, les probabilités, les statistiques, la science des données et les méthodes "
            "computationnelles afin d’apporter des réponses à des problématiques complexes. Cette "
            "complémentarité favorise une approche interdisciplinaire conciliant avancées théoriques, "
            "innovations méthodologiques et applications dans des domaines variés tels que les "
            "sciences du vivant, la santé publique, l’environnement, l’ingénierie, les systèmes "
            "industriels, l’économie et l’aide à la décision. À travers cette organisation, le LAMO "
            "ambitionne de renforcer son excellence scientifique tout en contribuant au développement "
            "socio-économique de Djibouti et de la région."
        )
        profile.address = "Université de Djibouti, Campus de Balbala, Croisement RN2-RN5"
        profile.director_name = "Dr Liban ISMAIL ABDILLAHI"
        profile.email_primary = "lamo@univ.edu.dj"
        profile.email_secondary = "liban_ismail_abdillahi@univ.edu.dj"
        profile.save()
        attach_image(profile, "logo", "logo_lamo.png")
        attach_image(profile, "university_logo", "logo_universite_djibouti.png")

    def seed_teams(self):
        team_dyn, _ = ResearchTeam.objects.update_or_create(
            slug="systemes-dynamiques-controle",
            defaults={
                "name": "Systèmes Dynamiques et Contrôle (SDC)",
                "short_description": (
                    "Modèles mathématiques, méthodes d’analyse et stratégies de contrôle pour les "
                    "systèmes complexes."
                ),
                "description": (
                    "Cette équipe développe des recherches en mathématiques fondamentales et "
                    "appliquées, avec pour objectif de concevoir des modèles mathématiques, des "
                    "méthodes d’analyse et des stratégies de contrôle pour les systèmes complexes. Ses "
                    "travaux reposent sur des approches théoriques, analytiques et numériques, avec "
                    "des applications dans les sciences du vivant, l’environnement, l’ingénierie et "
                    "les systèmes industriels."
                ),
                "order": 1,
            },
        )
        team_sto, _ = ResearchTeam.objects.update_or_create(
            slug="stochastiques-sciences-donnees",
            defaults={
                "name": "Stochastique et Sciences des Données (SSD)",
                "short_description": (
                    "Modélisation des phénomènes aléatoires, analyse statistique et exploitation des "
                    "données massives."
                ),
                "description": (
                    "Cette équipe mène des recherches consacrées à la modélisation des phénomènes "
                    "aléatoires, à l’analyse statistique et à l’exploitation des données massives. "
                    "Elle développe des approches probabilistes, statistiques et computationnelles "
                    "pour l’analyse des systèmes complexes et l’aide à la décision dans des domaines "
                    "variés."
                ),
                "order": 2,
            },
        )
        return team_dyn, team_sto

    def seed_themes(self, team_dyn, team_sto):
        # Les axes ont été redéfinis (3 par équipe) : on repart d'une base propre.
        ResearchTheme.objects.all().delete()
        themes = [
            (
                "Modélisation et analyse des systèmes dynamiques",
                (
                    "Cet axe couvre la modélisation mathématique de phénomènes issus des sciences du "
                    "vivant, de la physique, de l’environnement et de l’ingénierie. Il inclut l’étude "
                    "qualitative et quantitative des équations différentielles et des modèles "
                    "évolutifs, ainsi que l’analyse de la stabilité, des bifurcations et des "
                    "comportements asymptotiques des systèmes dynamiques."
                ),
                team_dyn, 1,
            ),
            (
                "Contrôle optimal et méthodes numériques",
                (
                    "Cet axe porte sur le développement de stratégies de contrôle pour les systèmes "
                    "dynamiques, notamment sous contraintes, ainsi que sur la conception d’algorithmes "
                    "numériques pour la simulation, l’optimisation et la résolution de problèmes "
                    "complexes."
                ),
                team_dyn, 2,
            ),
            (
                "Structures algébriques et fondements théoriques",
                (
                    "Cet axe est consacré à l’étude des structures algébriques avancées, telles que la "
                    "théorie des groupes, les algèbres et les groupes quantiques. Il inclut également "
                    "l’analyse des extensions et des interactions entre structures algébriques "
                    "classiques et généralisées, contribuant ainsi à renforcer les fondements "
                    "théoriques de la modélisation mathématique."
                ),
                team_dyn, 3,
            ),
            (
                "Modélisation stochastique et quantification des incertitudes",
                (
                    "Cet axe couvre la théorie des probabilités, les processus stochastiques et la "
                    "modélisation des phénomènes aléatoires. Il s’intéresse également à la "
                    "quantification des incertitudes, à l’analyse de sensibilité, à la fiabilité des "
                    "modèles et à la prise en compte des aléas dans les systèmes complexes."
                ),
                team_sto, 4,
            ),
            (
                "Statistiques, inférence et analyse des données",
                (
                    "Cet axe est consacré au développement de méthodes statistiques pour l’inférence, "
                    "l’estimation, la calibration et la validation des modèles. Il couvre également "
                    "l’analyse exploratoire des données, les méthodes de classification, la prévision, "
                    "l’analyse multivariée et les approches quantitatives destinées à l’extraction "
                    "d’information à partir des données."
                ),
                team_sto, 5,
            ),
            (
                "Science des données et méthodes computationnelles",
                (
                    "Cet axe porte sur la collecte, la gestion, l’analyse et la valorisation de "
                    "données complexes ou de grande dimension. Il intègre le développement de méthodes "
                    "numériques, statistiques et algorithmiques, ainsi que la conception d’outils "
                    "d’aide à la décision fondés sur l’exploitation des données et le calcul "
                    "scientifique."
                ),
                team_sto, 6,
            ),
        ]
        for title, description, team, order in themes:
            ResearchTheme.objects.update_or_create(
                title=title, defaults={"description": description, "team": team, "order": order}
            )

    def seed_permanent_members(self, team_dyn, team_sto):
        members = [
            ("Dr. Liban ISMAIL", "Maître de conférences en Mathématiques appliquées", "", True, team_dyn,
             "", "", "",
             "Directeur du LAMO. Ses travaux portent sur la modélisation et le contrôle de systèmes dynamiques complexes, avec des collaborations internationales autour de l'encadrement doctoral."),
            ("Dr. Yahyeh SOULEIMAN", "Maître de conférences en Mathématiques appliquées",
             "Doyen de l'IUT-T", False, team_sto,
             "yahyeh_souleiman@univ.edu.dj", "souleimanyahyeh@gmail.com", "+253 77 86 80 46 | +253 21 32 36 03",
             "Dr. Yahyeh SOULEIMAN est Maître de Conférences en Mathématiques Appliquées et Doyen de "
             "l'Institut Universitaire de Technologie Tertiaire (IUT-T) au Laboratoire d'Analyse, "
             "Modélisation et Optimisation (LAMO), Université de Djibouti. Mathématicien appliqué avec "
             "14 ans d'expérience dans l'enseignement supérieur et la recherche, son expertise porte sur "
             "la modélisation mathématique, l'analyse de données et l'optimisation dans les secteurs de "
             "la santé publique et de l'environnement. Il fait également preuve de leadership en tant "
             "que responsable de groupes de recherche, membre du comité éditorial de Applied Mathematics "
             "and Statistics (PJAMS), réviseur de plusieurs articles pour différentes revues "
             "internationales et directeur de thèses doctorales. Auteur de plusieurs publications "
             "évaluées par les pairs, il est également intervenant régulier lors de conférences "
             "scientifiques internationales."),
            ("Dr. Souleiman OMAR", "Maître de conférences en Mathématiques fondamentales", "", False, team_dyn,
             "", "", "",
             "Travaux en analyse mathématique et systèmes dynamiques, au service de la modélisation de phénomènes complexes."),
            ("Dr. Doualeh ABDILLAHI", "Maître de conférences en Statistiques appliquées", "", False, team_sto,
             "", "", "",
             "Spécialiste de statistique appliquée et de science des données, au service de projets interdisciplinaires du laboratoire."),
        ]
        for order, (full_name, title, role_tag, is_director, team, email, email_secondary, phone, bio) in enumerate(members, start=1):
            PermanentMember.objects.update_or_create(
                full_name=full_name,
                defaults={
                    "title": title, "role_tag": role_tag, "is_director": is_director, "team": team,
                    "email": email, "email_secondary": email_secondary, "phone": phone,
                    "bio": bio, "order": order,
                },
            )
        yahyeh = PermanentMember.objects.filter(full_name="Dr. Yahyeh SOULEIMAN").first()
        if yahyeh:
            attach_image(yahyeh, "photo", "member_yahyeh_souleiman.jpg")

    def seed_doctorants(self):
        rows = [
            ("M. Said ISMAIL", "2023", "Université Le Havre (LMAH)", "B. Ambrosio & M.A. Aziz Alaoui", "Yahyeh Souleiman",
             "Cette thèse de doctorat s'inscrit dans le domaine des mathématiques appliquées, avec une "
             "orientation vers l'analyse des systèmes dynamiques et des réseaux complexes.\n\n"
             "Le sujet porte sur l'analyse théorique et numérique des systèmes dynamiques et des réseaux "
             "complexes, avec des applications en neurosciences. L'objectif principal est de développer "
             "des modèles mathématiques capables de décrire et d'analyser les comportements collectifs "
             "émergents dans les réseaux complexes, en particulier ceux inspirés des réseaux neuronaux, "
             "tout en proposant des méthodes numériques adaptées à leur étude.\n\n"
             "Ce travail est réalisé dans le cadre d'une collaboration scientifique entre le Laboratoire "
             "d'Analyse, de Modélisation et d'Optimisation (LAMO) de l'Université de Djibouti et le "
             "Laboratoire de Mathématiques Appliquées du Havre (LMAH). Cette collaboration favorise les "
             "échanges scientifiques et le développement d'approches interdisciplinaires.\n\n"
             "Les recherches mobilisent des outils d'analyse des systèmes dynamiques, de modélisation "
             "mathématique et de simulation numérique afin de mieux comprendre les mécanismes collectifs "
             "à l'origine des comportements émergents dans les réseaux neuronaux."),
            ("M. Ali MOHAMED", "2024", "Université La Rochelle (LMIA)", "S. Kadri-Harouna & Kaïs Ammari", "Liban Ismail",
             "Cette thèse de doctorat porte sur le développement de méthodes multi-échelles pour le "
             "contrôle et l'approximation numérique des équations aux dérivées partielles, avec une "
             "application particulière à l'équation des ondes.\n\n"
             "L'objectif est de concevoir des schémas numériques capables de préserver les propriétés "
             "fondamentales du système continu, notamment l'observabilité et la contrôlabilité, tout en "
             "limitant les effets des hautes fréquences responsables de la perte d'observabilité dans les "
             "méthodes classiques.\n\n"
             "Les recherches combinent des approches théoriques et numériques fondées sur les bases "
             "d'ondelettes et les méthodes de Galerkin multi-échelles afin de développer des méthodes de "
             "discrétisation performantes pour les systèmes distribués.\n\n"
             "Les premiers résultats ont conduit à une publication dans les actes de la conférence IFAC "
             "ainsi qu'à plusieurs communications scientifiques internationales. Les travaux se "
             "poursuivent vers l'extension des méthodes proposées à des modèles multidimensionnels et à "
             "d'autres classes d'équations d'évolution aux équations aux dérivées partielles."),
            ("M. Gouled SOULEIMAN", "2024", "Université Le Havre (LMAH)", "N. Verdière & A. Berred", "Yahyeh Souleiman",
             "Cette thèse de doctorat s'inscrit dans le domaine des mathématiques appliquées et des "
             "sciences de l'environnement. Elle porte sur la modélisation des écosystèmes forestiers et "
             "l'analyse de l'impact des espèces invasives dans un contexte de changements climatiques.\n\n"
             "L'objectif principal est de développer des modèles mathématiques permettant de mieux "
             "comprendre les interactions entre les espèces natives et les espèces invasives, ainsi que "
             "leur influence sur la stabilité, la résilience et la régénération des écosystèmes "
             "forestiers.\n\n"
             "Ce travail est réalisé dans le cadre d'une collaboration scientifique entre le Laboratoire "
             "d'Analyse, de Modélisation et d'Optimisation (LAMO) et le Laboratoire de Mathématiques "
             "Appliquées du Havre (LMAH), favorisant le développement d'approches interdisciplinaires en "
             "modélisation écologique.\n\n"
             "Les recherches mobilisent des outils de modélisation mathématique, de systèmes dynamiques "
             "et de simulation numérique afin d'analyser les mécanismes d'invasion biologique et "
             "d'évaluer l'impact des changements climatiques sur la biodiversité et la durabilité des "
             "écosystèmes forestiers."),
            ("Mme. Saida BALLAH", "2024", "Université de Nantes (ONIRIS)", "Mohamed Hanafi", "Souleiman Omar",
             "Cette thèse de doctorat s'inscrit dans le domaine de la statistique, de la modélisation et "
             "de l'intelligence artificielle appliquées aux sciences du vivant et aux géosciences.\n\n"
             "Le sujet porte sur le développement d'approches tensorielles pour l'analyse de données "
             "multi-blocs. L'objectif est de concevoir des méthodes statistiques innovantes capables "
             "d'exploiter efficacement des ensembles de données complexes et de grande dimension à "
             "l'aide des représentations tensorielles.\n\n"
             "Réalisé en collaboration avec l'École nationale vétérinaire, agroalimentaire et de "
             "l'alimentation de Nantes-Atlantique (Oniris), ce travail contribue au développement de "
             "nouvelles méthodes d'analyse de données adaptées aux problématiques interdisciplinaires "
             "des sciences du vivant.\n\n"
             "Les recherches visent à développer des outils méthodologiques robustes en statistique "
             "multivariée, intelligence artificielle et apprentissage automatique, avec des applications "
             "à des données réelles issues des sciences appliquées."),
            ("M. Getachew FETENE", "2025", "Adama Science and Technology University", "Lemecha Legesse", "Yahyeh Souleiman", ""),
            ("M. Hakim AMER", "2026", "Université de Toulon", "Mehmet Ersoy", "Liban Ismail & Mohamed Yacin",
             "Cette thèse porte sur la modélisation hydrodynamique et sédimentaire des processus "
             "d'érosion côtière, avec une application au littoral djiboutien.\n\n"
             "L'objectif est de développer un modèle mathématique capable de représenter les "
             "interactions entre l'hydrodynamique (houle, courants et marées) et la dynamique "
             "sédimentaire afin de mieux comprendre et prévoir l'évolution du trait de côte dans un "
             "contexte de changement climatique.\n\n"
             "Le projet adopte une approche interdisciplinaire intégrant les effets des forçages "
             "climatiques et anthropiques sur les systèmes côtiers. Une attention particulière est "
             "portée à la collecte, au traitement et à l'analyse des données bathymétriques, "
             "météorologiques, océanographiques et satellitaires nécessaires à la calibration et à la "
             "validation des modèles.\n\n"
             "Les simulations numériques sont réalisées à l'aide du modèle CROCO (Coastal and Regional "
             "Ocean Community Model). Les résultats attendus permettront d'améliorer la compréhension "
             "des mécanismes d'érosion côtière et de proposer des outils d'aide à la décision pour une "
             "gestion durable du littoral djiboutien."),
            ("M. Kadir ALI", "2027", "Université Marie et Louis Pasteur (LmB)", "Raluca Eftimie", "Yahyeh Souleiman",
             "Cet encadrement doctoral concerne la thèse de doctorat de Kadir Ali Moussa, réalisée dans "
             "le cadre d'une cotutelle internationale entre l'Université de Djibouti et l'Université "
             "Marie et Louis Pasteur (France).\n\n"
             "Le projet de recherche porte sur la modélisation mathématique multi-échelle des "
             "infections à papillomavirus humain (HPV), avec pour objectif d'étudier les mécanismes "
             "biologiques impliqués dans la persistance de l'infection et son évolution vers les "
             "lésions précancéreuses et les cancers associés. Les travaux visent à développer un "
             "modèle intégrant différents niveaux d'organisation biologique, allant des interactions "
             "cellulaires jusqu'à la dynamique de transmission au sein des populations. Cette approche "
             "permettra d'analyser les facteurs influençant la progression de l'infection ainsi que "
             "l'impact des stratégies de prévention et de dépistage.\n\n"
             "La direction scientifique est assurée par le Pr Raluca Eftimie, avec un co-encadrement "
             "assuré par le Dr Yahyeh Souleiman. Les recherches s'appuient sur des outils avancés de "
             "modélisation mathématique, de systèmes dynamiques, d'analyse qualitative et de simulation "
             "numérique. Cette thèse contribue au développement des activités du LAMO dans le domaine "
             "de la biomathématique et renforce les collaborations scientifiques internationales du "
             "laboratoire."),
            ("M. Ismail ABDILLAHI", "2027", "Université Clermont Auvergne", "Pr Andrzej Stos & Pr Thierry Chateau", "Liban Ismail",
             "Cet encadrement doctoral concerne la thèse de M. Ismail ABDILLAHI, qui débutera au cours "
             "de l'année universitaire 2026–2027 dans le cadre d'une collaboration scientifique entre "
             "l'Université de Djibouti et l'Université Clermont Auvergne.\n\n"
             "Le projet de recherche porte sur la fiabilité des réseaux neuronaux face aux "
             "perturbations affectant les processus d'apprentissage, avec pour objectif de développer "
             "des méthodes permettant d'évaluer, d'analyser et d'améliorer la robustesse des modèles "
             "d'intelligence artificielle. Les travaux s'intéresseront notamment aux perturbations "
             "naturelles des données d'apprentissage, telles que les erreurs d'annotation, les biais de "
             "labellisation et les divergences entre annotateurs, ainsi qu'aux perturbations "
             "malveillantes liées aux attaques par empoisonnement des données et aux mécanismes de "
             "type backdoor. Les recherches mobiliseront des approches combinant apprentissage "
             "automatique, statistiques, méthodes d'explicabilité et expérimentation numérique afin de "
             "caractériser la fiabilité des modèles et de proposer des critères d'évaluation adaptés "
             "aux situations où les données de référence sont incomplètes ou incertaines.\n\n"
             "L'encadrement scientifique est assuré par les Professeurs Thierry Chateau et Andrzej "
             "Stos, avec un co-encadrement assuré par le Dr Liban Ismail au sein du LAMO. Cette thèse "
             "contribuera au développement de nouvelles approches pour la conception de systèmes "
             "d'intelligence artificielle plus robustes, fiables et interprétables."),
            ("M. Mohamed Ismael DINI", "2027", "Adama Science and Technology University (ASTU)", "Legesse Lemecha", "Yahyeh Souleiman & Liban Ismail",
             "Cet encadrement doctoral concerne la thèse de M. Mohamed Ismael Dini, qui débutera au "
             "cours de l'année universitaire 2026–2027 dans le cadre d'une collaboration scientifique "
             "entre l'Université de Djibouti et Adama Science and Technology University (ASTU).\n\n"
             "Le projet de recherche porte sur les aspects épidémiologiques, les facteurs "
             "sociodémographiques influents et l'analyse spatio-temporelle du paludisme à "
             "Djibouti-ville. L'objectif principal est de développer une meilleure compréhension de la "
             "dynamique de transmission du paludisme à travers l'analyse intégrée des données "
             "épidémiologiques, spatiales et temporelles, afin d'identifier les zones à risque et les "
             "facteurs déterminants de la propagation de la maladie.\n\n"
             "Les travaux s'intéresseront notamment à l'étude de la distribution spatiale et saisonnière "
             "des cas de paludisme, à l'identification des facteurs sociodémographiques et "
             "environnementaux associés à la transmission, ainsi qu'à l'évaluation de l'influence de "
             "l'accès aux services de santé sur l'évolution de la maladie. Les recherches mobiliseront "
             "des approches combinant épidémiologie, statistiques, analyse spatiale, modélisation "
             "mathématique et méthodes quantitatives d'aide à la décision afin de développer des outils "
             "permettant d'améliorer les stratégies de surveillance, de prévention et de contrôle du "
             "paludisme à Djibouti.\n\n"
             "L'encadrement scientifique sera assuré par le Pr Legesse Lemecha, avec un co-encadrement "
             "assuré par le Dr Yahyeh Souleiman et le Dr Liban Ismail au sein du LAMO. Cette thèse "
             "contribuera au développement des recherches en biomathématique, en modélisation "
             "épidémiologique et en santé publique, tout en renforçant les collaborations scientifiques "
             "internationales du laboratoire."),
            ("M. Abdourahman Djama GUEDI", "2027", "Adama Science and Technology University (ASTU)", "Legesse Lemecha", "Yahyeh Souleiman & Liban Ismail",
             "Cet encadrement doctoral concerne la thèse de M. Abdourahman Djama Guedi, qui débutera au "
             "cours de l'année universitaire 2026–2027 dans le cadre d'une collaboration scientifique "
             "entre l'Université de Djibouti et Adama Science and Technology University (ASTU).\n\n"
             "Le projet de recherche porte sur l'épidémiologie de la brucellose humaine chez les "
             "populations à risque à Djibouti : séroprévalence et identification des facteurs de "
             "risque. L'objectif est d'évaluer la charge réelle de cette zoonose émergente dans les "
             "populations exposées et d'identifier les principaux facteurs professionnels, "
             "comportementaux et alimentaires associés à l'infection.\n\n"
             "Les travaux s'intéresseront notamment à la mesure de la séroprévalence des anticorps "
             "anti-Brucella chez les groupes à haut risque, tels que les éleveurs, vétérinaires, "
             "bouchers et consommateurs de produits laitiers non pasteurisés, ainsi qu'à l'analyse des "
             "pratiques favorisant la transmission de la maladie. Les recherches mobiliseront des "
             "approches combinant épidémiologie, biostatistiques, analyse des facteurs de risque, "
             "modélisation mathématique et approche intégrée « Une seule santé (One Health) » afin de "
             "mieux comprendre l'interaction entre les facteurs humains, animaux et environnementaux.\n\n"
             "L'encadrement scientifique sera assuré par le Pr Legesse Lemecha, avec un co-encadrement "
             "assuré par le Dr Yahyeh Souleiman et le Dr Liban Ismail au sein du LAMO. Cette thèse "
             "contribuera au développement des recherches en biomathématique, en modélisation des "
             "maladies infectieuses et en santé publique, tout en apportant des connaissances "
             "essentielles pour l'amélioration des stratégies de surveillance et de prévention de la "
             "brucellose à Djibouti."),
        ]
        for order, (full_name, start_year, partner_university, thesis_director, co_supervisor, bio) in enumerate(rows, start=1):
            Doctorant.objects.update_or_create(
                full_name=full_name,
                defaults={
                    "start_year": start_year,
                    "partner_university": partner_university,
                    "thesis_director": thesis_director,
                    "co_supervisor": co_supervisor,
                    "bio": bio or f"Thèse en cotutelle avec {partner_university}, sous la direction de {thesis_director}.",
                    "order": order,
                },
            )

    def seed_associates(self):
        rows = [
            ("M. Hacène DJELLOUT", "Professeur", "Université Clermont Auvergne (UCA)", "France"),
            ("Mme. Raluca EFTIMIE", "Professeure", "Université Marie et Louis Pasteur", "France"),
            ("Mme. Nathalie VERDIÈRE", "Professeure", "Université Le Havre Normandie", "France"),
            ("M. Abdisalam HASSAN", "Professeur", "Université AMOUD", "Somalie"),
            ("M. Lemecha LEGESSE", "Professeur", "Adama Science and Technology University", "Éthiopie"),
        ]
        for order, (full_name, grade, institution, country) in enumerate(rows, start=1):
            AssociateResearcher.objects.update_or_create(
                full_name=full_name,
                defaults={
                    "grade": grade,
                    "institution": institution,
                    "country": country,
                    "bio": f"Chercheur associé au LAMO, {grade.lower()} à {institution}.",
                    "order": order,
                },
            )

    def seed_activities(self):
        conference, _ = Activity.objects.update_or_create(
            category=Activity.Category.CONFERENCE,
            title="M2ISDA — Mathematical Modeling and Innovations in Advanced Data Science",
            defaults={
                "edition_label": "2e édition",
                "year": "19–21 janvier 2027",
                "description": (
                    "Conférence internationale organisée par le LAMO et l'Université de Djibouti, "
                    "réunissant chercheurs, doctorants et professionnels autour des avancées récentes "
                    "en modélisation mathématique, statistique et science des données. Thèmes abordés : "
                    "épidémiologie mathématique, optimisation, modélisation environnementale et "
                    "logistique portuaire, aide à la décision."
                ),
                "link": "https://urls.fr/SHONvz",
                "order": 2,
            },
        )
        attach_image(conference, "image", "activity_m2isda_2027_poster.jpg")

        Activity.objects.update_or_create(
            category=Activity.Category.CONFERENCE,
            title="Conférence LAMO",
            defaults={"edition_label": "1ère édition", "year": "2024", "order": 1},
        )

        for order, year in enumerate(["2025", "2026"], start=1):
            Activity.objects.update_or_create(
                category=Activity.Category.OLYMPIADES,
                title="Olympiades de mathématiques",
                edition_label=f"Édition {year}",
                defaults={"year": "", "order": order},
            )

    def seed_partners(self):
        academic = [
            ("Université La Rochelle", "partner_la_rochelle.png", "France"),
            ("Université Marie et Louis Pasteur", "partner_marie_louis_pasteur.png", "France"),
            ("Adama Science and Technology University", "partner_adama.png", "Éthiopie"),
            ("Université Clermont Auvergne", "partner_clermont_auvergne.jpeg", "France"),
            ("Université Le Havre Normandie", "partner_le_havre_normandie.png", "France"),
            ("Université de Toulon", "partner_toulon.png", "France"),
            ("Université de Nantes", "partner_nantes.png", "France"),
            ("Amoud University", "partner_amoud.png", "Somalie"),
            ("Université de Lorraine", "partner_lorraine.png", "France"),
        ]
        institutional = [
            ("Institut National de Santé Publique de Djibouti", "partner_inspd.png", "Djibouti"),
            ("INSTAD - Institut National de la Statistique de Djibouti", "partner_instad.png", "Djibouti"),
            ("DPCS - Djibouti Port Community Systems", "partner_dpcs.png", "Djibouti"),
            ("Service de Santé des Armées", "partner_service_sante_armees.png", "Djibouti"),
            ("DPCR - Djibouti Ports Corridor Road", "partner_dpcr.png", "Djibouti"),
            ("SGTD - Société de Gestion du Terminal à Conteneurs de Doraleh", "partner_sgtd.png", "Djibouti"),
        ]
        for order, (name, filename, country) in enumerate(academic, start=1):
            partner, _ = Partner.objects.update_or_create(
                name=name,
                defaults={"category": Partner.Category.ACADEMIC, "country": country, "order": order},
            )
            attach_image(partner, "logo", filename)

        for order, (name, filename, country) in enumerate(institutional, start=1):
            partner, _ = Partner.objects.update_or_create(
                name=name,
                defaults={"category": Partner.Category.INSTITUTIONAL, "country": country, "order": order},
            )
            attach_image(partner, "logo", filename)

    def seed_publications(self):
        rows = [
            ("Haile Getachew Fetene, Yahyeh Souleiman, and Legesse Lemecha Obsu",
             "A Fractional Mathematical Model of Malaria Transmission Dynamics with Liver Stage Relapse",
             "Discover Applied Sciences, 2026", False, "https://doi.org/10.1007/s42452-026-09116-9", "DOI"),
            ("Yahyeh Souleiman, Liban Ismail, and Legesse Lemecha Obsu",
             "Optimal Control Strategies and Cost-Effectiveness Analysis of Malaria for Plasmodium falciparum and Plasmodium vivax in Djibouti",
             "Scientific African, 31 (2026): e03262", False, "https://doi.org/10.1016/j.sciaf.2026.e03262", "DOI"),
            ("Yahyeh Souleiman, Liban Ismail, and Raluca Eftimie",
             "Modeling and Investigating Plasmodium falciparum and Plasmodium vivax Infections: Application to Djibouti Data",
             "Infectious Disease Modelling, 9(4) (2024): 1095–1116", False, "https://doi.org/10.1016/j.idm.2024.05.005", "DOI"),
            ("Liban Ismail, Hacène Djellout, and Cédric Chauvière",
             "Global Sensitivity Analysis in the SIHR Epidemiological Model with Application to COVID-19",
             "Journal of Statistics & Management Systems, 27(7) (2024): 1277–1299", False, "https://doi.org/10.47974/JSMS-1019", "DOI"),
            ("Liban Ismail, Hacène Djellout, and Cédric Chauvière",
             "Climate System: A Global Sensitivity Approach",
             "Iranian Journal of Science, 47(1) (2023): 211–227", False, "https://doi.org/10.1007/s40995-022-01456-4", "DOI"),
            ("Yahyeh Souleiman, Abdoulrazack Mohamed, and Liban Ismail",
             "Analysis of the Dynamics of the SIHR Model: COVID-19 Case in Djibouti",
             "Applied Mathematics, 12(10) (2021): 867–881", False, "https://doi.org/10.4236/am.2021.1210058", "DOI"),
            ("Liban Ismail, Yahyeh Souleiman, Saralees Nadarajah, and Abdisalam Hassan",
             "Time-Dependent Intervention Modeling and Global Sensitivity Analysis of Epidemic Dynamics under Uncertainty in Resource-Limited African Settings",
             "À paraître", True, "", ""),
            ("Gouled Souleiman, Nathalie Verdière, Alexandre Berred, Yahyeh Souleiman, Simon Badji, et al.",
             "Optimal Control and Calibration Modeling of Forest Regeneration Under Anthropogenic Pressures: the Day Forest Ecosystem (Djibouti)",
             "Modeling Earth Systems and Environment, 2026 — à paraître", True, "https://hal.science/", "HAL"),
            ("Said Ismail, Benjamin Ambrosio, Moulay Ahmed Aziz-Alaoui, and Yahyeh Souleiman",
             "A Dynamical System Approach to Modeling Neural Network Activity in Drosophila Orientation",
             "À paraître", True, "", ""),
            ("Gouled Souleiman, Nathalie Verdière, Alexandre Berred, and Yahyeh Souleiman",
             "A Mathematical Model to Investigate the Impact of Climate Change on Forest Ecosystems and a Strategy for Its Regeneration",
             "À paraître", True, "", ""),
            ("Yahyeh Souleiman",
             "Convergences and Numerical Analysis of a Contact Problem with Normal Compliance and Unilateral Constraint",
             "African Journal of Mathematics and Computer Science Research, 14(1) (2021): 13–23", False, "https://doi.org/10.5897/AJMCSR2020.0865", "DOI"),
            ("Yahyeh Souleiman and Mikael Barboteu",
             "Numerical Analysis of a Sliding Frictional Contact Problem with Normal Compliance and Unilateral Contact",
             "Open Journal of Modelling and Simulation, 9(4) (2021): 385–402", False, "https://doi.org/10.4236/ojmsi.2021.94025", "DOI"),
            ("Mircea Sofonea and Yahyeh Souleiman",
             "Analysis of a Sliding Frictional Contact Problem with Unilateral Constraint",
             "Mathematics and Mechanics of Solids, 22(3) (2017): 324–342", False, "https://doi.org/10.1177/1081286515591304", "DOI"),
            ("Mircea Sofonea, Flavius Pétrulescu, and Yahyeh Souleiman",
             "Analysis of a Contact Problem with Wear and Unilateral Constraint",
             "Applicable Analysis, 95(11) (2016): 2590–2607", False, "https://doi.org/10.1080/00036811.2015.1102892", "DOI"),
            ("Mircea Sofonea and Yahyeh Souleiman",
             "A Viscoelastic Sliding Contact Problem with Normal Compliance, Unilateral Constraint and Memory Term",
             "Mediterranean Journal of Mathematics, 13(5) (2016): 2863–2886", False, "https://doi.org/10.1007/s00009-015-0661-9", "DOI"),
            ("Alexandru Chirvasitu and Souleiman Omar Hoch",
             "Ergodic Actions of the Compact Quantum Group O₋₁(2)",
             "arXiv Preprint, 2017", False, "https://arxiv.org/", "arXiv"),
            ("Alexandru Chirvasitu, Souleiman Omar Hoch, and Paweł Kasprzak",
             "Fundamental Isomorphism Theorems for Quantum Groups",
             "Expositiones Mathematicae", False, "https://doi.org/10.1016/j.exmath.2019.02.002", "DOI"),
        ]
        for order, (authors, title, reference, forthcoming, link, link_label) in enumerate(rows, start=1):
            Publication.objects.update_or_create(
                title=title,
                defaults={
                    "authors": authors, "reference": reference, "is_forthcoming": forthcoming,
                    "link": link, "link_label": link_label, "order": order,
                },
            )

    def seed_research_projects(self):
        completed, _ = ResearchProject.objects.update_or_create(
            title=(
                "Modélisation mathématique des maladies chroniques et du paludisme à Djibouti : analyse "
                "dynamique et aide à la décision en santé publique"
            ),
            defaults={
                "funder": "Centre d'Excellence Africain en Logistique et Transport (CEALT)",
                "period": "2022–2024",
                "amount": "30 000 USD",
                "status": ResearchProject.Status.COMPLETED,
                "description": (
                    "Ce projet constitue l'un des principaux projets achevés du LAMO. Il s'inscrit dans "
                    "une démarche de recherche appliquée dédiée à la modélisation des maladies chroniques "
                    "et du paludisme à Djibouti. Il visait principalement à analyser la dynamique de "
                    "propagation de ces pathologies, à comprendre les mécanismes de transmission "
                    "sous-jacents et à évaluer l'impact de différentes stratégies d'intervention en santé "
                    "publique afin de fournir des outils d'aide à la décision aux autorités sanitaires.\n\n"
                    "Les travaux réalisés ont permis de développer des modèles mathématiques adaptés au "
                    "contexte épidémiologique local, d'analyser les propriétés qualitatives et "
                    "quantitatives des systèmes dynamiques associés, ainsi que d'étudier les conditions "
                    "de stabilité et les comportements asymptotiques. Des simulations numériques ont "
                    "également été effectuées afin d'évaluer différents scénarios d'évolution et "
                    "d'intervention.\n\n"
                    "Ce projet a abouti à deux résultats scientifiques majeurs, matérialisés par des "
                    "publications internationales dans des revues indexées de haut niveau. Cette "
                    "contribution confirme la pertinence des approches de modélisation mathématique "
                    "comme outil d'aide à la décision en santé publique et a renforcé la visibilité "
                    "scientifique du LAMO ainsi que son expertise en modélisation épidémiologique."
                ),
                "order": 1,
            },
        )
        related_titles = [
            "Optimal Control Strategies and Cost-Effectiveness Analysis of Malaria for Plasmodium falciparum and Plasmodium vivax in Djibouti",
            "Modeling and Investigating Plasmodium falciparum and Plasmodium vivax Infections: Application to Djibouti Data",
        ]
        completed.related_publications.set(Publication.objects.filter(title__in=related_titles))

        ResearchProject.objects.update_or_create(
            title=(
                "Modélisation mathématique de la co-infection tuberculose–VIH/SIDA à Djibouti : dynamique "
                "de transmission et stratégies optimales de contrôle"
            ),
            defaults={
                "funder": "Agence Universitaire de la Francophonie (AUF)",
                "period": "2026 – en cours",
                "amount": "29 500 USD",
                "status": ResearchProject.Status.ONGOING,
                "description": (
                    "Ce projet constitue l'un des projets phares actuellement en cours de développement "
                    "au sein du LAMO. Il s'inscrit dans le domaine de la biomathématique appliquée et "
                    "vise à analyser de manière approfondie la dynamique de la co-infection "
                    "tuberculose–VIH/SIDA à Djibouti.\n\n"
                    "L'objectif scientifique est de mieux comprendre les interactions entre ces deux "
                    "pathologies et de proposer des stratégies optimales de contrôle permettant de "
                    "réduire leur propagation et d'améliorer l'efficacité des politiques de santé "
                    "publique. La problématique étudiée est particulièrement importante en raison de la "
                    "complexité des interactions entre la tuberculose et le VIH/SIDA, ainsi que de leur "
                    "impact combiné sur le système immunitaire et sur la dynamique de transmission au "
                    "sein des populations.\n\n"
                    "Le projet repose sur la formulation de modèles compartimentaux couplés décrivant la "
                    "dynamique de la co-infection, suivie de l'étude des propriétés mathématiques "
                    "fondamentales telles que l'existence, l'unicité et la positivité des solutions. Une "
                    "attention particulière est accordée à l'analyse des points d'équilibre et à leur "
                    "stabilité, ainsi qu'à l'intégration de stratégies de contrôle optimal dans les "
                    "systèmes dynamiques.\n\n"
                    "Des simulations numériques sont également mises en œuvre afin d'évaluer différents "
                    "scénarios épidémiologiques et de comparer l'efficacité des stratégies de prévention "
                    "et de traitement. Ce projet devrait contribuer au renforcement de la production "
                    "scientifique du laboratoire, au développement de nouvelles collaborations "
                    "internationales et à la formation de jeunes chercheurs dans le domaine de la "
                    "modélisation mathématique appliquée à la santé publique."
                ),
                "order": 2,
            },
        )

    def seed_habilitations(self):
        Habilitation.objects.update_or_create(
            full_name="Yahyeh SOULEIMAN",
            defaults={
                "period_label": "2027–2028",
                "garant": "Pr Raluca Eftimie",
                "institutions": "Université de Djibouti – Université Marie et Louis Pasteur (France)",
                "specialization": (
                    "Modélisation mathématique, biomathématique, systèmes dynamiques, calcul "
                    "fractionnaire, contrôle optimal et analyse numérique."
                ),
                "description": (
                    "Les travaux de l'HDR visent à synthétiser les contributions scientifiques "
                    "développées au cours des dernières années dans les domaines de la modélisation des "
                    "maladies infectieuses, de la modélisation environnementale, de l'analyse des "
                    "systèmes dynamiques et de l'aide à la décision. Ils mettent en évidence les avancées "
                    "méthodologiques relatives à l'analyse qualitative des modèles, à l'identification "
                    "des paramètres, à l'analyse de sensibilité, aux méthodes numériques et aux "
                    "stratégies de contrôle optimal.\n\n"
                    "Réalisée sous la responsabilité scientifique du Pr Raluca Eftimie, cette HDR "
                    "s'inscrit dans le cadre d'une collaboration entre l'Université de Djibouti et "
                    "l'Université Marie et Louis Pasteur (France). Elle contribue au renforcement des "
                    "coopérations scientifiques internationales et au développement des activités de "
                    "recherche du Laboratoire d'Analyse, de Modélisation et d'Optimisation (LAMO).\n\n"
                    "Cette habilitation a pour objectif de démontrer la capacité du candidat à conduire "
                    "des recherches de manière autonome, à définir de nouveaux axes scientifiques et à "
                    "encadrer des travaux doctoraux. Elle permettra de consolider les activités de "
                    "recherche du LAMO, de renforcer l'encadrement des doctorants et de développer de "
                    "nouvelles collaborations académiques internationales.\n\n"
                    "Les perspectives de cette HDR concernent notamment le développement de nouvelles "
                    "approches de modélisation mathématique appliquées à la santé publique, à "
                    "l'environnement, à l'intelligence artificielle et aux systèmes complexes, ainsi que "
                    "le renforcement du rayonnement scientifique de l'Université de Djibouti à l'échelle "
                    "internationale."
                ),
                "order": 1,
            },
        )
