import os

import pytest
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.service import Service


def should_drop(s):
    return s.startswith("#", 0) or len(s) == 0


def get_file(config, name):
    curr_path = config.invocation_params.dir.cwd()
    return os.path.join(curr_path, name)


def get_props(file_path):
    res = {}
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


@pytest.fixture(scope='session')
def settings(pytestconfig):
    file_path = get_file(pytestconfig, "settings")
    return get_props(file_path)


@pytest.fixture(scope='session')
def locators(pytestconfig):
    file_path = get_file(pytestconfig, "locators")
    return get_props(file_path)


@pytest.fixture(scope="session")
def tests_init(request, locators, settings):
    session = request.node
    for item in session.items:
        cls = item.getparent(pytest.Class)
        setattr(cls.obj, "locators", locators)
        setattr(cls.obj, "settings", settings)
    yield


@pytest.fixture(scope="session")
def driver_init(request, settings):
    options = FirefoxOptions()
    options.page_load_strategy = settings['page_load_strategy']
    options.headless = eval(settings["headless"])
    profile_path = settings['browser_profile']
    options.set_preference('profile', profile_path)
    service = Service(settings['driver_exec_path'])
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
