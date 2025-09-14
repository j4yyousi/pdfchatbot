from .utils import *
from django.core.files.uploadedfile import SimpleUploadedFile
from fpdf import FPDF
from io import BytesIO
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
    def upload_pdf(self):
        self.ref_file: SimpleUploadedFile = create_test_pdf()
        self.http_response: HttpResponse = self.client.post(
            reverse('upload'),
            {IDS["pdf_input"]: self.ref_file}
        )

    def test_upload_post_redirect(self):
        http_response: HttpResponse = self.client.post(reverse('upload'))
        self.assertEqual(http_response.status_code, HTTPStatus.FOUND)
    
    def test_unimplemented_methods(self):
        http_response: HttpResponse = self.client.get(reverse('upload'))
        self.assertEqual(http_response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    #mock functions where they are used, not where they are defined.
    @mock.patch("pdfchatbot.views.process_pdf")
    def test_upload_pdf(self, mock_process_pdf: mock.MagicMock):
        self.upload_pdf()
        self.assertEqual(mock_process_pdf.called, True)
        args, _ = mock_process_pdf.call_args
        post_file: InMemoryUploadedFile = args[0]
        self.assertEqual(self.ref_file.name, post_file.name)
        self.assertEqual(self.ref_file.size, post_file.size)

    def test_chat_form_exists_after_file_upload(self):
        self.upload_pdf()
        self.http_response = self.client.get(reverse('home'))
        response = BeautifulSoup(self.http_response.content, "html.parser")
        form_elem: Optional[PageElement] = response.find("form", {"id": IDS["chat_form"]})
        if isinstance(form_elem, Tag):
            self.assertEqual(form_elem.get("method"), "post")
            self.assertEqual(form_elem.get("action"), reverse('chat'))
        else:
            self.fail(f"{IDS["chat_form"]} not found")

    def test_chat_input_exists_after_file_upload(self):
        self.upload_pdf()
        self.http_response = self.client.get(reverse('home'))
        response = BeautifulSoup(self.http_response.content, "html.parser")
        input_elem: Optional[PageElement] = response.find("input", {"id": IDS["chat_input"]})
        if isinstance(input_elem, Tag):
            self.assertEqual(input_elem.get("type"), "text")
            self.assertEqual(input_elem.get("placeholder"), "Ask a question about the document...")
            self.assertIn("required", input_elem.attrs)
        else:
            self.fail(f"{IDS["chat_input"]} not found")

    def test_chat_question_submit_btn_exists_after_file_upload(self):
        self.upload_pdf()
        self.http_response = self.client.get(reverse('home'))
        response = BeautifulSoup(self.http_response.content, "html.parser")
        chat_btn: Optional[PageElement] = response.find("button", {"id": IDS["chat_btn"]})
        if isinstance(chat_btn, Tag):
            self.assertEqual(chat_btn.get("type"), "submit")
            self.assertEqual(chat_btn.string, "Send")
        else:
            self.fail(f"{IDS["chat_btn"]} not found")