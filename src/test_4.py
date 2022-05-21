import logging
import pdb
import time

import pytest
from src.inbox_page import InboxPage
from src.message_page import MessagePage
from src.compose_page import ComposePage


@pytest.mark.usefixtures("driver_init", "tests_init")
class TestInbox:

    def digits_len(self, s):
        return sum(list(map(lambda x: 1 if x.isdigit() else 0, s)))

    def letters_len(self, s):
        return sum(list(map(lambda x: 0 if x.isdigit() else 1, s)))

    def messages_test(self):
        inp = InboxPage(self.driver, self.locators, self.settings)
        mp = MessagePage(self.driver, self.locators, self.settings)
        cmp = ComposePage(self.driver, self.locators, self.settings)
        messages = inp.get_all_by_me()
        result_str = ""
        f_links = [m.get_attribute('href') for m in messages]
        assert len(f_links) == int(self.settings["messages_quantity"])
        for link in f_links:
            tb_tup = mp.get_topic_body(link)
            assert len(tb_tup) == 2
            topic = tb_tup[0]
            body = tb_tup[1]
            ltrs = self.letters_len(body)
            nums = self.digits_len(body)
            tmp_str = "Received mail on theme {} with message: {}. ".format(topic, body) + \
                      "It contains {} letters and {} numbers\n".format(ltrs, nums)
            result_str += tmp_str
        assert len(result_str) > 0
        marker_str = "Asferro Test Result"
        result_tpl = (marker_str, result_str)
        # go to compose
        cmp.go_to_compose_page()
        time.sleep(2)
        cmp.send_mail(result_tpl)
        messages_mid = inp.get_all_by_me()
        s_links = [m.get_attribute('href') for m in messages_mid]
        for link in s_links:
            mp.delete_if_not(link, marker_str)
        messages_end = inp.get_all_by_me()
        assert len(messages_end) == 1
