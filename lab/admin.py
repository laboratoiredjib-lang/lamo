from django.contrib import admin
from django.urls import reverse

from unfold.admin import ModelAdmin, TabularInline

from .models import (
    Activity,
    ActivityImage,
    AssociateResearcher,
    Doctorant,
    Habilitation,
    LabProfile,
    MasterCourse,
    News,
    Partner,
    PermanentMember,
    Publication,
    ResearchProject,
    ResearchTeam,
    ResearchTheme,
)


def dashboard_callback(request, context):
    """Alimente les cartes de statistiques du tableau de bord (UNFOLD.DASHBOARD_CALLBACK)."""
    stats = [
        ("Équipes de recherche", ResearchTeam.objects.count(), "diversity_3", "lab_researchteam_changelist"),
        ("Membres permanents", PermanentMember.objects.count(), "school", "lab_permanentmember_changelist"),
        ("Doctorants", Doctorant.objects.count(), "cast_for_education", "lab_doctorant_changelist"),
        ("Chercheurs associés", AssociateResearcher.objects.count(), "public", "lab_associateresearcher_changelist"),
        ("Publications", Publication.objects.count(), "article", "lab_publication_changelist"),
        ("Projets de recherche", ResearchProject.objects.count(), "science", "lab_researchproject_changelist"),
        ("Partenaires", Partner.objects.count(), "handshake", "lab_partner_changelist"),
        ("Actualités publiées", News.objects.filter(is_published=True).count(), "campaign", "lab_news_changelist"),
    ]
    context["dashboard_stats"] = [
        {"label": label, "value": value, "icon": icon, "href": reverse(f"admin:{url_name}")}
        for label, value, icon, url_name in stats
    ]
    return context


@admin.register(LabProfile)
class LabProfileAdmin(ModelAdmin):
    fieldsets = (
        ("Identité", {"fields": ("name", "acronym", "affiliation", "logo", "university_logo")}),
        ("Présentation", {"fields": ("mission", "presentation_extra", "teams_intro", "teams_conclusion")}),
        ("Contact", {"fields": ("address", "director_name", "email_primary", "email_secondary", "phone")}),
    )

    def has_add_permission(self, request):
        return not LabProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ResearchTeam)
class ResearchTeamAdmin(ModelAdmin):
    list_display = ("name", "order")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order",)


@admin.register(ResearchTheme)
class ResearchThemeAdmin(ModelAdmin):
    list_display = ("title", "team", "order")
    list_filter = ("team",)
    ordering = ("order",)


@admin.register(PermanentMember)
class PermanentMemberAdmin(ModelAdmin):
    list_display = ("full_name", "title", "role_tag", "team", "is_director", "order")
    list_filter = ("team", "is_director")
    ordering = ("order",)


@admin.register(Doctorant)
class DoctorantAdmin(ModelAdmin):
    list_display = ("full_name", "start_year", "partner_university", "thesis_director", "co_supervisor", "email")
    list_filter = ("start_year",)
    ordering = ("order",)


@admin.register(AssociateResearcher)
class AssociateResearcherAdmin(ModelAdmin):
    list_display = ("full_name", "grade", "institution", "country")
    list_filter = ("country",)
    ordering = ("order",)


@admin.register(Partner)
class PartnerAdmin(ModelAdmin):
    list_display = ("name", "category", "country", "order")
    list_filter = ("category",)
    ordering = ("category", "order")


@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = ("title", "date", "image", "is_published")
    list_filter = ("is_published",)
    ordering = ("-date",)


class ActivityImageInline(TabularInline):
    model = ActivityImage
    extra = 1


@admin.register(Activity)
class ActivityAdmin(ModelAdmin):
    list_display = ("title", "category", "edition_label", "year", "sort_date", "people", "order")
    list_filter = ("category",)
    inlines = [ActivityImageInline]
    ordering = ("category", "-sort_date", "order")


@admin.register(MasterCourse)
class MasterCourseAdmin(ModelAdmin):
    list_display = ("program", "course_title", "instructor", "order")
    list_filter = ("program",)
    ordering = ("order",)


@admin.register(Publication)
class PublicationAdmin(ModelAdmin):
    list_display = ("title", "authors", "reference", "year", "is_forthcoming", "order")
    list_filter = ("is_forthcoming",)
    ordering = ("-year", "order")


@admin.register(ResearchProject)
class ResearchProjectAdmin(ModelAdmin):
    list_display = ("title", "status", "funder", "period", "order")
    list_filter = ("status",)
    ordering = ("status", "order")


@admin.register(Habilitation)
class HabilitationAdmin(ModelAdmin):
    list_display = ("full_name", "title", "period_label", "garant", "order")
    ordering = ("order",)
