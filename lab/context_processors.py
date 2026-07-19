from .models import LabProfile, Partner, ResearchTeam


def lab_profile(request):
    return {
        "site_profile": LabProfile.load(),
        "footer_partners": Partner.objects.all()[:12],
        "nav_teams": ResearchTeam.objects.all(),
    }
