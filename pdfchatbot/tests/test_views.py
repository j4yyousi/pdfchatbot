from django.test import TestCase
from django.http import HttpResponse
from bs4 import BeautifulSoup

OK = 200

class HomeViewTest(TestCase):
    def test_get_homepage(self) -> None:
        http_response: HttpResponse = self.client.get("/")
        self.assertEqual(http_response.status_code, OK)
        response = BeautifulSoup(http_response.content, "html.parser")
        self.assertIn("PDF Q/A Chatbot", response.title.string)