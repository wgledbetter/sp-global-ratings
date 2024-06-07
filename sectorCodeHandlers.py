import csv
import time
from pathlib import Path
from typing import Dict

import ipdb
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

import settings as st
from scrapeTable import scrapePubfinTable
from scrapeTable import scrapeSERTable
from scrapeTable import scrapeTableStyle1
from tryAcceptCookies import tryAcceptCookies
from utils import waitForRow

# Utils ################################################################################


def getRatingTableName(table: BeautifulSoup) -> str:
    return (
        table.find_all("div", {"class": "breadcumb"})[0]
        .find_all("li")[0]
        .contents[0]
        .strip()
    )


# --------------------------------------------------------------------------------------


def getRankingTableName(table: BeautifulSoup) -> str:
    return (
        table.find_all("div", {"class": "breadcumb"})[0]
        .find_all("span")[0]
        .contents[0]
        .strip()
    )


# FI and CORP handler ##################################################################


def sectorCodeHandler_FI_CORP(
    entity: str, pageSource: BeautifulSoup, data: Dict, writeCSVs: bool
):
    # Scrape rating tables -------------------------------------------------------------

    ratingTables = pageSource.find_all("div", {"class": "table-module-data"})

    for table in ratingTables:
        if table.find_all("div") == []:
            # This protects against empty ratings tables
            continue

        tbName = getRatingTableName(table)

        tbData = scrapeTableStyle1(table)
        data[entity][tbName] = tbData

        if writeCSVs:
            with open(Path(st.OUTPUT_PREFIX) / f"{entity}-{tbName}.csv", "w") as f:
                cw = csv.writer(f)
                cw.writerow(st.RATING_TABLE_HEADERS)
                for d in tbData:
                    cw.writerow([d[h] for h in st.RATING_TABLE_HEADERS])

    # "Servicer Evaluation Ranking" Tables ---------------------------------------------

    rankingTables = pageSource.find_all("app-se-rankings")

    for table in rankingTables:
        if table.find_all("div") == []:
            # This protects against empty rankings tables
            continue

        tbName = getRankingTableName(table)

        tbData = scrapeSERTable(table)
        data[entity][tbName] = tbData

        if writeCSVs:
            with open(Path(st.OUTPUT_PREFIX) / f"{entity}-{tbName}.csv", "w") as f:
                cw = csv.writer(f)
                cw.writerow(st.RANKING_TABLE_HEADERS)
                for d in tbData:
                    cw.writerow([d[h] for h in st.RANKING_TABLE_HEADERS])


# PUBFIN handler #######################################################################


def sectorCodeHandler_PUBFIN(
    browser: WebDriver,
    entity: str,
    data: Dict,
    writeCSVs: bool,
):
    rowElems = browser.find_elements(By.CLASS_NAME, "table-module__row")

    for i in range(len(rowElems)):
        # If the cookie prompt is visible, we can't click all elements
        tryAcceptCookies(browser)

        rowElem = browser.find_elements(By.CLASS_NAME, "table-module__row")[i]
        linkElem = rowElem.find_element(By.TAG_NAME, "a")
        linkAddr = linkElem.get_attribute("href")
        issueId = linkAddr.split("/")[-1]
        tbName = f"Issue ID {issueId}"

        # I have to click it because it gave me 404s when I navigated directly to the link.
        linkElem.click()
        waitForRow(browser)

        bs = BeautifulSoup(browser.page_source)
        tbData = scrapePubfinTable(
            bs.find_all("div", {"class": "table-module__content"})[0]
        )
        data[entity][tbName] = tbData

        if writeCSVs:
            with open(Path(st.OUTPUT_PREFIX) / f"{entity}-{tbName}.csv", "w") as f:
                cw = csv.writer(f)
                cw.writerow(st.ISSUE_TABLE_HEADERS)
                for d in tbData:
                    cw.writerow([d[h] for h in st.ISSUE_TABLE_HEADERS])

        browser.back()
        waitForRow(browser)
