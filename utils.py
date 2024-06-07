import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def waitForRow(browser):
    ui.WebDriverWait(browser, 1000).until(
        EC.presence_of_element_located((By.CLASS_NAME, "table-module__row"))
    )
