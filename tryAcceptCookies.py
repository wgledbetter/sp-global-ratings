import time

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver


def tryAcceptCookies(browser: WebDriver):
    maybeAcceptCookies = browser.find_elements(By.ID, "onetrust-accept-btn-handler")

    if maybeAcceptCookies != []:
        try:
            maybeAcceptCookies[0].click()
            time.sleep(0.5)
        except:
            pass
