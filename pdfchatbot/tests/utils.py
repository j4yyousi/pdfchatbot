from django.test import TestCase
from django.http import HttpResponse
from bs4 import BeautifulSoup, Tag
from bs4.element import PageElement
from typing import Optional
from django.urls import reverse
from ..constants import IDS, TITLE
from http import HTTPStatus