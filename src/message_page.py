import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from src.base import CommonPage
import logging
import pdb


class MessagePage(CommonPage):

    def __init__(self, driver, locators, settings):
        super().__init__(driver, locators, settings)
        self.driver = driver
        self.locators = locators
        self.settings = settings

    def _go_to_message(self, link):
        self.driver.get(link)

    def _get_topic(self):
        pass

    def _get_body(self):
        pass

    def get_topic_body(self, link):
        self._go_to_message(link)
        topic = self._get_topic()
        body = self._get_body()
        return tuple(topic, body)