import csv

import selenium.webdriver.support.ui as ui
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Settings #############################################################################

LOGIN_URL = "https://www.spglobal.com/ratings/en/login"
DONE_LOGIN_URL = "https://www.spglobal.com/ratings/en/"

BASE_URL = "https://disclosure.spglobal.com/ratings/en/regulatory/org-details/sectorCode/{sectorCode}/entityId/{entityId}"
ENTITIES = {
    "Sony": {"sectorCode": "FI", "entityId": 354137},
    "AEG": {"sectorCode": "CORP", "entityId": 313715},
    "BofA": {"sectorCode": "CORP", "entityId": 413007},
    "Bath & Bodyworks": {"sectorCode": "CORP", "entityId": 106105},
    "7-Eleven": {"sectorCode": "CORP", "entityId": 102181},
    "Birkenstock": {"sectorCode": "CORP", "entityId": 687414},
    "Bright Horizons Family Solutions": {"sectorCode": "FI", "entityId": 445143},
    "Chase Bank": {"sectorCode": "FI", "entityId": 102911},
    # "Cortland": 15855,  # has the issue list issue
    "Truist": {"sectorCode": "FI", "entityId": 108973},
    "Cumulus Media": {"sectorCode": "CORP", "entityId": 324702},
    "CVS": {"sectorCode": "CORP", "entityId": 101476},
}
TABLE_MODULE_ROW_CLASS_NAME = "table-module__row"
TABLE_MODULE_COL_CLASS_NAME = "table-module__column"

# Main #################################################################################


def main():
    with webdriver.Firefox() as browser:
        browser.get(LOGIN_URL)
        ui.WebDriverWait(browser, 1000).until(EC.url_matches(DONE_LOGIN_URL))

        for entity in ENTITIES:
            # Load page with data
            browser.get(
                BASE_URL.format(
                    sectorCode=ENTITIES[entity]["sectorCode"],
                    entityId=ENTITIES[entity]["entityId"],
                )
            )
            ui.WebDriverWait(browser, 1000).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, TABLE_MODULE_ROW_CLASS_NAME)
                )
            )

            # Scrape page source for what we care about
            bs = BeautifulSoup(browser.page_source, "html.parser")
            rows = bs.find_all("div", {"class": TABLE_MODULE_ROW_CLASS_NAME})

            data = []
            for row in rows:
                cols = row.find_all("div", {"class": TABLE_MODULE_COL_CLASS_NAME})
                # Column 1: Type
                type = cols[0].find_all("p")[0].contents[0]

                # Column 2: Rating
                rating = cols[1].find_all("h5")[0].contents[0]

                # Column 3: Rating Date
                ratingDate = cols[2].find_all("p")[0].contents[0]

                # Column 4: Review Date
                reviewDate = cols[3].find_all("p")[0].contents[0]

                data.append([type, rating, ratingDate, reviewDate])

            with open(f"{entity}.csv", "w") as f:
                cw = csv.writer(f)
                cw.writerow(["Type", "Rating", "Rating Date", "Review Date"])
                cw.writerows(data)


# Run ##################################################################################

if __name__ == "__main__":
    main()
