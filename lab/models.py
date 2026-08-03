from django.db import models
from django.urls import reverse


class LabProfile(models.Model):
    """Singleton holding the laboratory's identity and general presentation."""

    name = models.CharField(max_length=255, default="Laboratoire d'Analyse, de Modélisation et d'Optimisation")
    acronym = models.CharField(max_length=20, default="LAMO")
    affiliation = models.CharField(
        max_length=500,
        default="Laboratoire de Recherche en Mathématiques et Numérique (LRMN), Université de Djibouti",
    )
    mission = models.TextField(
        help_text="Paragraphe de mission (première section de la présentation)."
    )
    presentation_extra = models.TextField(
        blank=True,
        help_text="Paragraphes complémentaires de présentation, séparés par une ligne vide.",
    )
    teams_intro = models.TextField(
        blank=True, help_text="Texte d'introduction affiché au-dessus des équipes de recherche."
    )
    teams_conclusion = models.TextField(
        blank=True,
        help_text="Paragraphe sur la complémentarité des équipes, affiché en bas de la page Équipes.",
    )

    address = models.CharField(max_length=500, blank=True)
    director_name = models.CharField(max_length=255, blank=True)
    email_primary = models.EmailField(blank=True)
    email_secondary = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    logo = models.ImageField(upload_to="brand/", blank=True, null=True)
    university_logo = models.ImageField(upload_to="brand/", blank=True, null=True)

    class Meta:
        verbose_name = "Profil du laboratoire"
        verbose_name_plural = "Profil du laboratoire"

    def __str__(self):
        return self.acronym

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={"mission": ""})
        return obj


class ResearchTeam(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=400, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Équipe de recherche"
        verbose_name_plural = "Équipes de recherche"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("lab:team_detail", args=[self.slug])


class ResearchTheme(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    team = models.ForeignKey(
        ResearchTeam, on_delete=models.SET_NULL, null=True, blank=True, related_name="themes"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Thématique de recherche"
        verbose_name_plural = "Thématiques de recherche"

    def __str__(self):
        return self.title


class PermanentMember(models.Model):
    full_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, help_text="Grade / spécialité")
    role_tag = models.CharField(
        max_length=120, blank=True,
        help_text="Fonction complémentaire affichée en badge, ex : Doyen de l'IUT-T",
    )
    team = models.ForeignKey(
        ResearchTeam, on_delete=models.SET_NULL, null=True, blank=True, related_name="members"
    )
    is_director = models.BooleanField(default=False)
    email = models.EmailField(blank=True)
    email_secondary = models.EmailField(blank=True)
    phone = models.CharField(max_length=120, blank=True, help_text="Un ou plusieurs numéros, séparés par « | ».")
    photo = models.ImageField(upload_to="members/", blank=True, null=True)
    bio = models.TextField(blank=True, help_text="Présentation courte affichée sur la fiche du membre.")
    thesis_link = models.URLField(blank=True, help_text="Lien vers la thèse de doctorat du membre.")
    scholar_link = models.URLField(blank=True, help_text="Lien vers le profil Google Scholar / liste des articles du membre.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "full_name"]
        verbose_name = "Membre permanent"
        verbose_name_plural = "Membres permanents"

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse("lab:member_permanent_detail", args=[self.pk])


class Doctorant(models.Model):
    full_name = models.CharField(max_length=255)
    start_year = models.CharField(max_length=9, help_text="Ex : 2023 ou 2025-2026")
    partner_university = models.CharField(max_length=255)
    thesis_director = models.CharField(max_length=255)
    co_supervisor = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True, help_text="Adresse électronique universitaire du doctorant.")
    photo = models.ImageField(upload_to="members/", blank=True, null=True)
    bio = models.TextField(blank=True, help_text="Sujet de thèse ou présentation courte.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-start_year", "order", "full_name"]
        verbose_name = "Doctorant"
        verbose_name_plural = "Doctorants"

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse("lab:member_doctorant_detail", args=[self.pk])


class AssociateResearcher(models.Model):
    full_name = models.CharField(max_length=255)
    grade = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    country = models.CharField(max_length=120)
    photo = models.ImageField(upload_to="members/", blank=True, null=True)
    bio = models.TextField(blank=True, help_text="Présentation courte affichée sur la fiche du chercheur.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "full_name"]
        verbose_name = "Chercheur associé"
        verbose_name_plural = "Chercheurs associés"

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse("lab:member_associate_detail", args=[self.pk])


class Partner(models.Model):
    class Category(models.TextChoices):
        ACADEMIC = "academic", "Partenaire académique"
        INSTITUTIONAL = "institutional", "Partenaire institutionnel & socio-économique"

    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="partners/")
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.ACADEMIC)
    country = models.CharField(max_length=120, blank=True)
    website = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "name"]
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"

    def __str__(self):
        return self.name


class Activity(models.Model):
    class Category(models.TextChoices):
        CONFERENCE = "conference", "Conférence"
        SEMINAIRE = "seminaire", "Séminaire"
        OLYMPIADES = "olympiades", "Olympiades"
        OFFRE = "offre", "Offre de thèse et de stage"
        PARTICIPATION = "participation", "Participation à une manifestation scientifique"
        EDITORIAL = "editorial", "Responsabilité éditoriale"
        JURY = "jury", "Participation à un jury de thèse"
        STAGE = "stage", "Encadrement de stage"
        CAPACITY = "capacity", "Renforcement de capacités"

    category = models.CharField(max_length=20, choices=Category.choices)
    title = models.CharField(max_length=255, help_text="Ex : 2e édition — M2ISDA 2027")
    edition_label = models.CharField(max_length=100, blank=True, help_text="Ex : 1ère édition, Édition 2025")
    year = models.CharField(max_length=20, blank=True, help_text="Date ou période de l'activité.")
    location = models.CharField(max_length=255, blank=True)
    people = models.CharField(
        max_length=500, blank=True,
        help_text="Présentateur, intervenant ou représentation du LAMO, ex : Dr Yahyeh SOULEIMAN",
    )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="activities/", blank=True, null=True)
    image_fit_contain = models.BooleanField(
        default=False,
        help_text="Cocher pour les visuels/affiches qui doivent rester entièrement visibles sans recadrage.",
    )
    link = models.URLField(blank=True, help_text="Lien externe (inscription, appel à candidature...)")
    document = models.FileField(
        upload_to="activities/documents/", blank=True, null=True,
        help_text="Document à télécharger (livret, programme...).",
    )
    document_label = models.CharField(
        max_length=100, blank=True, default="Télécharger le livret",
        help_text="Texte du bouton de téléchargement.",
    )
    video = models.FileField(
        upload_to="activities/videos/", blank=True, null=True,
        help_text="Vidéo à regarder directement sur la page (mp4).",
    )
    video_label = models.CharField(
        max_length=100, blank=True, default="Vidéo",
        help_text="Légende affichée au-dessus du lecteur vidéo.",
    )
    sort_date = models.DateField(
        null=True, blank=True,
        help_text="Date utilisée uniquement pour classer l'activité de la plus récente à la plus ancienne.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "-sort_date", "order"]
        verbose_name = "Activité"
        verbose_name_plural = "Activités"

    def __str__(self):
        return f"{self.get_category_display()} — {self.title}"

    def all_images(self):
        images = []
        if self.image:
            images.append(self.image)
        images += [gi.image for gi in self.gallery.all()]
        return images


class ActivityImage(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="activities/gallery/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Photo supplémentaire d'activité"
        verbose_name_plural = "Photos supplémentaires d'activité"

    def __str__(self):
        return f"Photo de {self.activity.title}"


class MasterCourse(models.Model):
    program = models.CharField(max_length=255, help_text="Ex : Master 1 IAMD")
    course_title = models.CharField(max_length=255)
    instructor = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Cours de Master"
        verbose_name_plural = "Cours de Master"

    def __str__(self):
        return f"{self.program} — {self.course_title}"


class Publication(models.Model):
    authors = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    reference = models.CharField(
        max_length=300, blank=True,
        help_text="Revue, volume, pages, année. Ex : Scientific African, 31 (2026): e03262.",
    )
    is_forthcoming = models.BooleanField(default=False, help_text="Coché si l'article est « à paraître ».")
    link = models.URLField(blank=True, help_text="Lien DOI, HAL ou arXiv de l'article.")
    link_label = models.CharField(max_length=20, default="DOI", blank=True)
    year = models.PositiveIntegerField(
        null=True, blank=True, help_text="Année de publication, utilisée pour classer les articles du plus récent au plus ancien.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-year", "order"]
        verbose_name = "Publication"
        verbose_name_plural = "Publications"

    def __str__(self):
        return self.title


class ResearchProject(models.Model):
    class Status(models.TextChoices):
        COMPLETED = "completed", "Projet réalisé"
        ONGOING = "ongoing", "Projet en cours"

    title = models.CharField(max_length=500)
    funder = models.CharField(max_length=255, blank=True)
    period = models.CharField(max_length=100, blank=True)
    amount = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ONGOING)
    description = models.TextField(blank=True)
    related_publications = models.ManyToManyField(Publication, blank=True, related_name="projects")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-order"]
        verbose_name = "Projet de recherche"
        verbose_name_plural = "Projets de recherche"

    def __str__(self):
        return self.title


class Habilitation(models.Model):
    full_name = models.CharField(max_length=255)
    title = models.CharField(max_length=500, blank=True, help_text="Titre des travaux de l'HDR.")
    period_label = models.CharField(max_length=100, blank=True)
    garant = models.CharField(max_length=255, blank=True, help_text="Garant de l'HDR")
    institutions = models.CharField(max_length=500, blank=True)
    specialization = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Habilitation à Diriger des Recherches"
        verbose_name_plural = "Habilitations à Diriger des Recherches"

    def __str__(self):
        return self.full_name


class News(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    excerpt = models.CharField(max_length=400, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="news/", blank=True, null=True, help_text="Affiche ou visuel associé à l'actualité.")
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"

    def __str__(self):
        return self.title
