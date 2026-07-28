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
SEPARATOR_TAIL_RE = re.compile(r"[\s—–-]+$")


@register.filter
def field_labels(text):
    """Comme linebreaks, mais met en valeur (gras, couleur) les libellés de champ connus
    ("École doctorale :", "Titre de la thèse :", ...) rencontrés dans un texte libre (jurys de
    thèse), chacun démarrant sa propre ligne même si plusieurs libellés partagent un paragraphe."""
    if not text:
        return ""
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    out_paragraphs = []
    for para in paragraphs:
        pieces = []
        last_end = 0
        first = True
        for m in FIELD_LABEL_RE.finditer(para):
            before = escape(para[last_end:m.start()])
            if first:
                pieces.append(before)
            else:
                pieces.append(SEPARATOR_TAIL_RE.sub("", before))
                pieces.append("<br>")
            pieces.append(f'<strong class="field-label">{escape(m.group(1))} :</strong> ')
            last_end = m.end()
            first = False
        pieces.append(escape(para[last_end:]))
        out_paragraphs.append("".join(pieces).replace("\n", "<br>"))
    html = "".join("<p>" + p + "</p>" for p in out_paragraphs)
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
