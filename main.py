import csv
import json
from pathlib import Path
from typing import Dict

import selenium.webdriver.support.ui as ui
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import settings as st
from input import ENTITIES
from scrapeTable import scrapeSERTable
from scrapeTable import scrapeTableStyle1

# Useful Functions #####################################################################


def getRatingTableName(table: BeautifulSoup) -> str:
    return (
        table.find_all("div", {"class": "breadcumb"})[0]
        .find_all("li")[0]
        .contents[0]
        .strip()
    )


def getRankingTableName(table: BeautifulSoup) -> str:
    return (
        table.find_all("div", {"class": "breadcumb"})[0]
        .find_all("span")[0]
        .contents[0]
        .strip()
    )


# Main #################################################################################


def main(entities: Dict = ENTITIES, writeCSVs: bool = st.INDIVIDUAL_CSVS):
    with webdriver.Firefox() as browser:
        browser.get(st.LOGIN_URL)
        ui.WebDriverWait(browser, 1000).until(EC.url_matches(st.DONE_LOGIN_URL))

        data = {}
        for entity in entities:
            # Initialize full data storage
            data[entity] = {}

            # Load page ----------------------------------------------------------------

            browser.get(
                st.BASE_URL.format(
                    sectorCode=ENTITIES[entity]["sectorCode"],
                    entityId=ENTITIES[entity]["entityId"],
                )
            )
            ui.WebDriverWait(browser, 1000).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, st.TABLE_MODULE_ROW_CLASS_NAME)
                )
            )

            bs = BeautifulSoup(browser.page_source, "html.parser")

            # Scrape rating tables -----------------------------------------------------

            ratingTables = bs.find_all("div", {"class": "table-module-data"})

            for table in ratingTables:
                if table.find_all("div") == []:
                    # This protects against empty ratings tables
                    continue

                tbName = getRatingTableName(table)

                tbData = scrapeTableStyle1(table)
                data[entity][tbName] = tbData

                if writeCSVs:
                    with open(
                        Path(st.OUTPUT_PREFIX) / f"{entity}-{tbName}.csv", "w"
                    ) as f:
                        cw = csv.writer(f)
                        cw.writerow(st.RATING_TABLE_HEADERS)
                        for d in tbData:
                            cw.writerow([d[h] for h in st.RATING_TABLE_HEADERS])

            # "Servicer Evaluation Ranking" Tables -------------------------------------

            rankingTables = bs.find_all("app-se-rankings")

            for table in rankingTables:
                if table.find_all("div") == []:
                    # This protects against empty rankings tables
                    continue

                tbName = getRankingTableName(table)

                tbData = scrapeSERTable(table)
                data[entity][tbName] = tbData

                if writeCSVs:
                    with open(
                        Path(st.OUTPUT_PREFIX) / f"{entity}-{tbName}.csv", "w"
                    ) as f:
                        cw = csv.writer(f)
                        cw.writerow(st.RANKING_TABLE_HEADERS)
                        for d in tbData:
                            cw.writerow([d[h] for h in st.RANKING_TABLE_HEADERS])

        return data


# Run ##################################################################################

if __name__ == "__main__":
    d = main()
    with open(Path(st.OUTPUT_PREFIX) / "data.json", "w") as f:
        f.write(json.dumps(d))
