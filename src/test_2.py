import time

import pytest
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pdb


@pytest.mark.usefixtures("driver_init")
class TestReceive:

    # For the sake of simplicity would continue from where I'm in drive nav.
    # Should be in account mailbox.

    # click on inbox button.
    # will need to have values in several tests in this class
    msg_values = dict()
    # def __init__(self):
    #     self.msg_values = dict()


    def count_test(self, locators):
        assert EC.url_contains(locators["mail_home_partial_url"])
        wait = WebDriverWait(self.driver, 90)

        inbox_btn = self.driver.find_element(By.CSS_SELECTOR, locators["inbox_btn"])
        inbox_btn.click()
        # it works as it is. Run a few times may need sleeps loops and refresh trick
        # sometimes messages are 'stuck', must loop here and wait until all messages are
        # delivered. I know that it's a cheat, since I do know that I shall get exactly 10
        # messages, but.. In real life I would put for loop and gave to it reasonable amount of time.
        loop = True
        while loop:
            wait.until(EC.presence_of_element_located((By.XPATH, locators["message_list_container_path"])))
            # All messages no check for sender.
            messages = self.driver.find_elements(By.CLASS_NAME, locators["message_list_item_class"])
            if len(messages) < 10:
                time.sleep(2)
            else:
                loop = False
        # pdb.set_trace()
        assert len(messages) == 10


    # Collect data to map
    # Parse map as required get topic, body, count letters and digits

    def some_test(self):
        # logging.log(logging.INFO, f"driver: {self.driver}")
        assert len(TestReceive.msg_values) == 0
