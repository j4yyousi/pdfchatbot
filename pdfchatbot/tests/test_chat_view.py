from .utils import *

class ChatViewTest(TestCase):
    def test_post_redirect(self):
        http_response: HttpResponse = self.client.post(reverse('chat'))
        self.assertEqual(http_response.status_code, HTTPStatus.FOUND)
    
    def test_unimplemented_methods(self):
        http_response: HttpResponse = self.client.get(reverse('chat'))
        self.assertEqual(http_response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
