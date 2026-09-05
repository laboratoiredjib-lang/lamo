import json
import logging

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

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


logger = logging.getLogger(__name__)

ASSISTANT_MAX_MESSAGE_LENGTH = 500
ASSISTANT_MAX_HISTORY_TURNS = 8
ASSISTANT_RATE_LIMIT_PER_HOUR = 30

ASSISTANT_SYSTEM_PROMPT = """Tu es l'assistant virtuel officiel du site web du LAMO (Laboratoire \
d'Analyse, de Modélisation et d'Optimisation), une unité de recherche du Centre de Recherche en \
Mathématiques et Numérique de l'Université de Djibouti.

Ton rôle : aider les visiteurs du site à trouver des informations sur le laboratoire, ses équipes, \
ses membres, ses activités, ses formations, ses publications et ses partenaires, et à s'orienter sur \
le site. Réponds toujours en français, de façon concise, chaleureuse et professionnelle.

Règles importantes :
- Base tes réponses UNIQUEMENT sur les informations fournies ci-dessous. N'invente jamais de noms, \
de dates, de chiffres ou de coordonnées qui n'y figurent pas.
- Si l'information demandée n'est pas dans ces données, dis-le honnêtement et propose de contacter \
le laboratoire directement (voir l'email dans le profil ci-dessous) plutôt que d'inventer une réponse.
- Ne réponds qu'aux questions en lien avec le LAMO, l'Université de Djibouti, les mathématiques \
appliquées ou l'orientation sur ce site. Pour toute autre question, redirige poliment vers ce périmètre.
- Reste bref : 2 à 5 phrases maximum, sauf si on te demande explicitement une liste détaillée.
- N'utilise pas de formatage Markdown (pas d'astérisques, pas de titres) : du texte simple, avec des \
tirets "-" pour les listes si besoin.

=== Données du site (source unique de vérité) ===
{knowledge_base}
"""


def _build_assistant_knowledge_base():
    profile = LabProfile.load()
    lines = []

    lines.append("--- Profil du laboratoire ---")
    lines.append(f"Nom complet : {profile.name} ({profile.acronym})")
    if profile.affiliation:
        lines.append(f"Affiliation : {profile.affiliation}")
    if profile.director_name:
        lines.append(f"Directeur : {profile.director_name}")
    if profile.address:
        lines.append(f"Adresse : {profile.address}")
    if profile.email_primary:
        lines.append(f"Email de contact : {profile.email_primary}")
    if profile.phone:
        lines.append(f"Téléphone : {profile.phone}")
    if profile.mission:
        lines.append(f"Mission : {profile.mission}")
    if profile.presentation_extra:
        lines.append(profile.presentation_extra)

    lines.append("\n--- Équipes de recherche et axes ---")
    for team in ResearchTeam.objects.prefetch_related("themes"):
        lines.append(f"Équipe : {team.name} — {team.short_description or team.description}")
        for theme in team.themes.all():
            lines.append(f"  Axe de recherche : {theme.title}")

    lines.append("\n--- Membres permanents ---")
    for m in PermanentMember.objects.select_related("team"):
        details = [m.title]
        if m.is_director:
            details.append("Directeur du laboratoire")
        if m.role_tag:
            details.append(m.role_tag)
        if m.team:
            details.append(f"Équipe {m.team.name}")
        lines.append(f"{m.full_name} — {', '.join(details)}")
        if m.bio:
            lines.append(f"  {m.bio}")

    lines.append("\n--- Doctorants ---")
    for d in Doctorant.objects.all():
        extra = f", co-encadrant : {d.co_supervisor}" if d.co_supervisor else ""
        lines.append(
            f"{d.full_name} — doctorant depuis {d.start_year}, université partenaire : "
            f"{d.partner_university}, directeur de thèse : {d.thesis_director}{extra}"
        )

    lines.append("\n--- Chercheurs associés (partenaires internationaux) ---")
    for a in AssociateResearcher.objects.all():
        lines.append(f"{a.full_name} — {a.grade}, {a.institution} ({a.country})")

    lines.append("\n--- Activités scientifiques (conférences, séminaires, olympiades, jurys...) ---")
    for act in Activity.objects.all():
        desc = f" — {act.description}" if act.description else ""
        lines.append(f"[{act.get_category_display()}] {act.title} ({act.year}){desc}")

    lines.append("\n--- Formations de Master ---")
    for c in MasterCourse.objects.all():
        lines.append(f"{c.program} : {c.course_title} (enseignant : {c.instructor})")

    lines.append("\n--- Publications scientifiques ---")
    for p in Publication.objects.all():
        year = p.year or "à paraître"
        lines.append(f"{p.authors} ({year}). {p.title}. {p.reference}")

    lines.append("\n--- Projets de recherche ---")
    for p in ResearchProject.objects.all():
        lines.append(
            f"{p.title} [{p.get_status_display()}] — financeur : {p.funder}, période : {p.period}"
        )

    lines.append("\n--- Habilitations à Diriger des Recherches (HDR) ---")
    for h in Habilitation.objects.all():
        lines.append(f"{h.full_name} — {h.title} (garant : {h.garant})")

    lines.append("\n--- Partenaires académiques et institutionnels ---")
    for p in Partner.objects.all():
        lines.append(f"{p.name} — {p.get_category_display()}, {p.country}")

    lines.append("\n--- Actualités récentes ---")
    for n in News.objects.filter(is_published=True)[:10]:
        lines.append(f"{n.date} : {n.title} — {n.excerpt}")

    return "\n".join(lines)


def _assistant_client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


@require_POST
def assistant_chat(request):
    """Endpoint JSON appelé par le widget de chat (lab/static/lab/js/main.js)."""
    if not settings.GEMINI_API_KEY:
        return JsonResponse(
            {
                "reply": (
                    "L'assistant n'est pas encore configuré. Merci de contacter le "
                    "laboratoire directement via la page Contact."
                )
            }
        )

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"error": "Requête invalide."}, status=400)

    message = (payload.get("message") or "").strip()
    if not message:
        return JsonResponse({"error": "Message vide."}, status=400)
    if len(message) > ASSISTANT_MAX_MESSAGE_LENGTH:
        return JsonResponse({"error": "Message trop long."}, status=400)

    history = payload.get("history")
    if not isinstance(history, list):
        history = []
    history = history[-ASSISTANT_MAX_HISTORY_TURNS:]

    cache_key = f"assistant-rate:{_assistant_client_ip(request)}"
    count = cache.get(cache_key, 0)
    if count >= ASSISTANT_RATE_LIMIT_PER_HOUR:
        return JsonResponse(
            {
                "reply": (
                    "Tu as posé beaucoup de questions récemment. Merci de patienter un peu "
                    "avant de continuer, ou de contacter directement le laboratoire."
                )
            }
        )
    cache.set(cache_key, count + 1, timeout=3600)

    contents = []
    for turn in history:
        role = turn.get("role") if isinstance(turn, dict) else None
        text = (turn.get("text") or "").strip() if isinstance(turn, dict) else ""
        if role in ("user", "model") and text:
            contents.append({"role": role, "parts": [{"text": text[:ASSISTANT_MAX_MESSAGE_LENGTH]}]})
    contents.append({"role": "user", "parts": [{"text": message}]})

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        system_prompt = ASSISTANT_SYSTEM_PROMPT.format(
            knowledge_base=_build_assistant_knowledge_base()
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.3,
                max_output_tokens=500,
            ),
        )
        reply = (response.text or "").strip()
        if not reply:
            reply = "Désolé, je n'ai pas pu générer de réponse. Réessaie ou contacte le laboratoire."
    except Exception:
        logger.exception("Erreur lors de l'appel à l'assistant IA du LAMO")
        reply = (
            "Désolé, une erreur est survenue. Merci de réessayer dans un instant, ou de "
            "contacter le laboratoire directement via la page Contact."
        )

    return JsonResponse({"reply": reply})
