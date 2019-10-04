# Vue pour la redirection des traduction sur la meme page

from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
import re


def strip_language(path):
    pattern = _('/(%s)/') % get_language()
    match = re.search(pattern, path)
    if match is None:
        return path
    return path[match.end(1):]
