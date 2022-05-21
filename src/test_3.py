import pytest
from selenium.webdriver.support import expected_conditions as EC

from src.compose_page import ComposePage
from src.inbox_page import InboxPage


@pytest.mark.usefixtures("driver_init", "tests_init")
class TestCompose:
    pass

    def delete_messages_test(self):
        assert EC.url_contains(self.locators["inbox_partial_url"])
        ip = InboxPage(self.driver, self.locators, self.settings)
        messages = ip.get_all_by_me()
        if len(messages) > 0:
            ip.delete_all()

        messages = ip.get_all_by_me()
        assert len(messages) == 0

    def count_test(self):
        mess_quant = int(self.settings["messages_quantity"])
        cp = ComposePage(self.driver, self.locators, self.settings)
        inp = InboxPage(self.driver, self.locators, self.settings)
        cp.send()

        if not inp.is_inbox_empty():
            if inp.all_messages_arrived():
                messages = inp.get_all_by_me()
                assert len(messages) == mess_quant
        else:
            pytest.fail(f"{mess_quant} messages didn't arrive to inbox.")
