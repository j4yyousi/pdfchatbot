from django.test import TestCase
from django.http import HttpResponse
from bs4 import BeautifulSoup, Tag
from bs4.element import PageElement
from typing import Optional
OK = 200

class HomeViewTest(TestCase):
    def setUp(self) -> None:
        pass
    
    def test_get_homepage(self):
        http_response: HttpResponse = self.client.get("/")
        self.assertEqual(http_response.status_code, OK)
        response = BeautifulSoup(http_response.content, "html.parser")
        #below code can be replaced by a one liner but I don't want a runtime error
        #if title is None and string is accessed. Also to get rid of pylance errors.
        title: Optional[Tag] = response.title
        if isinstance(title, Tag):
            self.assertEqual("PDF Q&A Chatbot", title.string)
        else:
            self.fail("title not found")

    def test_upload_pdf_button_exists(self):
        http_response: HttpResponse = self.client.get("/")
        response = BeautifulSoup(http_response.content, "html.parser")
        # input_elem is either a PageElement or None
        input_elem: Optional[PageElement] = response.find("input", {"id": "pdf-file"})
        self.assertIsNotNone(input_elem)
        if isinstance(input_elem, Tag):
            self.assertEqual(input_elem.get("type"), "file")
            self.assertEqual(input_elem.get("name"), "pdf_file")
            self.assertEqual(input_elem.get("accept"), ".pdf")
            self.assertIn("required", input_elem.attrs)
        else:
            self.fail("input_elem not found")