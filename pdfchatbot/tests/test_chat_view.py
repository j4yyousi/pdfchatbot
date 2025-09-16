from .utils import *
from ..views import get_messages, clear_messages, chatbot_answer

class ChatViewTest(Base):
    def test_post_redirect(self):
        http_response: HttpResponse = self.client.post(reverse('chat'))
        self.assertEqual(http_response.status_code, HTTPStatus.FOUND)
    
    def test_unimplemented_methods(self):
        http_response: HttpResponse = self.client.get(reverse('chat'))
        self.assertEqual(http_response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

@mock.patch("pdfchatbot.views.chatbot_is_file_uploaded", return_value=True)
class ChatMessagesTest(Base):
    def setUp(self):
        clear_messages()
        self.client.post(reverse('chat'), {"chat_input": "Question0"})
        self.client.post(reverse('chat'), {"chat_input": "Question2"})
        self.client.post(reverse('chat'), {"chat_input": "Question4"})
        self.ref_answer = chatbot_answer("")

    def test_chat_messages(self, cifu):
        self.assertNotEqual(get_messages(), [])
        for i, message in enumerate(get_messages()):
            if i % 2 == 0:
                self.assertEqual("question", message["type"])
                self.assertEqual("User: " + "Question" + str(i), message["content"])
            else:
                self.assertEqual("answer", message["type"])
                self.assertEqual("Chatbot: " + self.ref_answer, message["content"])

    def test_chat_ui(self, cifu):
        http_response: HttpResponse = self.client.get(reverse('home'))
        response = BeautifulSoup(http_response.content, "html.parser")
        div_elem: Optional[PageElement] = response.find("div", {"id": "chat_messages"})
        if isinstance(div_elem, Tag):
            contents = [div.get_text(strip=True) for div in response.select(".check_message_content")]
            self.assertNotEqual(contents, [])
            for i, message in enumerate(contents):
                if i % 2 == 0:
                    self.assertEqual("User: " + "Question" + str(i), message)
                else:
                    self.assertEqual("Chatbot: " + self.ref_answer, message)
        else:
            self.fail(f"div_elem not found")






