from .utils import *
from ..views import get_messages, clear_messages, get_answer

class ChatViewTest(Base):

    def test_post_redirect(self):
        http_response: HttpResponse = self.client.post(reverse('chat'))
        self.assertEqual(http_response.status_code, HTTPStatus.FOUND)
    
    def test_unimplemented_methods(self):
        http_response: HttpResponse = self.client.get(reverse('chat'))
        self.assertEqual(http_response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

class ChatMessagesTest(Base):
    def setUp(self):
        clear_messages()
        set_file_uploaded(True)
        self.client.post(reverse('chat'), {"chat_input": "Question0"})
        self.client.post(reverse('chat'), {"chat_input": "Question2"})
        self.client.post(reverse('chat'), {"chat_input": "Question4"})
        self.ref_answer = get_answer()

    def tearDown(self):
        set_file_uploaded(False)

    def test_chat_messages(self):
        self.assertNotEqual(get_messages(), [])
        for i, message in enumerate(get_messages()):
            if i % 2 == 0:
                self.assertEqual("question", message["type"])
                self.assertEqual("User: " + "Question" + str(i), message["content"])
            else:
                self.assertEqual("answer", message["type"])
                self.assertEqual("Chatbot: " + self.ref_answer, message["content"])

    def test_chat_ui(self):
        http_response: HttpResponse = self.client.get(reverse('home'))
        response = BeautifulSoup(http_response.content, "html.parser")
        div_elem: Optional[PageElement] = response.find("div", {"id": "chat_messages"})
        if isinstance(div_elem, Tag):
            contents = [div.get_text(strip=True) for div in response.select(".message_content")]
            self.assertNotEqual(contents, [])
            for i, message in enumerate(contents):
                if i % 2 == 0:
                    self.assertEqual("User: " + "Question" + str(i), message)
                else:
                    self.assertEqual("Chatbot: " + self.ref_answer, message)
        else:
            self.fail(f"div_elem not found")






