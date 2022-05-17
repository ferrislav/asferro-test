import os
from selenium import webdriver
import pytest


def should_drop(s):
    return s.startswith("#", 0) or len(s) == 0


@pytest.fixture(scope="package")
def locators(pytestconfig):
    res = {}
    curr_path = pytestconfig.invocation_params.dir.cwd()
    file_path = os.path.join(curr_path, "locators")
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            b = should_drop(line)
            if not b:
                st_list = line.split("=")
                if len(st_list) == 2:
                    res[st_list[0].strip()] = st_list[1].strip()
    assert len(res) > 0
    return res


@pytest.fixture(scope="session")
def driver_init(request):
    web_driver = webdriver.Firefox()
    session = request.node
    for item in session.items:
        cls = item.getparent(pytest.Class)
        setattr(cls.obj, "driver", web_driver)
    yield
    web_driver.close()

