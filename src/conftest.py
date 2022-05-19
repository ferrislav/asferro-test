import os
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.service import Service
import pytest


def should_drop(s):
    return s.startswith("#", 0) or len(s) == 0


@pytest.fixture(scope='session')
def locators(pytestconfig):
    res = {}
    curr_path = pytestconfig.invocation_params.dir.cwd()
    file_path = os.path.join(curr_path, "locators")
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            b = should_drop(line)
            if not b:
                st_list = line.split("=", 1)
                if len(st_list) == 2:
                    res[st_list[0].strip()] = st_list[1].strip()
    assert len(res) > 0
    return res


@pytest.fixture(scope="session")
def locators_init(request, locators):
    session = request.node
    for item in session.items:
        cls = item.getparent(pytest.Class)
        setattr(cls.obj, "locators", locators)
    yield


@pytest.fixture(scope="session")
def driver_init(request):
    options = FirefoxOptions()
    options.page_load_strategy = 'eager'
    profile_path = r"/home/zxxz/.mozilla/firefox/70g38rbt.Selenium_webdriver"
    options.set_preference('profile', profile_path)
    service = Service('/home/zxxz/.cargo/bin/geckodriver')
    web_driver = webdriver.Firefox(
        service=service,
        options=options,
    )
    session = request.node
    for item in session.items:
        cls = item.getparent(pytest.Class)
        setattr(cls.obj, "driver", web_driver)
    yield
    web_driver.close()
