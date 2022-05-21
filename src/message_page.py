from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.base import CommonPage


class MessagePage(CommonPage):

    def __init__(self, driver, locators, settings):
        super().__init__(driver, locators, settings)
        self.driver = driver
        self.locators = locators
        self.settings = settings

    def _go_to_message(self, link):
        self.driver.get(link)

    def get_topic(self):
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.visibility_of_element_located((By.XPATH, self.locators["message_topic"])))
        return self.driver.find_element(By.XPATH, self.locators["message_topic"]).text

    def get_topic_body(self, link):
        self._go_to_message(link)
        wait = WebDriverWait(self.driver, 5)
        topic = self.get_topic()
        wait.until(EC.visibility_of_element_located((By.XPATH, self.locators["message_body_path"])))
        body = self.driver.find_element(By.XPATH, self.locators["message_body_path"]).text
        return topic, body



    def delete_if_not(self, link, filter_str):
        self._go_to_message(link)
        topic = self.get_topic()
        WebDriverWait(self.driver, 10)\
            .until(EC.visibility_of_element_located((By.XPATH, self.locators["message_delete_btn"])))
        delete_btn = self.driver.find_element(By.XPATH, self.locators["message_delete_btn"])
        if not topic.__eq__(filter_str):
            delete_btn.click()
