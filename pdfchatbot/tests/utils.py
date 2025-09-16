from django.test import TestCase
from django.http import HttpResponse
from bs4 import BeautifulSoup, Tag
from bs4.element import PageElement
from typing import Optional
from django.urls import reverse
from http import HTTPStatus
from unittest import mock
from django.core.files.uploadedfile import SimpleUploadedFile
from fpdf import FPDF
from io import BytesIO

def create_test_pdf() -> SimpleUploadedFile:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="This is a test PDF", ln=True, align="C")
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO(pdf_bytes)
    return SimpleUploadedFile(
        name="test.pdf",
        content=buffer.getvalue(),
        content_type="application/pdf"
    )

class Base(TestCase):

    def upload_pdf(self):
        self.ref_file: SimpleUploadedFile = create_test_pdf()
        self.http_response: HttpResponse = self.client.post(
            reverse('upload'),
            {"pdf_input": self.ref_file}
        )