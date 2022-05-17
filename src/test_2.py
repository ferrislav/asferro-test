import pytest
import logging
# fixture to get all mails and return map of them


@pytest.mark.usefixtures("driver_init")
class TestReceive:
    def some_test(self):
        logging.log(logging.INFO, f"driver: {self.driver}")
