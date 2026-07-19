from django.db import models
from django.urls import reverse


class LabProfile(models.Model):
    """Singleton holding the laboratory's identity and general presentation."""

    name = models.CharField(max_length=255, default="Laboratoire d'Analyse, de Modélisation et d'Optimisation")
    acronym = models.CharField(max_length=20, default="LAMO")
    affiliation = models.CharField(
        max_length=500,
        default="Centre de Recherche en Mathématiques et Numérique (CRMN), Université de Djibouti",
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
    team = models.ForeignKey(
        ResearchTeam, on_delete=models.SET_NULL, null=True, blank=True, related_name="members"
    )
    is_director = models.BooleanField(default=False)
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to="members/", blank=True, null=True)
    bio = models.TextField(blank=True, help_text="Présentation courte affichée sur la fiche du membre.")
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
    photo = models.ImageField(upload_to="members/", blank=True, null=True)
    bio = models.TextField(blank=True, help_text="Sujet de thèse ou présentation courte.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "start_year", "full_name"]
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


class News(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    excerpt = models.CharField(max_length=400, blank=True)
    content = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"

    def __str__(self):
        return self.title
