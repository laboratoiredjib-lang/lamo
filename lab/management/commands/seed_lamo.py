from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from lab.models import (
    Activity,
    AssociateResearcher,
    Doctorant,
    LabProfile,
    Partner,
    PermanentMember,
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
            ("M. Said ISMAIL", "2023", "Université Le Havre (LMAH)", "B. Ambrosio & M.A. Aziz Alaoui", "Yahyeh Souleiman"),
            ("M. Ali MOHAMED", "2024", "Université La Rochelle (LMIA)", "S. Kadri-Harouna & Kaïs Ammari", "Liban Ismail"),
            ("M. Gouled SOULEIMAN", "2024", "Université Le Havre (LMAH)", "N. Verdière & A. Berred", "Yahyeh Souleiman"),
            ("Mme. Saida BALLAH", "2024", "Université de Nantes (ONIRIS)", "Mohamed Hanafi", "Souleiman Omar"),
            ("M. Getachew FETENE", "2025", "Adama Science and Technology University", "Lemecha Legesse", "Yahyeh Souleiman"),
            ("M. Hakim AMER", "2026", "Université de Toulon", "Mehmet Ersoy", "Liban Ismail & Mohamed Yacin"),
            ("M. Kadir ALI", "2027", "Université Marie et Louis Pasteur (LmB)", "Raluca Eftimie", "Yahyeh Souleiman"),
            ("M. Ismail ABDILLAHI", "2027", "Université Clermont Auvergne", "Andrezj Stos", "Liban Ismail"),
        ]
        for order, (full_name, start_year, partner_university, thesis_director, co_supervisor) in enumerate(rows, start=1):
            Doctorant.objects.update_or_create(
                full_name=full_name,
                defaults={
                    "start_year": start_year,
                    "partner_university": partner_university,
                    "thesis_director": thesis_director,
                    "co_supervisor": co_supervisor,
                    "bio": f"Thèse en cotutelle avec {partner_university}, sous la direction de {thesis_director}.",
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
