from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import (
    Activity,
    AssociateResearcher,
    Doctorant,
    Habilitation,
    LabProfile,
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
        "academic_partners": Partner.objects.filter(category=Partner.Category.ACADEMIC),
        "institutional_partners": Partner.objects.filter(category=Partner.Category.INSTITUTIONAL),
    }
    return render(request, "lab/partners.html", context)


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
        "conferences": activities_qs.filter(category=Activity.Category.CONFERENCE),
        "seminaires": activities_qs.filter(category=Activity.Category.SEMINAIRE),
        "olympiades": activities_qs.filter(category=Activity.Category.OLYMPIADES),
        "offres": activities_qs.filter(category=Activity.Category.OFFRE),
    }
    return render(request, "lab/activities.html", context)


def production(request):
    context = {
        "profile": LabProfile.load(),
        "doctorants": Doctorant.objects.all(),
        "doctorants_count": Doctorant.objects.count(),
        "publications": Publication.objects.all(),
        "projects": ResearchProject.objects.prefetch_related("related_publications"),
        "habilitations": Habilitation.objects.all(),
    }
    return render(request, "lab/production.html", context)


def formations(request):
    context = {
        "profile": LabProfile.load(),
        "doctorants_count": Doctorant.objects.count(),
    }
    return render(request, "lab/formations.html", context)
