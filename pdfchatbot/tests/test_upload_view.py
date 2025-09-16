from .utils import *
from django.core.files.uploadedfile import InMemoryUploadedFile

class UploadViewTest(Base):
    def test_upload_post_redirect(self):
        http_response: HttpResponse = self.client.post(reverse('upload'))
        self.assertEqual(http_response.status_code, HTTPStatus.FOUND)
    
    def test_unimplemented_methods(self):
        http_response: HttpResponse = self.client.get(reverse('upload'))
        self.assertEqual(http_response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    @mock.patch("pdfchatbot.views.chatbot_process_pdf")
    def test_upload_pdf(self, mock_process_pdf: mock.MagicMock):
        self.upload_pdf()
        self.assertEqual(mock_process_pdf.called, True)
        args, _ = mock_process_pdf.call_args
        post_file: InMemoryUploadedFile = args[0]
        self.assertEqual(self.ref_file.name, post_file.name)
        self.assertEqual(self.ref_file.size, post_file.size)

    @mock.patch("pdfchatbot.views.chatbot_is_file_uploaded", return_value=True)
    def test_chat_form_exists_after_file_upload(self, cifu):
        self.upload_pdf()
        self.http_response = self.client.get(reverse('home'))
        response = BeautifulSoup(self.http_response.content, "html.parser")
        form_elem: Optional[PageElement] = response.find("form", {"id": "chat_form"})
        if isinstance(form_elem, Tag):
            self.assertEqual(form_elem.get("method"), "post")
            self.assertEqual(form_elem.get("action"), reverse('chat'))
        else:
            self.fail(f"chat_form not found")

    @mock.patch("pdfchatbot.views.chatbot_is_file_uploaded", return_value=True)
    def test_file_name_exists_after_file_upload(self, cifu):
        self.upload_pdf()
        self.http_response = self.client.get(reverse('home'))
        response = BeautifulSoup(self.http_response.content, "html.parser")
        div_elem: Optional[PageElement] = response.find("div", {"id": "file_name"})
        if isinstance(div_elem, Tag):
            self.assertEqual(div_elem.get_text(), "Uploaded " + self.ref_file.name)
        else:
            self.fail(f"div_elem not found")

    @mock.patch("pdfchatbot.views.chatbot_is_file_uploaded", return_value=True)
    def test_chat_input_exists_after_file_upload(self, cifu):
        self.upload_pdf()
        self.http_response = self.client.get(reverse('home'))
        response = BeautifulSoup(self.http_response.content, "html.parser")
        input_elem: Optional[PageElement] = response.find("input", {"id": "chat_input"})
        if isinstance(input_elem, Tag):
            self.assertEqual(input_elem.get("type"), "text")
            self.assertEqual(input_elem.get("name"), "chat_input")
            self.assertEqual(input_elem.get("placeholder"), "Ask a question about the document...")
            self.assertIn("required", input_elem.attrs)
        else:
            self.fail(f"chat_input not found")

    @mock.patch("pdfchatbot.views.chatbot_is_file_uploaded", return_value=True)
    def test_chat_question_submit_btn_exists_after_file_upload(self, cifu):
        self.upload_pdf()
        self.http_response = self.client.get(reverse('home'))
        response = BeautifulSoup(self.http_response.content, "html.parser")
        chat_btn: Optional[PageElement] = response.find("button", {"id": "chat_btn"})
        if isinstance(chat_btn, Tag):
            self.assertEqual(chat_btn.get("type"), "submit")
            self.assertEqual(chat_btn.string, "Send")
        else:
            self.fail(f"{"chat_btn"} not found")