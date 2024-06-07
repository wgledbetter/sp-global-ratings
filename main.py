import json
import time
from pathlib import Path
from typing import Dict

import selenium.webdriver.support.ui as ui
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import settings as st
from input import ENTITIES
from sectorCodeHandlers import sectorCodeHandler_FI_CORP
from sectorCodeHandlers import sectorCodeHandler_PUBFIN
from slowSendKeys import slowSendKeys
from utils import waitForRow

# Main #################################################################################


def main(
    login: Dict = {},
    entities: Dict = ENTITIES,
    writeCSVs: bool = st.INDIVIDUAL_CSVS,
):
    with webdriver.Firefox() as browser:
        browser.get(st.LOGIN_URL)

        if login == {}:
            ui.WebDriverWait(browser, 1000).until(EC.url_matches(st.DONE_LOGIN_URL))
        else:
            ui.WebDriverWait(browser, 1000).until(
                EC.presence_of_element_located((By.ID, "input27"))
            )
            userNameInput = browser.find_element(By.ID, "input27")
            slowSendKeys(userNameInput, login["user"])
            userNameInput.send_keys(Keys.RETURN)

            ui.WebDriverWait(browser, 1000).until(
                EC.presence_of_element_located((By.CLASS_NAME, "authenticator-button"))
            )
            usePassword = browser.find_elements(By.CLASS_NAME, "authenticator-button")[
                1
            ]
            usePassword.click()

            ui.WebDriverWait(browser, 1000).until(
                EC.presence_of_element_located((By.CLASS_NAME, "password-with-toggle"))
            )
            passwordInput = browser.find_element(By.CLASS_NAME, "password-with-toggle")
            slowSendKeys(passwordInput, login["pass"])
            time.sleep(1)

        data = {}
        for entity in entities:
            # Initialize full data storage
            data[entity] = {}

            eid = entities[entity]["entityId"]
            sc = entities[entity]["sectorCode"]

            # Parse Data ---------------------------------------------------------------

            if entities[entity]["sectorCode"] in ["FI", "CORP"]:
                browser.get(st.FI_CORP_BASE_URL.format(sectorCode=sc, entityId=eid))
                waitForRow(browser)

                sectorCodeHandler_FI_CORP(
                    entity=entity,
                    pageSource=BeautifulSoup(browser.page_source, "html.parser"),
                    data=data,
                    writeCSVs=writeCSVs,
                )

            elif entities[entity]["sectorCode"] in ["PUBFIN"]:
                browser.get(st.PUBFIN_BASE_URL.format(sectorCode=sc, entityId=eid))
                waitForRow(browser)

                sectorCodeHandler_PUBFIN(
                    browser=browser,
                    entity=entity,
                    data=data,
                    writeCSVs=writeCSVs,
                )

        return data


# Run ##################################################################################

if __name__ == "__main__":
    d = main()
    with open(Path(st.OUTPUT_PREFIX) / "data.json", "w") as f:
        f.write(json.dumps(d))
