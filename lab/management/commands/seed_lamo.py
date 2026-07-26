from datetime import date
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from lab.models import (
    Activity,
    ActivityImage,
    AssociateResearcher,
    Doctorant,
    Habilitation,
    LabProfile,
    MasterCourse,
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
        self.seed_master_courses()
        self.seed_formation_activities()
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
             "", "", "", "member_liban_ismail.png",
             "Le Dr Liban ISMAIL est Maître de conférences en mathématiques appliquées à l'Université de "
             "Djibouti et Directeur du Laboratoire d'Analyse, de Modélisation et d'Optimisation (LAMO). Ses "
             "activités de recherche portent principalement sur la modélisation mathématique, les "
             "statistiques, la science des données, la recherche opérationnelle et l'optimisation, avec des "
             "applications dans les domaines de la santé publique, de l'environnement, de l'énergie, de la "
             "logistique et du développement durable. À travers ses travaux, il contribue au développement "
             "de solutions innovantes fondées sur les méthodes quantitatives pour répondre à des "
             "problématiques scientifiques et sociétales complexes.\n\n"
             "En parallèle de ses activités de recherche et d'enseignement, le Dr Liban ISMAIL est "
             "activement impliqué dans l'expertise scientifique internationale en qualité de reviewer pour "
             "des revues scientifiques internationales à comité de lecture. Au cours de la période "
             "2025–2026, il a représenté le LAMO dans le cadre de l'évaluation par les pairs de plusieurs "
             "manuscrits scientifiques publiés chez Springer Nature. Ses expertises couvrent notamment la "
             "modélisation mathématique, l'analyse de sensibilité globale, le contrôle optimal, la "
             "modélisation environnementale, la transition énergétique ainsi que les applications de "
             "l'intelligence artificielle aux systèmes complexes."),
            ("Dr. Yahyeh SOULEIMAN", "Maître de conférences en Mathématiques appliquées",
             "Doyen de l'IUT-T", False, team_sto,
             "yahyeh_souleiman@univ.edu.dj", "souleimanyahyeh@gmail.com", "+253 77 86 80 46 | +253 21 32 36 03",
             "member_yahyeh_souleiman.jpg",
             "Dr Yahyeh SOULEIMAN est Maître de Conférences en Mathématiques Appliquées, Doyen de l'Institut "
             "Universitaire de Technologie Tertiaire (IUT-T) de l'Université de Djibouti et membre "
             "permanent du LAMO. Fort de plus de quatorze années d'expérience dans l'enseignement "
             "supérieur, la recherche et les responsabilités académiques, il développe des travaux "
             "scientifiques à l'interface des mathématiques appliquées, de la modélisation et de l'analyse "
             "quantitative. Ses domaines d'expertise couvrent notamment la modélisation mathématique, "
             "l'analyse statistique et la science des données, l'optimisation, ainsi que leurs applications "
             "à la santé publique, à l'environnement et au développement durable.\n\n"
             "Très engagé dans l'animation de la recherche scientifique, il exerce un rôle de leadership "
             "académique à travers la coordination de groupes de recherche, l'encadrement de mémoires et de "
             "thèses de doctorat, ainsi que le développement de collaborations scientifiques nationales et "
             "internationales. Il est également membre du comité éditorial de la revue Applied Mathematics "
             "and Statistics (PJAMS) et intervient régulièrement comme évaluateur scientifique (reviewer) "
             "pour plusieurs revues internationales à comité de lecture.\n\n"
             "Auteur de nombreuses publications scientifiques dans des revues internationales indexées et "
             "conférencier invité lors de plusieurs manifestations scientifiques internationales, il "
             "participe activement au rayonnement scientifique de l'Université de Djibouti et du LAMO, "
             "tout en favorisant le transfert des connaissances vers les secteurs socio-économiques et les "
             "politiques publiques."),
            ("Dr. Souleiman OMAR", "Maître de conférences en Mathématiques fondamentales", "", False, team_dyn,
             "", "", "", "member_souleiman_omar.png",
             "Dr Souleiman Omar Hoch est Maître de conférences en mathématiques à l'Université de Djibouti "
             "et une figure importante de la recherche scientifique et de l'enseignement supérieur à "
             "Djibouti. Il est reconnu pour ses travaux en mathématiques pures, notamment en théorie des "
             "groupes quantiques, algèbres d'opérateurs et géométrie non commutative, avec plusieurs "
             "publications dans des revues internationales.\n\n"
             "En parallèle de ses activités académiques, il occupe des fonctions de direction et de "
             "coordination au sein de l'Université de Djibouti. Il est notamment Directeur du Centre "
             "d'Excellence Africain en Logistique et Transport (CEALT/CELT), un centre financé dans le "
             "cadre du programme ACE-Impact de la Banque mondiale. À ce titre, il pilote les activités de "
             "recherche, de formation, de coopération internationale et de développement institutionnel du "
             "centre.\n\n"
             "Ses responsabilités comprennent également la coordination de projets internationaux visant à "
             "renforcer les capacités de recherche de l'Université de Djibouti dans les domaines de la "
             "logistique, des transports, de l'ingénierie et de l'innovation. Plus récemment, il a "
             "participé au développement de nouvelles infrastructures de recherche, notamment dans le "
             "domaine des énergies renouvelables, afin de soutenir la transition énergétique et le "
             "développement durable à Djibouti."),
            ("Dr. Doualeh ABDILLAHI", "Maître de conférences en Statistiques appliquées", "", False, team_sto,
             "", "", "", "member_doualeh_abdillahi.png",
             "Dr Doualeh Abdillahi Ali est Maître de conférences en mathématiques appliquées et Directeur "
             "des études à la Faculté de Droit, Économie et Gestion de l'Université de Djibouti. Il est "
             "titulaire d'un doctorat en mathématiques appliquées, spécialité statistique, obtenu en 2023 à "
             "l'Université Clermont Auvergne, après y avoir également réalisé un Master en mathématiques "
             "appliquées.\n\n"
             "Ses activités d'enseignement et de recherche portent principalement sur les statistiques, les "
             "mathématiques appliquées, l'analyse des données et les méthodes quantitatives. Au sein de "
             "l'Université de Djibouti, il participe aux activités de formation, d'encadrement des "
             "étudiants et au développement de la recherche scientifique dans ces domaines.\n\n"
             "Sur le plan institutionnel, il est également membre du LAMO, où il contribue aux activités "
             "scientifiques du laboratoire, notamment à l'organisation de conférences internationales, de "
             "séminaires de recherche et de projets collaboratifs. Il a ainsi fait partie de la délégation "
             "de l'Université de Djibouti ayant représenté le LAMO lors de la conférence internationale "
             "DATA-SD 2025 organisée par l'Université d'Amoud (Somalie)."),
        ]
        for order, (full_name, title, role_tag, is_director, team, email, email_secondary, phone, photo, bio) in enumerate(members, start=1):
            member, _ = PermanentMember.objects.update_or_create(
                full_name=full_name,
                defaults={
                    "title": title, "role_tag": role_tag, "is_director": is_director, "team": team,
                    "email": email, "email_secondary": email_secondary, "phone": phone,
                    "bio": bio, "order": order,
                },
            )
            attach_image(member, "photo", photo)

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
            ("M. Hacène DJELLOUT", "Professeur", "Université Clermont Auvergne (UCA)", "France", "associate_hacene_djellout.jpeg",
             "Hacène Djellout est Professeur des universités en mathématiques appliquées à l'Université "
             "Clermont Auvergne (France), où il exerce au sein du Laboratoire de Mathématiques Blaise "
             "Pascal (LMBP). Il est spécialiste des probabilités, des statistiques, des processus "
             "stochastiques, de la modélisation mathématique et de l'analyse de sensibilité. Il est "
             "également responsable pédagogique du Master Mathématiques de l'Université Clermont "
             "Auvergne.\n\n"
             "Ses travaux de recherche portent principalement sur les grandes déviations, les déviations "
             "modérées, les équations différentielles stochastiques, les chaînes de Markov, les méthodes "
             "spectrales, le chaos polynomial (Polynomial Chaos Expansion), ainsi que la quantification "
             "des incertitudes et l'analyse de sensibilité globale. Il est l'auteur de nombreuses "
             "publications dans des revues internationales de premier plan telles que The Annals of "
             "Applied Probability, Annales de l'Institut Henri Poincaré, Probabilistic Engineering "
             "Mechanics, Mathematical Methods in the Applied Sciences et Journal of Theoretical "
             "Probability.\n\n"
             "Il a développé une collaboration scientifique avec le LAMO de l'Université de Djibouti, "
             "participant à plusieurs travaux de recherche en modélisation mathématique, analyse de "
             "sensibilité globale et modélisation épidémiologique, notamment sur l'analyse de sensibilité "
             "du modèle SIHR appliqué à la COVID-19 et sur la modélisation des systèmes climatiques "
             "utilisant les développements en chaos polynomial."),
            ("Mme. Raluca EFTIMIE", "Professeure", "Université Marie et Louis Pasteur", "France", "associate_raluca_eftimie.png",
             "Raluca Eftimie est Professeure des universités en mathématiques appliquées à l'Université "
             "Marie et Louis Pasteur (anciennement Université de Franche-Comté), où elle est membre du "
             "Laboratoire de Mathématiques de Besançon (LMB). Elle est une spécialiste reconnue en "
             "biologie mathématique, modélisation mathématique, équations différentielles ordinaires et "
             "aux dérivées partielles (EDO/EDP), ainsi qu'en modélisation des systèmes biologiques "
             "complexes.\n\n"
             "Ses recherches portent principalement sur la modélisation mathématique du cancer (oncologie "
             "mathématique), de l'immunologie, de l'épidémiologie, de l'écologie mathématique, ainsi que "
             "sur l'étude des phénomènes de formation de motifs (pattern formation) et des systèmes non "
             "linéaires et non locaux, avec des applications à la médecine, à l'immunothérapie et aux "
             "maladies infectieuses.\n\n"
             "Auteure de plus de 130 publications scientifiques dans des revues internationales de haut "
             "niveau, elle siège aux comités éditoriaux de plusieurs revues prestigieuses, notamment "
             "Journal of Mathematical Biology, Journal of Theoretical Biology, Mathematical Biosciences "
             "and Engineering et Computational and Systems Oncology, et est Chief Editor de la section "
             "Mathematical Biology de la revue Frontiers in Applied Mathematics and Statistics. Elle "
             "développe des collaborations scientifiques avec le LAMO de l'Université de Djibouti dans "
             "les domaines de la modélisation mathématique des maladies infectieuses, de l'immunologie et "
             "de la biologie mathématique."),
            ("Mme. Nathalie VERDIÈRE", "Maîtresse de conférences HDR", "Université Le Havre Normandie", "France", "",
             "Nathalie Verdière est Maîtresse de conférences HDR (Habilitée à Diriger des Recherches) en "
             "Mathématiques Appliquées à l'Université Le Havre Normandie. Elle est membre permanent du "
             "Laboratoire de Mathématiques Appliquées du Havre (LMAH) et enseigne principalement au "
             "département Génie Électrique et Informatique Industrielle (GEII) de l'IUT du Havre. Elle "
             "est également membre associée du LAMO de l'Université de Djibouti, où elle participe au "
             "développement de collaborations scientifiques internationales.\n\n"
             "Ses recherches portent sur la modélisation mathématique des systèmes dynamiques, "
             "l'identifiabilité, l'observabilité, la détection et le diagnostic de défauts, la "
             "contrôlabilité des réseaux de systèmes complexes ainsi que l'estimation de paramètres, avec "
             "des applications dans des domaines variés tels que la physique, l'automatique, la biologie, "
             "les neurosciences, la dynamique des populations et les sciences de l'environnement.\n\n"
             "Auteure de plus de 60 publications scientifiques dans des revues internationales à comité "
             "de lecture, elle encadre des doctorants et participe à plusieurs projets de recherche "
             "nationaux et internationaux. Dans le cadre de sa collaboration avec le LAMO, elle apporte "
             "son expertise en modélisation mathématique, en théorie du contrôle et en analyse des "
             "systèmes dynamiques, notamment à travers l'encadrement de la thèse du doctorant Gouled "
             "Souleiman."),
            ("M. Abdisalam HASSAN", "Professeur associé", "Université AMOUD", "Somalie", "associate_abdisalam_hassan.png",
             "Le Dr Abdisalam Hassan Muse est Professeur associé en statistique et mathématiques "
             "appliquées à l'Université d'Amoud (Amoud University), en Somalie (Borama). Il est "
             "actuellement Directeur du Research and Innovation Centre et Doyen de la School of "
             "Postgraduate Studies and Research, où il dirige également les programmes de master en "
             "statistique appliquée, mathématiques appliquées et statistique médicale. Fort de plus de "
             "dix années d'expérience dans l'enseignement supérieur et la recherche, il joue un rôle "
             "majeur dans le développement de la recherche scientifique en Afrique de l'Est.\n\n"
             "Ses domaines d'expertise couvrent les statistiques appliquées, les mathématiques, la "
             "science des données, les méthodes bayésiennes, l'analyse de survie, la cartographie des "
             "maladies (disease mapping), la modélisation spatiale et l'analyse de données. Il est "
             "l'auteur de plus de 70 publications scientifiques dans des revues internationales et "
             "supervise de nombreux étudiants en master et en doctorat.\n\n"
             "Selon l'AD Scientific Index 2026, il figure parmi les chercheurs les mieux classés de "
             "Somalie en sciences mathématiques, avec un h-index de 19 et plus de 1 000 citations. Il "
             "entretient des relations scientifiques avec le LAMO de l'Université de Djibouti, "
             "participant à des conférences internationales, à des projets de recherche collaboratifs et "
             "au renforcement des partenariats académiques entre les deux institutions."),
            ("M. Lemecha LEGESSE", "Professeur", "Adama Science and Technology University", "Éthiopie", "associate_legesse_lemecha.jpeg",
             "Legesse Lemecha Obsu est Professeur en mathématiques appliquées à l'Adama Science and "
             "Technology University (ASTU), en Éthiopie, et Directeur de l'École Doctorale. Il est membre "
             "du Département de Mathématiques Appliquées, où il exerce des activités d'enseignement, de "
             "recherche et d'encadrement de doctorants.\n\n"
             "Ses travaux de recherche portent principalement sur la modélisation mathématique, les "
             "équations différentielles, le contrôle optimal, la recherche opérationnelle, les méthodes "
             "numériques et l'optimisation, appliqués à des problématiques d'intérêt sociétal : "
             "épidémiologie, agriculture, gestion des ressources naturelles, dynamique des populations et "
             "optimisation des systèmes de transport.\n\n"
             "Cette coopération scientifique avec le LAMO se traduit par des échanges réguliers, la "
             "co-signature de plusieurs articles scientifiques et le développement de travaux de "
             "recherche conjoints. Il a également participé à l'atelier scientifique organisé par le "
             "laboratoire en 2024 et à une rencontre scientifique à Djibouti en novembre 2024, "
             "contribuant activement au renforcement des liens académiques entre les deux institutions."),
        ]
        for order, (full_name, grade, institution, country, photo, bio) in enumerate(rows, start=1):
            associate, _ = AssociateResearcher.objects.update_or_create(
                full_name=full_name,
                defaults={
                    "grade": grade,
                    "institution": institution,
                    "country": country,
                    "bio": bio,
                    "order": order,
                },
            )
            if photo:
                attach_image(associate, "photo", photo)

    def _seed_activity_rows(self, rows):
        for row in rows:
            defaults = dict(row["defaults"])
            image = defaults.pop("image", "")
            gallery = defaults.pop("gallery", [])
            activity, _ = Activity.objects.update_or_create(
                category=row["category"], title=row["title"], defaults=defaults,
            )
            if image:
                attach_image(activity, "image", image)
            if gallery:
                activity.gallery.all().delete()
                for order, filename in enumerate(gallery, start=1):
                    path = SEED_MEDIA / filename
                    if not path.exists():
                        continue
                    with open(path, "rb") as fh:
                        ActivityImage.objects.create(
                            activity=activity, order=order,
                            image=File(fh, name=filename),
                        )

    def seed_activities(self):
        # Anciens intitulés génériques remplacés par les activités détaillées ci-dessous.
        Activity.objects.filter(
            title__in=["Conférence LAMO", "Olympiades de mathématiques"]
        ).delete()

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
                "sort_date": date(2027, 1, 19),
                "order": 2,
            },
        )
        attach_image(conference, "image", "activity_m2isda_2027_poster.jpg")

        conference_2024, _ = Activity.objects.update_or_create(
            category=Activity.Category.CONFERENCE,
            title="M2ISDA — Modélisation mathématique et innovation en sciences des données avancées",
            defaults={
                "edition_label": "1ère édition",
                "year": "30–31 octobre 2024",
                "location": "Salle de conférences de la faculté d'ingénieurs de l'Université de Djibouti",
                "description": (
                    "Cet atelier scientifique a été organisé par le LAMO dans le but de renforcer les "
                    "échanges autour des approches modernes de modélisation mathématique et des "
                    "innovations en sciences des données avancées. Il a réuni des chercheurs, des "
                    "enseignants-chercheurs, des praticiens ainsi que des représentants d'institutions "
                    "nationales et internationales, notamment le Pr. Hacène Djellout (Université Clermont "
                    "Auvergne), le Dr. Abdisalam (Université d'Amoud), le Dr. Usame (Université de "
                    "Jigjiga) et le Pr. Legesse (Adama Science and Technology University).\n\n"
                    "L'atelier a mis en lumière les dernières avancées en science des données et en "
                    "intelligence artificielle, en soulignant leur rôle central dans l'aide à la décision "
                    "et l'analyse des systèmes complexes. Les discussions ont également impliqué "
                    "l'Institut National de la Statistique de Djibouti (INSTAD) et l'Hôpital Militaire de "
                    "Djibouti, ouvrant des perspectives de collaboration scientifique, en particulier dans "
                    "la validation des modèles à partir de données réelles.\n\n"
                    "L'événement a bénéficié de la présence et du soutien des autorités nationales, "
                    "notamment du Ministère de l'Enseignement supérieur et de la Recherche ainsi que de "
                    "l'Université de Djibouti, constituant un cadre privilégié de dialogue scientifique et "
                    "de renforcement des partenariats."
                ),
                "sort_date": date(2024, 10, 30),
                "order": 1,
            },
        )
        attach_image(conference_2024, "image", "activity_m2isda2024_comite.jpeg")

        seminaires = [
            {
                "category": Activity.Category.SEMINAIRE,
                "title": "Modélisation mathématique des écosystèmes forestiers dans un contexte de changement climatique",
                "defaults": {
                    "year": "24 avril 2025", "location": "Laboratoire d'Analyse, de Modélisation et d'Optimisation (LAMO)",
                    "people": "Gouled SOULEIMAN (doctorant LAMO)", "sort_date": date(2025, 4, 24), "order": 1,
                    "description": (
                        "Séminaire doctoral consacré à la présentation des travaux de recherche du "
                        "doctorant Gouled SOULEIMAN, portant sur la modélisation mathématique des "
                        "écosystèmes forestiers dans un contexte de changement climatique et "
                        "environnemental. L'étude met en évidence les impacts combinés des facteurs "
                        "climatiques (incendies, inondations, sécheresses, vagues de chaleur, espèces "
                        "invasives) et anthropiques (déforestation, surpâturage, pollution) sur la "
                        "structure et le fonctionnement des forêts.\n\n"
                        "L'objectif principal de cette recherche est de développer des outils "
                        "mathématiques permettant de mieux comprendre la dynamique de ces écosystèmes "
                        "sous contraintes multiples, afin de proposer des approches d'analyse et de "
                        "gestion adaptées aux défis environnementaux actuels."
                    ),
                    "image": "activity_seminaire_gouled_avril2025.jpeg",
                },
            },
            {
                "category": Activity.Category.SEMINAIRE,
                "title": "Prédire la blessure, optimiser l'entraînement : l'intelligence artificielle au service de la performance durable en football",
                "defaults": {
                    "year": "15 janvier 2026, à partir de 9h", "location": "Faculté d'Ingénieurs, Salle des conférences",
                    "people": "Pr. Pierre DRUILHET (Université Clermont Auvergne)", "sort_date": date(2026, 1, 15), "order": 2,
                    "description": (
                        "Séminaire-conférence consacré à l'apport de l'intelligence artificielle dans "
                        "l'analyse de la performance sportive, en particulier dans le domaine du football, "
                        "animé par le Professeur Pierre DRUILHET, spécialiste en mathématiques appliquées "
                        "et en science des données à l'Université Clermont Auvergne.\n\n"
                        "La conférence a permis de présenter des approches modernes basées sur "
                        "l'apprentissage automatique et l'analyse de données sportives, avec pour "
                        "objectif de développer des modèles prédictifs capables d'anticiper les risques "
                        "de blessures chez les athlètes, tout en optimisant les programmes d'entraînement."
                    ),
                    "image": "activity_seminaire_druilhet.jpeg",
                },
            },
            {
                "category": Activity.Category.SEMINAIRE,
                "title": "L'intelligence artificielle est-elle multiforme ?",
                "defaults": {
                    "year": "12 février 2026", "location": "Faculté d'Ingénieurs, Université de Djibouti",
                    "people": "Pr. Engelbert Mephu Nguifo", "sort_date": date(2026, 2, 12), "order": 3,
                    "description": (
                        "Séminaire scientifique ayant réuni des enseignants-chercheurs, des chercheurs et "
                        "des étudiants de l'Université de Djibouti, notamment ceux du Master Intelligence "
                        "Artificielle et Modélisation des Données (IAMD). Animé par le Professeur "
                        "Engelbert Mephu Nguifo, spécialiste en intelligence artificielle, le séminaire a "
                        "présenté une analyse approfondie des différentes formes que revêt aujourd'hui "
                        "l'intelligence artificielle : apprentissage automatique, apprentissage profond, "
                        "systèmes de recommandation, systèmes intelligents et technologies génératives.\n\n"
                        "La séance d'ouverture a été assurée par le Directeur du LAMO, Dr Liban Ismail "
                        "Abdillahi, qui a rappelé le rôle stratégique de la recherche en intelligence "
                        "artificielle dans le développement scientifique, technologique et "
                        "socio-économique de Djibouti."
                    ),
                    "image": "activity_seminaire_mephu.jpeg",
                },
            },
            {
                "category": Activity.Category.SEMINAIRE,
                "title": "Mathématiques appliquées et intelligence artificielle",
                "defaults": {
                    "year": "Jeudi 2 avril 2026, à partir de 9h30", "location": "Faculté d'Ingénieurs, Salle des conférences",
                    "people": "M. Gouled Souleiman (LAMO) et Pr. Andrzej Stos (Université Clermont Auvergne)", "sort_date": date(2026, 4, 2), "order": 4,
                    "description": (
                        "Séminaire scientifique consacré aux thématiques actuelles en mathématiques "
                        "appliquées et en intelligence artificielle, réunissant M. Gouled Souleiman, "
                        "doctorant en mathématiques appliquées et membre du LAMO, ainsi que le Professeur "
                        "Andrzej Stos, chercheur à l'Université Clermont Auvergne, spécialiste en analyse "
                        "mathématique et en probabilités, avec des applications en machine learning et "
                        "deep learning.\n\n"
                        "La modération a été assurée par le directeur du LAMO, Dr Liban Ismail Abdillahi. "
                        "Ce séminaire a constitué un espace d'échange entre chercheurs, étudiants et "
                        "professionnels autour des applications de la science des données dans des "
                        "secteurs stratégiques tels que le numérique, les télécommunications et la "
                        "finance."
                    ),
                    "image": "activity_seminaire_avril2026_affiche.jpeg",
                    "gallery": ["activity_seminaire_stos.jpeg", "activity_seminaire_avril2026_gouled.jpeg"],
                },
            },
            {
                "category": Activity.Category.SEMINAIRE,
                "title": "Journée de sensibilisation aux mathématiques et aux sciences – École d'Excellence",
                "defaults": {
                    "year": "29 janvier 2026 (jeudi)", "location": "École d'Excellence, Djibouti",
                    "people": "Pr. Stéphanie LÉGER (Polytech Clermont – Université Clermont Auvergne)", "sort_date": date(2026, 1, 29), "order": 5,
                    "description": (
                        "Matinée de sensibilisation aux mathématiques et aux sciences organisée au sein "
                        "de l'École d'Excellence, dans une dynamique visant à renforcer l'intérêt des "
                        "élèves pour les disciplines scientifiques et à encourager l'émergence de "
                        "vocations scientifiques dès le cycle secondaire.\n\n"
                        "La séance a été animée par la Professeure Stéphanie LÉGER, Maître de Conférences "
                        "en Ingénierie Mathématique et Data Science à Polytech Clermont, en mission "
                        "académique à l'Université de Djibouti dans le cadre du Master IAMD."
                    ),
                    "image": "activity_ecoleexcellence_affiche.jpeg",
                },
            },
        ]
        self._seed_activity_rows(seminaires)

        olympiades = [
            {
                "category": Activity.Category.OLYMPIADES,
                "title": "Journée Internationale des Mathématiques",
                "defaults": {
                    "edition_label": "Édition 2025", "year": "12 & 13 février 2025", "location": "Université de Djibouti",
                    "sort_date": date(2025, 2, 12), "order": 1,
                    "description": (
                        "Journée des Mathématiques organisée sur deux jours, réunissant des étudiants "
                        "universitaires ainsi que des élèves des lycées de la capitale, avec pour objectif "
                        "de stimuler l'excellence scientifique et de renforcer l'intérêt des jeunes pour "
                        "les mathématiques. Le premier jour a été consacré à un concours de mathématiques ; "
                        "le second a été marqué par des conférences scientifiques et pédagogiques animées "
                        "par des enseignants-chercheurs et des professeurs de lycée."
                    ),
                    "image": "activity_jim2025_presentation.jpeg",
                },
            },
            {
                "category": Activity.Category.OLYMPIADES,
                "title": "Cérémonie de remise des prix — Journée Internationale des Mathématiques 2025",
                "defaults": {
                    "edition_label": "Édition 2025", "year": "13 février 2025", "location": "Université de Djibouti",
                    "sort_date": date(2025, 2, 13), "order": 2,
                    "description": (
                        "Cérémonie officielle de remise des prix, en présence du Ministre de l'Éducation "
                        "nationale, M. Moustapha Mohamed, et du Président de l'Université de Djibouti, "
                        "Dr Djama Mohamed, célébrant les lauréats du concours de mathématiques et saluant "
                        "leur engagement et leurs performances remarquables."
                    ),
                    "image": "activity_jim2025_remise_prix.jpeg",
                },
            },
            {
                "category": Activity.Category.OLYMPIADES,
                "title": "Lancement de la phase de sensibilisation — Olympiades Nationales de Mathématiques",
                "defaults": {
                    "edition_label": "Édition 2026", "year": "4 au 8 janvier 2026",
                    "location": "Université de Djibouti et établissements partenaires dans tout le pays",
                    "people": "LAMO & ADAM-Maths", "sort_date": date(2026, 1, 4), "order": 3,
                    "description": (
                        "Lancement officiel de la phase de sensibilisation des Olympiades Nationales de "
                        "Mathématiques, en collaboration avec l'association ADAM-Maths. Cette phase s'est "
                        "déroulée sur l'ensemble du territoire national : les trois communes de la "
                        "capitale (Balbala, Boulaos et Ras-Dika), ainsi que les cinq régions de l'intérieur "
                        "du pays (Ali Sabieh, Arta, Dikhil, Obock et Tadjourah)."
                    ),
                    "image": "activity_onm2026_sensibilisation.jpeg",
                },
            },
            {
                "category": Activity.Category.OLYMPIADES,
                "title": "Lancement des épreuves de la phase régionale — ONM 2026",
                "defaults": {
                    "edition_label": "Édition 2026", "year": "12 janvier 2026",
                    "location": "Université de Djibouti et sites régionaux décentralisés",
                    "people": "LAMO & ADAM-Maths", "sort_date": date(2026, 1, 12), "order": 4,
                    "description": (
                        "Lancement officiel de la phase régionale des épreuves, étape clé du processus de "
                        "sélection des meilleurs candidats à l'échelle nationale, déployée simultanément "
                        "dans les trois communes de la capitale et les cinq régions de l'intérieur du pays."
                    ),
                    "image": "activity_onm2026_regionale_epreuve.jpeg",
                    "gallery": ["activity_onm2026_regionale_epreuve_2.jpeg"],
                },
            },
            {
                "category": Activity.Category.OLYMPIADES,
                "title": "Cérémonie de remise des prix — phase régionale ONM 2026",
                "defaults": {
                    "edition_label": "Édition 2026", "year": "15 janvier 2026",
                    "location": "Université de Djibouti (site central) et sites décentralisés",
                    "people": "LAMO & ADAM-Maths", "sort_date": date(2026, 1, 15), "order": 5,
                    "description": (
                        "Cérémonie de remise des prix de la phase régionale, en présence du Président de "
                        "l'Université de Djibouti, Dr Djama Mohamed, et du Conseiller du Ministre de "
                        "l'Enseignement supérieur et de la Recherche, Dr Fahmi. Les trois premiers "
                        "lauréats de chaque niveau ont été récompensés pour leurs performances "
                        "exceptionnelles."
                    ),
                    "image": "activity_onm2026_regionale_remise.jpeg",
                },
            },
            {
                "category": Activity.Category.OLYMPIADES,
                "title": "Répartition des candidats — phase régionale ONM 2026",
                "defaults": {
                    "edition_label": "Édition 2026", "sort_date": date(2026, 1, 15), "order": 6,
                    "description": (
                        "Participation globale de 6 100 candidats à la phase régionale : 5 500 candidats "
                        "de niveau scolaire (90 %) et 600 candidats de niveau universitaire (10 %), "
                        "traduisant une forte mobilisation des élèves du secondaire et une implication "
                        "significative de l'enseignement supérieur."
                    ),
                    "image": "activity_onm2026_stats_regionale.jpeg",
                },
            },
            {
                "category": Activity.Category.OLYMPIADES,
                "title": "Lancement des épreuves de la phase nationale — ONM 2026",
                "defaults": {
                    "edition_label": "Édition 2026", "year": "1er février 2026 (dimanche)", "location": "Université de Djibouti",
                    "people": "LAMO & ADAM-Maths", "sort_date": date(2026, 2, 1), "order": 7,
                    "description": (
                        "Lancement de la phase nationale, aboutissement du processus de sélection "
                        "réunissant les meilleurs candidats issus des phases régionales, en présence du "
                        "Secrétaire Général du MENFOP, M. Mohamed Abdallah, et du Président de "
                        "l'Université de Djibouti, Dr Djama Mohamed."
                    ),
                    "image": "activity_onm2026_nationale_epreuve.jpeg",
                    "gallery": ["activity_onm2026_nationale_epreuve_2.jpeg"],
                },
            },
            {
                "category": Activity.Category.OLYMPIADES,
                "title": "Cérémonie de remise des prix — phase nationale ONM 2026",
                "defaults": {
                    "edition_label": "Édition 2026", "year": "23 mars 2026 (lundi)", "location": "Université de Djibouti (site central)",
                    "people": "LAMO & ADAM-Maths", "sort_date": date(2026, 3, 23), "order": 8,
                    "description": (
                        "Cérémonie officielle marquant l'aboutissement du processus national de "
                        "sélection, honorée par la présence du Ministre de l'Enseignement Supérieur et de "
                        "la Recherche, Dr Nabil Mohamed, du Ministre de l'Éducation Nationale, M. "
                        "Moustapha Mohamed, et du Ministre du Budget, M. Isman Robleh. Les trois premiers "
                        "lauréats de chaque niveau ont été récompensés par des prix et certificats "
                        "d'excellence."
                    ),
                    "image": "activity_onm2026_nationale_remise.jpeg",
                    "gallery": [
                        "activity_onm2026_nationale_remise_2.jpeg",
                        "activity_onm2026_nationale_laureats.jpeg",
                        "activity_onm2026_nationale_laureats_2.jpeg",
                    ],
                },
            },
            {
                "category": Activity.Category.OLYMPIADES,
                "title": "Répartition des candidats par genre — phase nationale ONM 2026",
                "defaults": {
                    "edition_label": "Édition 2026", "sort_date": date(2026, 3, 23), "order": 9,
                    "description": (
                        "Sur 581 candidats à la phase nationale : 217 filles (37 %) et 364 garçons (63 %), "
                        "une répartition qui traduit une progression encourageante de l'implication "
                        "féminine dans les activités mathématiques compétitives."
                    ),
                    "image": "activity_onm2026_stats_genre.jpeg",
                },
            },
            {
                "category": Activity.Category.OLYMPIADES,
                "title": "Répartition des lauréats par région — ONM 2026",
                "defaults": {
                    "edition_label": "Édition 2026", "sort_date": date(2026, 3, 23), "order": 10,
                    "description": (
                        "Balbala 27 %, Boulaos 20 %, Université de Djibouti 20 %, CPGE 13 %, Ali-Sabieh "
                        "7 %, Ras-Dika 6 %, autres secteurs 7 % — une représentation relativement "
                        "équilibrée des différentes régions et établissements du pays."
                    ),
                    "image": "activity_onm2026_stats_region.jpeg",
                },
            },
            {
                "category": Activity.Category.OLYMPIADES,
                "title": "Répartition des lauréats par filière — ONM 2026",
                "defaults": {
                    "edition_label": "Édition 2026", "sort_date": date(2026, 3, 23), "order": 11,
                    "description": (
                        "5ème 20 %, 9ème 20 %, Licence (FS+IUT-I) 20 %, CPGE (L1+L2) 13 %, Seconde 13 %, "
                        "1ère S 7 %, Terminale S 7 % — une diversité de profils illustrant le caractère "
                        "inclusif des Olympiades Nationales de Mathématiques."
                    ),
                    "image": "activity_onm2026_stats_filiere.jpeg",
                },
            },
        ]
        self._seed_activity_rows(olympiades)

        participations = [
            {
                "category": Activity.Category.PARTICIPATION,
                "title": "Mathematical Modeling of Epidemiological Dynamics",
                "defaults": {
                    "year": "17 au 21 juin 2024", "location": "Université Le Havre Normandie, France",
                    "people": "Dr Yahyeh SOULEIMAN", "sort_date": date(2024, 6, 17), "order": 1,
                    "description": (
                        "Le Dr Yahyeh SOULEIMAN a présenté ses travaux de recherche en modélisation "
                        "mathématique des dynamiques épidémiologiques lors de cette conférence "
                        "internationale, en tant que représentant du LAMO. Les échanges scientifiques ont "
                        "porté sur le développement de modèles épidémiologiques, l'analyse des dynamiques "
                        "de transmission et l'élaboration de stratégies de contrôle."
                    ),
                    "image": "activity_participation_lehavre2024.jpeg",
                },
            },
            {
                "category": Activity.Category.PARTICIPATION,
                "title": "1ère édition des Journées Scientifiques du CHU de Djibouti",
                "defaults": {
                    "year": "22 et 23 décembre 2024", "location": "Palais du Peuple, Djibouti",
                    "people": "Dr Liban ISMAIL et Dr Yahyeh SOULEIMAN", "sort_date": date(2024, 12, 22), "order": 2,
                    "description": (
                        "Les membres du LAMO ont participé à la première édition des Journées "
                        "Scientifiques du Centre Hospitalier Universitaire de Djibouti, qui a rassemblé "
                        "plus de 300 professionnels de santé autour du thème « La recherche médicale au "
                        "service de la qualité des soins ». À travers leur participation, ils ont mis en "
                        "évidence l'apport des mathématiques appliquées et de la modélisation dans "
                        "l'amélioration des systèmes de santé."
                    ),
                    "image": "activity_participation_chu2024.jpeg",
                },
            },
            {
                "category": Activity.Category.PARTICIPATION,
                "title": "Colloque annuel des doctorantes et doctorants — La Rochelle Université",
                "defaults": {
                    "year": "19 et 20 mai 2025", "location": "La Rochelle Université, France",
                    "people": "Ali MOHAMED (doctorant LAMO)", "sort_date": date(2025, 5, 19), "order": 3,
                    "description": (
                        "Le doctorant Ali MOHAMED a présenté ses travaux de thèse portant sur l'analyse "
                        "mathématique et les méthodes numériques, à travers une contribution intitulée "
                        "« Observability inequality for the wavelet-based Galerkin method », publiée dans "
                        "les actes de la conférence IFAC (IFAC PapersOnLine, volume 59, numéro 13, pages "
                        "46–51, 2025)."
                    ),
                },
            },
            {
                "category": Activity.Category.PARTICIPATION,
                "title": "A Mathematical Model to Investigate the Impact of Climate Change on Forest Ecosystems and a Strategy for Its Regeneration",
                "defaults": {
                    "year": "6 juin 2025", "location": "Carcans Maubuisson, France",
                    "people": "Gouled SOULEIMAN (doctorant LAMO)", "sort_date": date(2025, 6, 6), "order": 4,
                    "description": (
                        "Exposé scientifique présenté par le doctorant Gouled SOULEIMAN dans le cadre de "
                        "la 12ième Biennale Française des Mathématiques Appliquées et Industrielles, "
                        "portant sur la modélisation mathématique des effets du changement climatique sur "
                        "les écosystèmes forestiers et des stratégies de régénération optimales."
                    ),
                    "image": "activity_participation_biennale2025_affiche.jpeg",
                },
            },
            {
                "category": Activity.Category.PARTICIPATION,
                "title": "Conférence internationale DATA-SD 2025",
                "defaults": {
                    "year": "18 au 20 août 2025", "location": "Amoud University, Borama, Somaliland",
                    "people": "Dr Yahyeh SOULEIMAN, Dr Souleiman Omar Hoch, Dr Doualeh, Dr Liban Ismail Abdillahi",
                    "sort_date": date(2025, 8, 18), "order": 5,
                    "description": (
                        "Le LAMO a participé à la conférence internationale DATA-SD 2025 (International "
                        "Conference on Data Science for Sustainable Development), réunissant des "
                        "chercheurs, enseignants-chercheurs et experts autour des avancées récentes en "
                        "science des données, modélisation mathématique, optimisation et développement "
                        "durable. Quatre membres du laboratoire ont représenté l'Université de Djibouti, "
                        "renforçant la visibilité du LAMO et développant de nouvelles collaborations "
                        "scientifiques."
                    ),
                    "image": "activity_participation_datasd2025.jpeg",
                },
            },
            {
                "category": Activity.Category.PARTICIPATION,
                "title": "Modeling and investigating malaria Plasmodium falciparum and Plasmodium vivax infections: Application to Djibouti data",
                "defaults": {
                    "year": "18 au 20 août 2025", "location": "Amoud University, Borama, Somaliland (DATA-SD 2025)",
                    "people": "Dr Yahyeh SOULEIMAN, en collaboration avec Liban Ismail et Raluca Eftimie", "sort_date": date(2025, 8, 18), "order": 6,
                    "description": (
                        "Communication scientifique portant sur la modélisation mathématique de la "
                        "transmission du paludisme à Djibouti, à partir de données épidémiologiques "
                        "réelles collectées dans le contexte djiboutien, visant à mieux comprendre les "
                        "mécanismes de propagation et à évaluer l'impact de différentes stratégies de "
                        "prévention et de contrôle."
                    ),
                    "image": "activity_participation_datasd2025_presentation.jpeg",
                },
            },
            {
                "category": Activity.Category.PARTICIPATION,
                "title": "Mathematical modeling of active regeneration via a facilitator species strategy: stability and bifurcations",
                "defaults": {
                    "year": "1er–2 juin 2026", "location": "Lyon, France",
                    "people": "Gouled SOULEIMAN (doctorant LAMO)", "sort_date": date(2026, 6, 1), "order": 7,
                    "description": (
                        "Exposé scientifique présenté par le doctorant Gouled SOULEIMAN dans le cadre de "
                        "The French Conference on Complex Systems, portant sur la modélisation "
                        "mathématique des dynamiques de régénération active dans les systèmes écologiques, "
                        "avec une analyse des conditions de stabilité et des phénomènes de bifurcation."
                    ),
                    "image": "activity_participation_lyon2026_affiche.jpeg",
                },
            },
        ]
        self._seed_activity_rows(participations)

        editorial = [
            {
                "category": Activity.Category.EDITORIAL,
                "title": "Membre du comité éditorial — Precision Journal of Applied Mathematics and Statistics (PJAMS)",
                "defaults": {
                    "year": "2026", "people": "Dr Yahyeh SOULEIMAN", "sort_date": date(2026, 1, 1), "order": 1,
                    "description": (
                        "Le Dr Yahyeh SOULEIMAN a été nommé membre du comité éditorial (Editorial Board "
                        "Member) de la revue scientifique internationale à comité de lecture Precision "
                        "Journal of Applied Mathematics and Statistics (PJAMS), dédiée à la publication de "
                        "travaux originaux en mathématiques appliquées, statistiques et disciplines "
                        "interdisciplinaires associées. Cette nomination témoigne de la reconnaissance "
                        "internationale de son expertise scientifique et contribue au renforcement du "
                        "rayonnement du LAMO et de l'Université de Djibouti."
                    ),
                    "image": "activity_editorial_pjams_logo.jpeg",
                },
            },
            {
                "category": Activity.Category.EDITORIAL,
                "title": "Activités d'expertise scientifique : évaluation d'articles (Dr Yahyeh SOULEIMAN)",
                "defaults": {
                    "year": "2021–2026", "people": "Dr Yahyeh SOULEIMAN — Reviewer", "sort_date": date(2026, 6, 1), "order": 2,
                    "description": (
                        "Le Dr Yahyeh SOULEIMAN s'implique activement comme évaluateur scientifique "
                        "(reviewer) pour plusieurs revues internationales à comité de lecture, couvrant "
                        "notamment la modélisation mathématique, le calcul fractionnaire, les équations "
                        "différentielles, le contrôle optimal, la mécanique des milieux continus et la "
                        "modélisation des maladies infectieuses. Manuscrits évalués :\n\n"
                        "2021 – Palestine Journal of Mathematics : A Quasistatic Frictional Contact "
                        "Problem for Thermo-Electro-Viscoelastic Materials.\n"
                        "2022 – Asian Research Journal of Mathematics : On the Solution of a Non-linear "
                        "Fractional-Order Mathematical Model of Glucose–Insulin System Incorporating "
                        "β-Cells Compartment.\n"
                        "2023 – Asian Research Journal of Mathematics : Fixed Point Results for Rational "
                        "Type Contraction in Metric Spaces.\n"
                        "2024 – Precision Journal of Disease Biology (PJDB) : Identification of Bioactive "
                        "Postbiotics Against Neonatal Meningitis Caused by Group B Streptococcus via "
                        "Srr2-Targeted In-Silico Screening.\n"
                        "2025 – Evolution Equations and Control Theory : Exponential Decay for a "
                        "Thermo-Viscoelastic Dynamic Contact Problem with Friction and Infinite Memory.\n"
                        "2026 – Scientific African : Impact of Behavioural Protection on HIV–Mpox "
                        "Co-infection Dynamics : A Mathematical Modelling Approach."
                    ),
                },
            },
            {
                "category": Activity.Category.EDITORIAL,
                "title": "Activités d'expertise scientifique : évaluation d'articles (Dr Liban ISMAIL)",
                "defaults": {
                    "year": "2025–2026", "people": "Dr Liban ISMAIL — Reviewer", "sort_date": date(2026, 3, 1), "order": 3,
                    "description": (
                        "Le Dr Liban ISMAIL, Directeur du LAMO, participe aux activités d'expertise "
                        "scientifique internationale en qualité d'évaluateur pour des revues à comité de "
                        "lecture, couvrant la modélisation mathématique, l'analyse de sensibilité globale, "
                        "le contrôle optimal, la modélisation environnementale, la transition énergétique "
                        "et les applications de l'intelligence artificielle. Manuscrits évalués :\n\n"
                        "2025 – Carbon Balance and Management (Springer Nature) : Mathematical Modeling "
                        "of Carbon Dioxide Emissions with GDP Linkage : Sensitivity Analysis and Optimal "
                        "Control Strategy (recommandation de révision suivie d'une acceptation).\n"
                        "2026 – Earth Systems and Environment (Springer) : Machine learning-based "
                        "Performance Prediction of Horizontal Ground Source Heat Pump in Tropical "
                        "Country."
                    ),
                },
            },
        ]
        self._seed_activity_rows(editorial)

    def seed_master_courses(self):
        courses = [
            ("Master 1 IAMD", "Outils mathématiques pour les données", "Dr Liban ISMAIL ABDILLAHI",
             "Fournir aux étudiants les fondements mathématiques essentiels à la manipulation, l'analyse "
             "et la modélisation des données, avec un accent particulier sur les espaces vectoriels, "
             "l'algèbre linéaire et les méthodes d'optimisation."),
            ("Master 1 IAMD", "Méthodologie de la recherche", "Dr Souleiman OMAR HOCH",
             "Familiariser les étudiants avec les principes fondamentaux de la recherche scientifique, la "
             "construction d'un projet de recherche, la rédaction académique ainsi que les outils de "
             "veille scientifique et bibliographique."),
            ("Master 1 MPM", "Modélisation statistique et analyse de données", "Dr Liban ISMAIL ABDILLAHI",
             "Méthodes statistiques avancées, inférence statistique, régression et analyse exploratoire "
             "de données, avec des applications concrètes en sciences de l'ingénieur et en data science."),
            ("Master 1 MPM", "Recherche opérationnelle", "Dr Yahyeh Souleiman Isman",
             "Méthodes d'optimisation, programmation linéaire et entière, ainsi que techniques de prise "
             "de décision dans des systèmes complexes."),
        ]
        for order, (program, course_title, instructor, description) in enumerate(courses, start=1):
            MasterCourse.objects.update_or_create(
                program=program, course_title=course_title,
                defaults={"instructor": instructor, "description": description, "order": order},
            )

    def seed_formation_activities(self):
        # Anciens intitulés remplacés par des versions enrichies (voir jury de thèse.docx).
        Activity.objects.filter(
            title__in=[
                "Soutenance de thèse de Mohamed ABDILLAHI — Université Clermont Auvergne",
                "Soutenance de thèse d'Abdoulrazack MOHAMED — Université de La Rochelle",
            ]
        ).delete()

        jury = [
            {
                "category": Activity.Category.JURY,
                "title": "Examinateur — Soutenance de thèse de Mohamed ABDILLAHI ISMAN, Université Clermont Auvergne",
                "defaults": {
                    "year": "18 décembre 2024", "location": "Université Clermont Auvergne, France",
                    "people": "Dr Yahyeh SOULEIMAN ISMAN — Examinateur", "sort_date": date(2024, 12, 18), "order": 1,
                    "description": (
                        "École doctorale : Sciences Fondamentales — Laboratoire : LMBP – Laboratoire de "
                        "Mathématiques Blaise Pascal (Équipe PAS) — Spécialité : Mathématiques appliquées "
                        "et applications des mathématiques.\n\n"
                        "Titre de la thèse : « Contribution à la modélisation de la demande en électricité "
                        "et à l'estimation non paramétrique à noyau de la densité dans des variétés "
                        "riemanniennes ».\n\n"
                        "Directrice de thèse : Pr Anne-Françoise Yao. Co-directeurs : Pr Julien Ah Pine et "
                        "Pr Paul-Marie Grollemund.\n\n"
                        "Le Dr Yahyeh SOULEIMAN ISMAN a participé à cette soutenance en qualité "
                        "d'examinateur. Cette nomination reflète la reconnaissance de son expertise "
                        "scientifique dans le domaine des mathématiques appliquées et de la modélisation. "
                        "Elle illustre également son engagement dans l'évaluation de travaux de recherche "
                        "doctorale et contribue au renforcement des collaborations scientifiques entre "
                        "l'Université de Djibouti et les établissements d'enseignement supérieur français."
                    ),
                    "image": "formation_jury_clermont_2024.jpeg",
                },
            },
            {
                "category": Activity.Category.JURY,
                "title": "Co-encadrement — Thèse d'Abdoulrazack MOHAMED ABDI, La Rochelle Université",
                "defaults": {
                    "year": "11 décembre 2024", "location": "La Rochelle Université, France",
                    "people": "Dr Yahyeh SOULEIMAN ISMAN — Co-encadrant", "sort_date": date(2024, 12, 11), "order": 2,
                    "description": (
                        "École doctorale : EUCLIDE — Laboratoire : MIA – Mathématiques, Images et "
                        "Applications — Discipline : Mathématiques appliquées.\n\n"
                        "Titre de la thèse : « Contribution mathématique à l'analyse de systèmes "
                        "différentiels modélisant la transmission ».\n\n"
                        "Directrice de thèse : Pr Catherine Choquet. Co-encadrant : Dr Yahyeh Souleiman "
                        "Isman (Université de Djibouti).\n\n"
                        "Le Dr Yahyeh SOULEIMAN ISMAN a assuré le co-encadrement scientifique de cette "
                        "thèse de doctorat en collaboration avec la directrice de thèse. Cette activité "
                        "témoigne de son implication dans la formation par la recherche, le développement "
                        "de collaborations scientifiques internationales et le renforcement des "
                        "partenariats académiques entre l'Université de Djibouti et La Rochelle Université."
                    ),
                    "image": "formation_jury_larochelle_2024.jpeg",
                },
            },
            {
                "category": Activity.Category.JURY,
                "title": "Invité — Soutenance de thèse du Dr Liban ISMAIL ABDILLAHI, Université Clermont Auvergne",
                "defaults": {
                    "year": "28 juin 2023", "location": "Université Clermont Auvergne, France",
                    "people": "Dr Yahyeh SOULEIMAN ISMAN — Invité", "sort_date": date(2023, 6, 28), "order": 3,
                    "description": (
                        "École doctorale : École doctorale des Sciences fondamentales — Laboratoire : LMBP "
                        "– Laboratoire de Mathématiques Blaise Pascal — Discipline : Mathématiques "
                        "appliquées.\n\n"
                        "Titre de la thèse : « Analyse de sensibilité appliquée à certains modèles issus "
                        "du climat, de l'épidémiologie et de la finance ».\n\n"
                        "Directeur de thèse : Pr Hacène Djellout. Président du jury : Pr Pierre Druilhet. "
                        "Rapporteurs : Pr Frédéric Proïa et Pr Raluca Eftimie.\n\n"
                        "Le Dr Yahyeh SOULEIMAN ISMAN a été invité à assister à cette soutenance de thèse "
                        "de doctorat, illustrant son intégration au sein des collaborations scientifiques "
                        "entretenues avec le Laboratoire de Mathématiques Blaise Pascal (LMBP) et les "
                        "équipes de recherche de l'Université Clermont Auvergne. Cette participation a "
                        "favorisé le développement de collaborations académiques et le renforcement des "
                        "échanges scientifiques dans le domaine des mathématiques appliquées."
                    ),
                    "image": "formation_jury_liban_these_2023.jpeg",
                },
            },
        ]
        self._seed_activity_rows(jury)

        stages = [
            {
                "category": Activity.Category.STAGE,
                "title": "Magdi ALI — Étude comparative des méthodes d'explicabilité pour la détection des biais dans les modèles de classification",
                "defaults": {
                    "year": "2025–2026", "people": "Encadrement : Dr Liban ISMAIL ABDILLAHI et Dr Souleiman OMAR HOCH",
                    "sort_date": date(2026, 1, 1), "order": 1,
                    "description": "Application aux données de crédit bancaire, dans le cadre du stage de fin d'études du Master IAMD.",
                },
            },
            {
                "category": Activity.Category.STAGE,
                "title": "Ahmed ILMI — Analyse du prix de vente des maisons : étude prédictive",
                "defaults": {
                    "year": "2025–2026", "people": "Encadrement : Dr Liban ISMAIL ABDILLAHI et Dr Souleiman OMAR HOCH",
                    "sort_date": date(2026, 1, 1), "order": 2,
                    "description": "Étude prédictive basée sur le jeu de données Ames Housing, dans le cadre du stage de fin d'études du Master IAMD.",
                },
            },
            {
                "category": Activity.Category.STAGE,
                "title": "Houssein AHMED — Prédiction de séries temporelles météorologiques réelles",
                "defaults": {
                    "year": "2025–2026", "people": "Encadrement : Dr Liban ISMAIL ABDILLAHI et Dr Souleiman OMAR HOCH",
                    "sort_date": date(2026, 1, 1), "order": 3,
                    "description": "Stage de fin d'études du Master IAMD portant sur la prévision de séries temporelles météorologiques réelles.",
                },
            },
        ]
        self._seed_activity_rows(stages)

        capacity = [
            {
                "category": Activity.Category.CAPACITY,
                "title": "Formation internationale sur le logiciel CROCO",
                "defaults": {
                    "year": "Novembre 2024", "location": "Barcelonnette, France",
                    "people": "Dr Liban ISMAIL et M. Hakim AMER", "sort_date": date(2024, 11, 1), "order": 1,
                    "description": (
                        "Formation internationale consacrée au logiciel CROCO (Coastal and Regional Ocean "
                        "Community Model), réunissant des chercheurs et des spécialistes travaillant dans "
                        "le domaine de la modélisation océanique et environnementale. Cette formation a "
                        "permis d'approfondir les connaissances relatives à la mise en œuvre des modèles "
                        "hydrodynamiques, un atout important pour le développement des activités de "
                        "recherche du laboratoire en modélisation des systèmes complexes, environnement "
                        "marin et érosion côtière."
                    ),
                    "image": "formation_croco_training_2024.jpeg",
                },
            },
        ]
        self._seed_activity_rows(capacity)

    def seed_partners(self):
        academic = [
            ("Université La Rochelle", "partner_la_rochelle.png", "France", "https://www.univ-larochelle.fr/"),
            ("Université Marie et Louis Pasteur", "partner_marie_louis_pasteur.png", "France", "https://www.umlp.fr/"),
            ("Adama Science and Technology University", "partner_adama.png", "Éthiopie", "https://www.astu.edu.et/"),
            ("Université Clermont Auvergne", "partner_clermont_auvergne.jpeg", "France", "https://www.uca.fr/"),
            ("Université Le Havre Normandie", "partner_le_havre_normandie.png", "France", "https://www.univ-lehavre.fr/"),
            ("Université de Toulon", "partner_toulon.png", "France", "https://www.univ-tln.fr/"),
            ("Université de Nantes", "partner_nantes.png", "France", "https://www.univ-nantes.fr/"),
            ("Amoud University", "partner_amoud.png", "Somalie", "https://amouduniversity.org/"),
            ("Université de Lorraine", "partner_lorraine.png", "France", "https://www.univ-lorraine.fr/"),
        ]
        institutional = [
            ("Institut National de Santé Publique de Djibouti", "partner_inspd.png", "Djibouti", "https://inspdj.net/"),
            ("INSTAD - Institut National de la Statistique de Djibouti", "partner_instad.png", "Djibouti", "https://instad.dj/"),
            ("DPCS - Djibouti Port Community Systems", "partner_dpcs.png", "Djibouti", "https://www.dpcs.dj/"),
            ("Service de Santé des Armées", "partner_service_sante_armees.png", "Djibouti", ""),
            ("DPCR - Djibouti Ports Corridor Road", "partner_dpcr.png", "Djibouti", "https://dpcr.dj/"),
            ("SGTD - Société de Gestion du Terminal à Conteneurs de Doraleh", "partner_sgtd.png", "Djibouti", "https://www.sgtd-terminal.com/"),
        ]
        for order, (name, filename, country, website) in enumerate(academic, start=1):
            partner, _ = Partner.objects.update_or_create(
                name=name,
                defaults={"category": Partner.Category.ACADEMIC, "country": country, "website": website, "order": order},
            )
            attach_image(partner, "logo", filename)

        for order, (name, filename, country, website) in enumerate(institutional, start=1):
            partner, _ = Partner.objects.update_or_create(
                name=name,
                defaults={"category": Partner.Category.INSTITUTIONAL, "country": country, "website": website, "order": order},
            )
            attach_image(partner, "logo", filename)

    def seed_publications(self):
        rows = [
            ("Haile Getachew Fetene, Yahyeh Souleiman, and Legesse Lemecha Obsu",
             "A Fractional Mathematical Model of Malaria Transmission Dynamics with Liver Stage Relapse",
             "Discover Applied Sciences, 2026", False, "https://doi.org/10.1007/s42452-026-09116-9", "DOI", 2026),
            ("Yahyeh Souleiman, Liban Ismail, and Legesse Lemecha Obsu",
             "Optimal Control Strategies and Cost-Effectiveness Analysis of Malaria for Plasmodium falciparum and Plasmodium vivax in Djibouti",
             "Scientific African, 31 (2026): e03262", False, "https://doi.org/10.1016/j.sciaf.2026.e03262", "DOI", 2026),
            ("Yahyeh Souleiman, Liban Ismail, and Raluca Eftimie",
             "Modeling and Investigating Plasmodium falciparum and Plasmodium vivax Infections: Application to Djibouti Data",
             "Infectious Disease Modelling, 9(4) (2024): 1095–1116", False, "https://doi.org/10.1016/j.idm.2024.05.005", "DOI", 2024),
            ("Liban Ismail, Hacène Djellout, and Cédric Chauvière",
             "Global Sensitivity Analysis in the SIHR Epidemiological Model with Application to COVID-19",
             "Journal of Statistics & Management Systems, 27(7) (2024): 1277–1299", False, "https://doi.org/10.47974/JSMS-1019", "DOI", 2024),
            ("Liban Ismail, Hacène Djellout, and Cédric Chauvière",
             "Climate System: A Global Sensitivity Approach",
             "Iranian Journal of Science, 47(1) (2023): 211–227", False, "https://doi.org/10.1007/s40995-022-01456-4", "DOI", 2023),
            ("Yahyeh Souleiman, Abdoulrazack Mohamed, and Liban Ismail",
             "Analysis of the Dynamics of the SIHR Model: COVID-19 Case in Djibouti",
             "Applied Mathematics, 12(10) (2021): 867–881", False, "https://doi.org/10.4236/am.2021.1210058", "DOI", 2021),
            ("Liban Ismail, Yahyeh Souleiman, Saralees Nadarajah, and Abdisalam Hassan",
             "Time-Dependent Intervention Modeling and Global Sensitivity Analysis of Epidemic Dynamics under Uncertainty in Resource-Limited African Settings",
             "À paraître", True, "", "", 2026),
            ("Gouled Souleiman, Nathalie Verdière, Alexandre Berred, Yahyeh Souleiman, Simon Badji, et al.",
             "Optimal Control and Calibration Modeling of Forest Regeneration Under Anthropogenic Pressures: the Day Forest Ecosystem (Djibouti)",
             "Modeling Earth Systems and Environment, 2026 — à paraître", True, "https://hal.science/", "HAL", 2026),
            ("Said Ismail, Benjamin Ambrosio, Moulay Ahmed Aziz-Alaoui, and Yahyeh Souleiman",
             "A Dynamical System Approach to Modeling Neural Network Activity in Drosophila Orientation",
             "À paraître", True, "", "", 2026),
            ("Gouled Souleiman, Nathalie Verdière, Alexandre Berred, and Yahyeh Souleiman",
             "A Mathematical Model to Investigate the Impact of Climate Change on Forest Ecosystems and a Strategy for Its Regeneration",
             "À paraître", True, "", "", 2026),
            ("Yahyeh Souleiman",
             "Convergences and Numerical Analysis of a Contact Problem with Normal Compliance and Unilateral Constraint",
             "African Journal of Mathematics and Computer Science Research, 14(1) (2021): 13–23", False, "https://doi.org/10.5897/AJMCSR2020.0865", "DOI", 2021),
            ("Yahyeh Souleiman and Mikael Barboteu",
             "Numerical Analysis of a Sliding Frictional Contact Problem with Normal Compliance and Unilateral Contact",
             "Open Journal of Modelling and Simulation, 9(4) (2021): 385–402", False, "https://doi.org/10.4236/ojmsi.2021.94025", "DOI", 2021),
            ("Mircea Sofonea and Yahyeh Souleiman",
             "Analysis of a Sliding Frictional Contact Problem with Unilateral Constraint",
             "Mathematics and Mechanics of Solids, 22(3) (2017): 324–342", False, "https://doi.org/10.1177/1081286515591304", "DOI", 2017),
            ("Mircea Sofonea, Flavius Pétrulescu, and Yahyeh Souleiman",
             "Analysis of a Contact Problem with Wear and Unilateral Constraint",
             "Applicable Analysis, 95(11) (2016): 2590–2607", False, "https://doi.org/10.1080/00036811.2015.1102892", "DOI", 2016),
            ("Mircea Sofonea and Yahyeh Souleiman",
             "A Viscoelastic Sliding Contact Problem with Normal Compliance, Unilateral Constraint and Memory Term",
             "Mediterranean Journal of Mathematics, 13(5) (2016): 2863–2886", False, "https://doi.org/10.1007/s00009-015-0661-9", "DOI", 2016),
            ("Alexandru Chirvasitu and Souleiman Omar Hoch",
             "Ergodic Actions of the Compact Quantum Group O₋₁(2)",
             "arXiv Preprint, 2017", False, "https://arxiv.org/", "arXiv", 2017),
            ("Alexandru Chirvasitu, Souleiman Omar Hoch, and Paweł Kasprzak",
             "Fundamental Isomorphism Theorems for Quantum Groups",
             "Expositiones Mathematicae", False, "https://doi.org/10.1016/j.exmath.2019.02.002", "DOI", None),
        ]
        for order, (authors, title, reference, forthcoming, link, link_label, year) in enumerate(rows, start=1):
            Publication.objects.update_or_create(
                title=title,
                defaults={
                    "authors": authors, "reference": reference, "is_forthcoming": forthcoming,
                    "link": link, "link_label": link_label, "year": year, "order": order,
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
                "title": (
                    "Contribution à la modélisation, à l'analyse et au contrôle des systèmes complexes : "
                    "applications à la santé, à l'environnement et à l'aide à la décision"
                ),
                "period_label": "2027–2028",
                "garant": "Pr Raluca Eftimie",
                "institutions": "Université de Djibouti – Université Marie et Louis Pasteur (France)",
                "specialization": (
                    "Modélisation mathématique des systèmes complexes : santé publique, environnement et "
                    "aide à la décision."
                ),
                "description": (
                    "Cette Habilitation à Diriger des Recherches (HDR), actuellement en cours de "
                    "réalisation, a pour objectif de présenter une synthèse des contributions "
                    "scientifiques développées au cours des dernières années dans le domaine de la "
                    "modélisation mathématique des systèmes complexes. Les travaux s'inscrivent à "
                    "l'interface des mathématiques appliquées, de la santé publique, des sciences de "
                    "l'environnement et de l'aide à la décision, en mobilisant des approches théoriques, "
                    "numériques et computationnelles.\n\n"
                    "Les recherches portent principalement sur la modélisation des maladies infectieuses, "
                    "la modélisation des systèmes écologiques et environnementaux, l'analyse qualitative "
                    "des systèmes dynamiques, la modélisation d'ordre fractionnaire, l'optimisation et le "
                    "contrôle optimal. Elles visent à développer des modèles mathématiques robustes, à "
                    "analyser leurs propriétés dynamiques, à identifier les paramètres influents, à "
                    "évaluer l'impact des stratégies d'intervention et à proposer des outils d'aide à la "
                    "décision destinés aux acteurs publics et aux décideurs.\n\n"
                    "Cette HDR est réalisée sous la responsabilité scientifique du Pr Raluca Eftimie, "
                    "Professeure à l'Université Marie et Louis Pasteur (France), dans le cadre d'une "
                    "collaboration scientifique entre l'Université de Djibouti et l'Université Marie et "
                    "Louis Pasteur. Elle contribue au renforcement des coopérations internationales en "
                    "recherche, au développement des activités scientifiques du Laboratoire d'Analyse, de "
                    "Modélisation et d'Optimisation (LAMO) et à la consolidation de la formation doctorale "
                    "au sein de l'Université de Djibouti.\n\n"
                    "L'objectif de cette habilitation est de démontrer la capacité du candidat à conduire "
                    "des recherches de manière autonome, à définir de nouveaux axes scientifiques, à "
                    "piloter des projets de recherche et à encadrer des doctorants. À plus long terme, "
                    "elle ouvrira de nouvelles perspectives de recherche dans les domaines de la "
                    "modélisation mathématique, de l'intelligence artificielle, de la science des données "
                    "et des systèmes complexes, tout en contribuant au rayonnement scientifique de "
                    "l'Université de Djibouti sur les plans régional et international."
                ),
                "order": 1,
            },
        )
