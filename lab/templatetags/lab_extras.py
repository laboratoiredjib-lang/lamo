import re

from django import template

register = template.Library()

HONORIFIC_RE = re.compile(r"^(dr|mme|mlle|m|pr|professeur|professeure|prof)\.?\s+", re.IGNORECASE)


@register.filter
def initials(full_name):
    """Return up to two initials from a name, skipping leading honorifics (Dr., M., Mme., ...)."""
    if not full_name:
        return ""
    name = HONORIFIC_RE.sub("", full_name.strip())
    words = [w for w in name.split() if w]
    letters = "".join(w[0] for w in words[:2])
    return letters.upper() if letters else full_name[0].upper()
