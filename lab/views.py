from django.shortcuts import get_object_or_404, render

from .models import (
    AssociateResearcher,
    Doctorant,
    LabProfile,
    News,
    Partner,
    PermanentMember,
    ResearchTeam,
    ResearchTheme,
)


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
        "teams": ResearchTeam.objects.all(),
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


def themes(request):
    context = {
        "profile": LabProfile.load(),
        "themes": ResearchTheme.objects.select_related("team").all(),
    }
    return render(request, "lab/themes.html", context)


def members_permanent(request):
    context = {
        "profile": LabProfile.load(),
        "members": PermanentMember.objects.select_related("team").all(),
        "active_tab": "permanents",
    }
    return render(request, "lab/members_permanent.html", context)


def members_doctorants(request):
    context = {
        "profile": LabProfile.load(),
        "doctorants": Doctorant.objects.all(),
        "active_tab": "doctorants",
    }
    return render(request, "lab/members_doctorants.html", context)


def members_associates(request):
    context = {
        "profile": LabProfile.load(),
        "associates": AssociateResearcher.objects.all(),
        "active_tab": "associes",
    }
    return render(request, "lab/members_associates.html", context)


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
