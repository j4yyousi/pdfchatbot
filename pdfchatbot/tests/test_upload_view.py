from .utils import *
from django.core.files.uploadedfile import SimpleUploadedFile
from fpdf import FPDF
from io import BytesIO

def create_test_pdf() -> SimpleUploadedFile:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, text="This is a test PDF", ln=True, align="C")
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO(pdf_bytes)
    return SimpleUploadedFile(
        name="test.pdf",
        content=buffer.getvalue(),
        content_type="application/pdf"
    )

class UploadViewTest(TestCase):
    def test_upload_post_redirect(self):
        #test_file: SimpleUploadedFile = create_test_pdf()
        #http_response: HttpResponse = self.client.post(reverse('upload'), {IDS["pdf_input"]: test_file})
        http_response: HttpResponse = self.client.post(reverse('upload'))
        self.assertEqual(http_response.status_code, HTTPStatus.FOUND)
    
    def test_unimplemented_methods(self):
        http_response: HttpResponse = self.client.get(reverse('upload'))
        self.assertEqual(http_response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

