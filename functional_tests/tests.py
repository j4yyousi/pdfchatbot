"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class TestUploadPdf(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        pass
        self.browser.quit()
    
    def test_upload_pdf(self) -> None:
        #self.browser.get(self.live_server_url)
        #user visits home page
        #self.assertIn("PDF Q/A Chatbot", self.browser.title)
        #user finds choose button
"""