import json
import logging
import re
import unicodedata

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


def _assistant_profile_block():
    profile = LabProfile.load()
    lines = ["--- Profil du laboratoire ---"]
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
    return "\n".join(lines)


def _assistant_knowledge_items():
    """Construit la base de connaissances comme une liste d'éléments individuels
    (une équipe, un membre, une activité, une publication...) plutôt qu'un seul
    gros bloc de texte par catégorie. C'est ce qui permet à _select_relevant_knowledge
    de choisir précisément les éléments pertinents pour une question donnée, sans
    risquer de tronquer une catégorie entière (ex. les activités scientifiques,
    ~21 000 caractères à elles seules) au milieu de son contenu."""
    items = []

    for team in ResearchTeam.objects.prefetch_related("themes"):
        body_lines = [f"Équipe : {team.name} — {team.short_description or team.description}"]
        for theme in team.themes.all():
            body_lines.append(f"  Axe de recherche : {theme.title}")
        items.append(("Équipes de recherche et axes", team.name, "\n".join(body_lines)))

    for m in PermanentMember.objects.select_related("team"):
        details = [m.title]
        if m.is_director:
            details.append("Directeur du laboratoire")
        if m.role_tag:
            details.append(m.role_tag)
        if m.team:
            details.append(f"Équipe {m.team.name}")
        body = f"{m.full_name} — {', '.join(details)}"
        if m.bio:
            body += f"\n  {m.bio}"
        items.append(("Membres permanents", m.full_name, body))

    for d in Doctorant.objects.all():
        extra = f", co-encadrant : {d.co_supervisor}" if d.co_supervisor else ""
        body = (
            f"{d.full_name} — doctorant depuis {d.start_year}, université partenaire : "
            f"{d.partner_university}, directeur de thèse : {d.thesis_director}{extra}"
        )
        if d.bio:
            body += f"\n  {d.bio}"
        items.append(("Doctorants", d.full_name, body))

    for a in AssociateResearcher.objects.all():
        body = f"{a.full_name} — {a.grade}, {a.institution} ({a.country})"
        items.append(("Chercheurs associés (partenaires internationaux)", a.full_name, body))

    for act in Activity.objects.all():
        desc = f" — {act.description}" if act.description else ""
        title = f"{act.get_category_display()} : {act.title}"
        body = f"[{act.get_category_display()}] {act.title} ({act.year}){desc}"
        items.append(("Activités scientifiques (conférences, séminaires, olympiades, jurys...)", title, body))

    for c in MasterCourse.objects.all():
        body = f"{c.program} : {c.course_title} (enseignant : {c.instructor})"
        items.append(("Formations de Master", c.course_title, body))

    for p in Publication.objects.all():
        year = p.year or "à paraître"
        body = f"{p.authors} ({year}). {p.title}. {p.reference}"
        items.append(("Publications scientifiques", f"{p.title} {p.authors}", body))

    for p in ResearchProject.objects.all():
        body = f"{p.title} [{p.get_status_display()}] — financeur : {p.funder}, période : {p.period}"
        items.append(("Projets de recherche", p.title, body))

    for h in Habilitation.objects.all():
        body = f"{h.full_name} — {h.title} (garant : {h.garant})"
        items.append(("Habilitations à Diriger des Recherches (HDR)", h.full_name, body))

    for p in Partner.objects.all():
        body = f"{p.name} — {p.get_category_display()}, {p.country}"
        items.append(("Partenaires académiques et institutionnels", p.name, body))

    for n in News.objects.filter(is_published=True)[:10]:
        body = f"{n.date} : {n.title} — {n.excerpt}"
        items.append(("Actualités récentes", n.title, body))

    return items


ASSISTANT_STOPWORDS = {
    "les", "des", "une", "sont", "avec", "pour", "dans", "cette", "cet", "ces",
    "que", "qui", "quel", "quelle", "quels", "quelles", "est", "etes", "sur",
    "lamo", "laboratoire", "peux", "peut", "parle", "moi", "parlez", "vous", "vos",
    "ont", "ete", "etre", "avoir", "fait", "faite", "faites", "leur", "leurs",
    "tout", "tous", "toute", "toutes", "plus", "bien", "meme", "aussi", "ainsi",
    "notamment", "egalement", "depuis", "apres", "avant", "entre", "lors", "afin",
    "comme", "dont", "elle", "elles", "ses", "son", "sa", "nos", "notre", "and",
}


def _assistant_normalize(text, include_years=True):
    """Renvoie l'ensemble des mots (et années si demandé) significatifs, sans accents
    ni pluriel simple. Les années sont exclues du titre par défaut lors du scoring :
    beaucoup d'activités portent leur année dans leur nom (« ONM 2026 »...), ce qui
    fausserait le bonus de titre pour toute question mentionnant juste une année."""
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    words = re.findall(r"[a-z]{3,}", ascii_text.lower())
    stemmed = {w[:-1] if w.endswith("s") and len(w) > 4 else w for w in words}
    result = stemmed - ASSISTANT_STOPWORDS
    if include_years:
        result |= set(re.findall(r"\b(?:19|20)\d{2}\b", text))
    return result


def _select_relevant_knowledge(query_text, max_chars=15000):
    """Sélectionne les éléments de la base de connaissances les plus pertinents pour
    la question posée, pour rester sous la limite de tokens/minute du niveau gratuit
    de l'API utilisée (la base complète, ~38 000 caractères, dépasse cette limite à
    elle seule). Score par mots distincts (pas par fréquence brute) pour qu'un élément
    répétant des mots communs ne l'emporte pas sur un élément court mais ciblé ; les
    correspondances dans le titre de l'élément (nom, sujet...) comptent triple.
    Un élément qui ne tient pas entièrement dans le budget restant est ignoré plutôt
    que tronqué, pour ne jamais couper une fiche au milieu."""
    query_words = _assistant_normalize(query_text)

    scored = []
    for category, title, body in _assistant_knowledge_items():
        title_words = _assistant_normalize(title, include_years=False)
        score = 3 * len(query_words & title_words) + len(query_words & _assistant_normalize(body))
        scored.append((score, category, body))
    # Les équipes de recherche donnent un socle utile même pour les questions génériques.
    # À score égal, privilégie les éléments les plus courts : ça laisse de la place
    # pour plus d'éléments distincts au lieu de gaspiller le budget sur un seul gros
    # bloc (ex. une longue biographie de doctorant) qui a été pioché en premier par hasard.
    def _sort_key(item):
        score, category, body = item
        priority = 1000 if category == "Équipes de recherche et axes" else score
        return (-priority, len(body))

    scored.sort(key=_sort_key)

    grouped = {}
    order = []
    budget = max_chars - len(_assistant_profile_block())
    for score, category, body in scored:
        cost = len(body) + len(category) + 6
        if cost > budget:
            continue
        if category not in grouped:
            grouped[category] = []
            order.append(category)
        grouped[category].append(body)
        budget -= cost

    parts = [_assistant_profile_block()]
    for category in order:
        parts.append(f"\n--- {category} ---")
        parts.extend(grouped[category])

    return "\n".join(parts)


def _assistant_client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


@require_POST
def assistant_chat(request):
    """Endpoint JSON appelé par le widget de chat (lab/static/lab/js/main.js)."""
    if not settings.GROQ_API_KEY:
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

    conversation = []
    for turn in history:
        role = turn.get("role") if isinstance(turn, dict) else None
        text = (turn.get("text") or "").strip() if isinstance(turn, dict) else ""
        if role in ("user", "model") and text:
            conversation.append({
                "role": "user" if role == "user" else "assistant",
                "content": text[:ASSISTANT_MAX_MESSAGE_LENGTH],
            })
    conversation.append({"role": "user", "content": message})

    query_text = " ".join(turn["content"] for turn in conversation[-3:])
    knowledge_base = _select_relevant_knowledge(query_text)
    system_prompt = ASSISTANT_SYSTEM_PROMPT.format(knowledge_base=knowledge_base)
    messages = [{"role": "system", "content": system_prompt}] + conversation

    try:
        import requests

        api_response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-oss-120b",
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 700,
                "reasoning_effort": "low",
            },
            timeout=20,
        )
        api_response.raise_for_status()
        reply = (api_response.json()["choices"][0]["message"]["content"] or "").strip()
        if not reply:
            reply = "Désolé, je n'ai pas pu générer de réponse. Réessaie ou contacte le laboratoire."
    except Exception:
        logger.exception("Erreur lors de l'appel à l'assistant IA du LAMO")
        reply = (
            "Désolé, une erreur est survenue. Merci de réessayer dans un instant, ou de "
            "contacter le laboratoire directement via la page Contact."
        )

    return JsonResponse({"reply": reply})
