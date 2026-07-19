from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from lab.models import (
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
    help = "Charge les données réelles du LAMO (profil, équipes, membres, partenaires)."

    def handle(self, *args, **options):
        self.seed_profile()
        team_dyn, team_sto = self.seed_teams()
        self.seed_themes(team_dyn, team_sto)
        self.seed_permanent_members(team_dyn, team_sto)
        self.seed_doctorants()
        self.seed_associates()
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
                "name": "Systèmes Dynamiques & Contrôle",
                "short_description": (
                    "Modélisation, analyse, simulation numérique et contrôle de systèmes "
                    "dynamiques complexes."
                ),
                "description": (
                    "Cette équipe développe des approches mathématiques pour la modélisation, "
                    "l’analyse, la simulation numérique et le contrôle de systèmes dynamiques "
                    "complexes issus de divers domaines d’application."
                ),
                "order": 1,
            },
        )
        team_sto, _ = ResearchTeam.objects.update_or_create(
            slug="stochastiques-sciences-donnees",
            defaults={
                "name": "Stochastiques et Sciences de Données",
                "short_description": (
                    "Méthodes probabilistes, statistiques et intelligence artificielle au "
                    "service de la décision."
                ),
                "description": (
                    "Cette équipe s’intéresse au développement de méthodes probabilistes, "
                    "statistiques, de simulation numérique et d’intelligence artificielle pour "
                    "l’analyse, la modélisation, la prévision et l’aide à la décision dans des "
                    "contextes complexes."
                ),
                "order": 2,
            },
        )
        return team_dyn, team_sto

    def seed_themes(self, team_dyn, team_sto):
        themes = [
            ("Équations différentielles, systèmes dynamiques et analyse des systèmes", team_dyn, 1),
            ("Contrôle optimal et modélisation des phénomènes complexes", team_dyn, 2),
            ("Biomathématiques et bio-statistique (modélisation épidémiologique)", team_dyn, 3),
            ("Processus stochastiques, probabilités et incertitude", team_sto, 4),
            ("Statistique, science des données et intelligence artificielle", team_sto, 5),
            ("Recherche opérationnelle, optimisation, simulation et aide à la décision", team_sto, 6),
        ]
        for title, team, order in themes:
            ResearchTheme.objects.update_or_create(
                title=title, defaults={"team": team, "order": order}
            )

    def seed_permanent_members(self, team_dyn, team_sto):
        members = [
            ("Dr. Liban ISMAIL", "Maître de conférences en Mathématiques appliquées", True, team_dyn,
             "Directeur du LAMO. Ses travaux portent sur la modélisation et le contrôle de systèmes dynamiques complexes, avec des collaborations internationales autour de l'encadrement doctoral."),
            ("Dr. Yahyeh SOULEIMAN", "Maître de conférences en Mathématiques appliquées", False, team_sto,
             "Recherches en méthodes probabilistes et statistiques appliquées, avec un fort investissement dans l'encadrement de doctorants en cotutelle."),
            ("Dr. Souleiman OMAR", "Maître de conférences en Mathématiques fondamentales", False, team_dyn,
             "Travaux en analyse mathématique et systèmes dynamiques, au service de la modélisation de phénomènes complexes."),
            ("Dr. Doualeh ABDILLAHI", "Maître de conférences en Statistiques appliquées", False, team_sto,
             "Spécialiste de statistique appliquée et de science des données, au service de projets interdisciplinaires du laboratoire."),
        ]
        for order, (full_name, title, is_director, team, bio) in enumerate(members, start=1):
            PermanentMember.objects.update_or_create(
                full_name=full_name,
                defaults={"title": title, "is_director": is_director, "team": team, "bio": bio, "order": order},
            )

    def seed_doctorants(self):
        rows = [
            ("M. Said ISMAIL", "2023", "Université Le Havre (LMAH)", "B. Ambrosio ; M.A. Aziz Alaoui", "Yahyeh Souleiman"),
            ("M. Getachew FETENE", "2025", "Adama Science and Technology University", "Lemecha Legesse", "Yahyeh Souleiman"),
            ("M. Ali MOHAMED", "2024", "Université La Rochelle (LMIA)", "S. Kadri-Harouna & Kaïs Ammari", "Liban Ismail"),
            ("M. Gouled SOULEIMAN", "2024", "Université Le Havre (LMAH)", "N. Verdière & A. Berred", "Yahyeh Souleiman"),
            ("Mme. Saida BALLAH", "2024", "Université de Nantes (ONIRIS)", "Mohamed Hanafi", "Souleiman Omar"),
            ("M. Hakim AMER", "2026", "Université de Toulon", "Mehmet Ersoy", "Liban Ismail"),
            ("M. Kadir ALI", "2026", "Université Marie et Louis Pasteur (LmB)", "Raluca Eftimie", "Yahyeh Souleiman"),
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
            ("Mme. Raluca EFTIMIE", "Professeure", "Université Marie et Louis Pasteur (Besançon)", "France"),
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
