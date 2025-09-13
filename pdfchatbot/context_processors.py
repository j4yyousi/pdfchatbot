from .constants import IDS
from django.http import HttpRequest
def element_ids(request: HttpRequest) -> dict[str, dict[str, str]]:
    """
    used in settings.py to use id names from IDS
    """
    return {"ids": IDS}