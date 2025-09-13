from .utils import *

class HomeViewTest(TestCase):
    def setUp(self) -> None:
        self.http_response: HttpResponse = self.client.get(reverse('home'))
        self.response = BeautifulSoup(self.http_response.content, "html.parser")
    
    def test_get_homepage(self):
        self.assertEqual(self.http_response.status_code, HTTPStatus.OK)
        #below code can be replaced by a one liner but I don't want a runtime error
        #if title is None and string is accessed. Also to get rid of pylance errors.
        title: Optional[Tag] = self.response.title
        if isinstance(title, Tag):
            self.assertEqual(TITLE, title.string)
        else:
            self.fail("title not found")

    def test_upload_pdf_form_exists(self) -> None:
        form_elem: Optional[PageElement] = self.response.find("form", {"id": IDS["pdf_upload_form"]})
        if isinstance(form_elem, Tag):
            self.assertEqual(form_elem.get("method"), "post")
            self.assertEqual(form_elem.get("enctype"), "multipart/form-data")
            self.assertEqual(form_elem.get("action"), reverse('upload'))
        else:
            self.fail(f"{IDS["pdf_upload_form"]} not found")

    def test_choose_file_button_exists(self):
        # input_elem is either a PageElement or None.
        input_elem: Optional[PageElement] = self.response.find("input", {"id": IDS["pdf_input"]})
        #A tag is a subclass of PageElement.
        if isinstance(input_elem, Tag):
            self.assertEqual(input_elem.get("type"), "file")
            self.assertEqual(input_elem.get("name"), IDS["pdf_input"])
            self.assertEqual(input_elem.get("accept"), ".pdf")
            self.assertIn("required", input_elem.attrs)
        else:
            self.fail(f"{IDS["pdf_input"]} not found")
    
    def test_upload_pdf_button_exists(self):
        upload_btn: Optional[PageElement] = self.response.find("button", {"id": IDS["upload_pdf_btn"]})
        if isinstance(upload_btn, Tag):
            self.assertEqual(upload_btn.get("type"), "submit")
            self.assertEqual(upload_btn.string, "Upload PDF")
        else:
            self.fail(f"{IDS["upload_pdf_btn"]} not found")
