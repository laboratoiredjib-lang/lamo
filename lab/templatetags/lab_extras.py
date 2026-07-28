import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

HONORIFIC_RE = re.compile(r"^(dr|mme|mlle|m|pr|professeur|professeure|prof)\.?\s+", re.IGNORECASE)

FIELD_LABELS = [
    "École doctorale", "Laboratoire", "Spécialité", "Discipline",
    "Titre de la thèse", "Directeur de thèse", "Directrice de thèse",
    "Co-directeurs", "Co-directeur", "Co-encadrant", "Co-encadrement",
    "Examinateur", "Invité", "Président du jury", "Rapporteurs",
    "Date de soutenance", "Lieu", "Doctorant",
]
FIELD_LABEL_RE = re.compile(
    r"(?<![\wÀ-ÿ])(" + "|".join(re.escape(l) for l in sorted(FIELD_LABELS, key=len, reverse=True)) + r")\s*:\s*"
)


@register.filter
def field_labels(text):
    """Comme linebreaks, mais met en valeur (gras, couleur) les libellés de champ connus
    ("École doctorale :", "Titre de la thèse :", ...) rencontrés dans un texte libre (jurys de thèse)."""
    if not text:
        return ""
    highlighted = FIELD_LABEL_RE.sub(r'<strong class="field-label">\1 :</strong> ', escape(text))
    paragraphs = [p for p in highlighted.split("\n\n") if p.strip()]
    html = "".join("<p>" + p.replace("\n", "<br>") + "</p>" for p in paragraphs)
    return mark_safe(html)


@register.filter
def initials(full_name):
    """Return up to two initials from a name, skipping leading honorifics (Dr., M., Mme., ...)."""
    if not full_name:
        return ""
    name = HONORIFIC_RE.sub("", full_name.strip())
    words = [w for w in name.split() if w]
    letters = "".join(w[0] for w in words[:2])
    return letters.upper() if letters else full_name[0].upper()
