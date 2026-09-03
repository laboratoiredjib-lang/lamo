from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import (
    Activity,
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


def health_check(request):
    return HttpResponse("OK")


def home(request):
    context = {
        "profile": LabProfile.load(),
        "teams": ResearchTeam.objects.all(),
        "themes": ResearchTheme.objects.all()[:6],
        "news": News.objects.filter(is_published=True)[:3],
        "partners": Partner.objects.all()[:10],
        "stats": {
            "teams": ResearchTeam.objects.count(),
            "permanents": PermanentMember.objects.count(),
            "doctorants": Doctorant.objects.count(),
            "associates": AssociateResearcher.objects.count(),
            "publications": Publication.objects.count(),
            "projects": ResearchProject.objects.count(),
            "partners": Partner.objects.count(),
            "news": News.objects.filter(is_published=True).count(),
        },
    }
    return render(request, "lab/home.html", context)


def team_list(request):
    context = {
        "profile": LabProfile.load(),
        "teams": ResearchTeam.objects.prefetch_related("themes"),
    }
    return render(request, "lab/team_list.html", context)


def team_detail(request, slug):
    team = get_object_or_404(ResearchTeam, slug=slug)
    context = {
        "profile": LabProfile.load(),
        "team": team,
        "themes": team.themes.all(),
        "members": team.members.all(),
    }
    return render(request, "lab/team_detail.html", context)


def members_permanent(request):
    context = {
        "profile": LabProfile.load(),
        "members": PermanentMember.objects.select_related("team").all(),
        "active_tab": "permanents",
    }
    return render(request, "lab/members_permanent.html", context)


def member_permanent_detail(request, pk):
    member = get_object_or_404(PermanentMember.objects.select_related("team"), pk=pk)
    others = PermanentMember.objects.exclude(pk=pk)[:4]
    context = {"profile": LabProfile.load(), "member": member, "others": others, "active_tab": "permanents"}
    return render(request, "lab/member_permanent_detail.html", context)


def members_doctorants(request):
    context = {
        "profile": LabProfile.load(),
        "doctorants": Doctorant.objects.all(),
        "active_tab": "doctorants",
    }
    return render(request, "lab/members_doctorants.html", context)


def member_doctorant_detail(request, pk):
    member = get_object_or_404(Doctorant, pk=pk)
    others = Doctorant.objects.exclude(pk=pk)[:4]
    context = {"profile": LabProfile.load(), "member": member, "others": others, "active_tab": "doctorants"}
    return render(request, "lab/member_doctorant_detail.html", context)


def members_associates(request):
    context = {
        "profile": LabProfile.load(),
        "associates": AssociateResearcher.objects.all(),
        "active_tab": "associes",
    }
    return render(request, "lab/members_associates.html", context)


def member_associate_detail(request, pk):
    member = get_object_or_404(AssociateResearcher, pk=pk)
    others = AssociateResearcher.objects.exclude(pk=pk)[:4]
    context = {"profile": LabProfile.load(), "member": member, "others": others, "active_tab": "associes"}
    return render(request, "lab/member_associate_detail.html", context)


def partners(request):
    context = {
        "profile": LabProfile.load(),
        "counts": {
            "academic": Partner.objects.filter(category=Partner.Category.ACADEMIC).count(),
            "institutional": Partner.objects.filter(category=Partner.Category.INSTITUTIONAL).count(),
        },
    }
    return render(request, "lab/partners.html", context)


def partners_academic(request):
    context = {
        "profile": LabProfile.load(),
        "academic_partners": Partner.objects.filter(category=Partner.Category.ACADEMIC),
        "active_partners_tab": "academiques",
    }
    return render(request, "lab/partners_academic.html", context)


def partners_institutional(request):
    context = {
        "profile": LabProfile.load(),
        "institutional_partners": Partner.objects.filter(category=Partner.Category.INSTITUTIONAL),
        "active_partners_tab": "institutionnels",
    }
    return render(request, "lab/partners_institutional.html", context)


def partners_national(request):
    context = {
        "profile": LabProfile.load(),
        "active_partners_tab": "nationales",
    }
    return render(request, "lab/partners_national.html", context)


def partners_international(request):
    context = {
        "profile": LabProfile.load(),
        "active_partners_tab": "internationales",
    }
    return render(request, "lab/partners_international.html", context)


def news_list(request):
    context = {
        "profile": LabProfile.load(),
        "news": News.objects.filter(is_published=True),
    }
    return render(request, "lab/news_list.html", context)


def contact(request):
    context = {
        "profile": LabProfile.load(),
    }
    return render(request, "lab/contact.html", context)


def activities(request):
    activities_qs = Activity.objects.all()
    context = {
        "profile": LabProfile.load(),
        "counts": {
            "conferences": activities_qs.filter(category=Activity.Category.CONFERENCE).count(),
            "seminaires": activities_qs.filter(category=Activity.Category.SEMINAIRE).count(),
            "olympiades": activities_qs.filter(category=Activity.Category.OLYMPIADES).count(),
            "participations": activities_qs.filter(category=Activity.Category.PARTICIPATION).count(),
            "editorial": activities_qs.filter(category=Activity.Category.EDITORIAL).count(),
        },
    }
    return render(request, "lab/activities.html", context)


def activities_conferences(request):
    context = {
        "profile": LabProfile.load(),
        "activities": Activity.objects.filter(category=Activity.Category.CONFERENCE),
        "active_activity_tab": "conferences",
    }
    return render(request, "lab/activities_conferences.html", context)


def activities_seminaires(request):
    context = {
        "profile": LabProfile.load(),
        "activities": Activity.objects.filter(category=Activity.Category.SEMINAIRE),
        "active_activity_tab": "seminaires",
    }
    return render(request, "lab/activities_seminaires.html", context)


def activities_olympiades(request):
    context = {
        "profile": LabProfile.load(),
        "activities": Activity.objects.filter(category=Activity.Category.OLYMPIADES),
        "active_activity_tab": "olympiades",
    }
    return render(request, "lab/activities_olympiades.html", context)


def activities_participations(request):
    context = {
        "profile": LabProfile.load(),
        "activities": Activity.objects.filter(category=Activity.Category.PARTICIPATION),
        "active_activity_tab": "participations",
    }
    return render(request, "lab/activities_participations.html", context)


def activities_editorial(request):
    context = {
        "profile": LabProfile.load(),
        "activities": Activity.objects.filter(category=Activity.Category.EDITORIAL),
        "active_activity_tab": "editorial",
    }
    return render(request, "lab/activities_editorial.html", context)


def production(request):
    context = {
        "profile": LabProfile.load(),
        "counts": {
            "articles": Publication.objects.count(),
            "theses": Doctorant.objects.count(),
            "hdr": Habilitation.objects.count(),
            "projets": ResearchProject.objects.count(),
        },
    }
    return render(request, "lab/production.html", context)


def production_articles(request):
    context = {
        "profile": LabProfile.load(),
        "publications": Publication.objects.all(),
        "active_production_tab": "articles",
    }
    return render(request, "lab/production_articles.html", context)


def production_theses(request):
    context = {
        "profile": LabProfile.load(),
        "doctorants": Doctorant.objects.all(),
        "active_production_tab": "theses",
    }
    return render(request, "lab/production_theses.html", context)


def production_hdr(request):
    context = {
        "profile": LabProfile.load(),
        "habilitations": Habilitation.objects.all(),
        "active_production_tab": "hdr",
    }
    return render(request, "lab/production_hdr.html", context)


def production_projets(request):
    context = {
        "profile": LabProfile.load(),
        "projects": ResearchProject.objects.prefetch_related("related_publications"),
        "active_production_tab": "projets",
    }
    return render(request, "lab/production_projets.html", context)


def formations(request):
    context = {
        "profile": LabProfile.load(),
        "doctorants_count": Doctorant.objects.count(),
        "counts": {
            "masters": MasterCourse.objects.count(),
            "doctoral": Doctorant.objects.count(),
            "jury": Activity.objects.filter(category=Activity.Category.JURY).count(),
            "stage": Activity.objects.filter(category=Activity.Category.STAGE).count(),
            "capacity": Activity.objects.filter(category=Activity.Category.CAPACITY).count(),
        },
    }
    return render(request, "lab/formations.html", context)


def formations_masters(request):
    context = {
        "profile": LabProfile.load(),
        "courses": MasterCourse.objects.all(),
        "active_formation_tab": "masters",
    }
    return render(request, "lab/formations_masters.html", context)


def formations_doctoral(request):
    context = {
        "profile": LabProfile.load(),
        "doctorants": Doctorant.objects.all(),
        "active_formation_tab": "doctoral",
    }
    return render(request, "lab/formations_doctoral.html", context)


def formations_jury(request):
    context = {
        "profile": LabProfile.load(),
        "activities": Activity.objects.filter(category=Activity.Category.JURY),
        "active_formation_tab": "jury",
    }
    return render(request, "lab/formations_jury.html", context)


def formations_stage(request):
    context = {
        "profile": LabProfile.load(),
        "activities": Activity.objects.filter(category=Activity.Category.STAGE),
        "active_formation_tab": "stage",
    }
    return render(request, "lab/formations_stage.html", context)


def formations_capacity(request):
    context = {
        "profile": LabProfile.load(),
        "activities": Activity.objects.filter(category=Activity.Category.CAPACITY),
        "active_formation_tab": "capacity",
    }
    return render(request, "lab/formations_capacity.html", context)
