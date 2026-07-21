from django.contrib import admin

from .models import (
    Activity,
    AssociateResearcher,
    Doctorant,
    LabProfile,
    News,
    Partner,
    PermanentMember,
    ResearchTeam,
    ResearchTheme,
)


@admin.register(LabProfile)
class LabProfileAdmin(admin.ModelAdmin):
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
class ResearchTeamAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order",)


@admin.register(ResearchTheme)
class ResearchThemeAdmin(admin.ModelAdmin):
    list_display = ("title", "team", "order")
    list_filter = ("team",)
    ordering = ("order",)


@admin.register(PermanentMember)
class PermanentMemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "title", "role_tag", "team", "is_director", "order")
    list_filter = ("team", "is_director")
    ordering = ("order",)


@admin.register(Doctorant)
class DoctorantAdmin(admin.ModelAdmin):
    list_display = ("full_name", "start_year", "partner_university", "thesis_director", "co_supervisor")
    list_filter = ("start_year",)
    ordering = ("order",)


@admin.register(AssociateResearcher)
class AssociateResearcherAdmin(admin.ModelAdmin):
    list_display = ("full_name", "grade", "institution", "country")
    list_filter = ("country",)
    ordering = ("order",)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "country", "order")
    list_filter = ("category",)
    ordering = ("category", "order")


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "is_published")
    list_filter = ("is_published",)
    ordering = ("-date",)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "edition_label", "year", "order")
    list_filter = ("category",)
    ordering = ("category", "order")
