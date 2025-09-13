from .utils import *
from django.core.files.uploadedfile import SimpleUploadedFile
from fpdf import FPDF
from io import BytesIO
#import pdfchatbot.processpdf
from unittest import mock
from django.core.files.uploadedfile import UploadedFile, InMemoryUploadedFile

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

class UploadViewTest(TestCase):
    def test_upload_post_redirect(self):
        http_response: HttpResponse = self.client.post(reverse('upload'))
        self.assertEqual(http_response.status_code, HTTPStatus.FOUND)
    
    def test_unimplemented_methods(self):
        http_response: HttpResponse = self.client.get(reverse('upload'))
        self.assertEqual(http_response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    #mock functions where they are used, not where they are defined.
    @mock.patch("pdfchatbot.views.process_pdf")
    def test_upload_pdf(self, mock_process_pdf: mock.MagicMock):
        ref_file: SimpleUploadedFile = create_test_pdf()
        self.client.post(reverse('upload'), {IDS["pdf_input"]: ref_file})
        self.assertEqual(mock_process_pdf.called, True)
        args, _ = mock_process_pdf.call_args
        post_file: InMemoryUploadedFile = args[0]
        self.assertEqual(ref_file.name, post_file.name)
        self.assertEqual(ref_file.size, post_file.size)
