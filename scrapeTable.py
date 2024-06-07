from typing import Dict
from typing import List

from bs4 import BeautifulSoup

# Utils ################################################################################


def getFirstPContents(thingWithP: BeautifulSoup) -> str:
    return thingWithP.find_all("p")[0].contents[0].strip()


def getFirstH5Contents(thingWithH5: BeautifulSoup) -> str:
    return thingWithH5.find_all("h5")[0].contents[0].strip()


# Primary Table Scraper ################################################################


def scrapeTableStyle1(table: BeautifulSoup) -> List[Dict[str, str]]:
    rows = table.find_all("div", {"class": "table-module__row"})

    data = []
    for row in rows:
        cols = row.find_all("div", {"class": "table-module__column"})
        # Column 1: Type
        type = getFirstPContents(cols[0])

        # Column 2: Rating
        rating = getFirstH5Contents(cols[1])

        # Column 3: Rating Date
        ratingDate = getFirstPContents(cols[2])

        # Column 4: Review Date
        reviewDate = getFirstPContents(cols[3])

        data.append(
            {
                "Type": type,
                "Rating": rating,
                "Rating Date": ratingDate,
                "Review Date": reviewDate,
            }
        )

    return data


# Evaluation Rankings Scraper ##########################################################


def scrapeSERTable(table) -> List[Dict[str, str]]:
    rows = table.find_all("div", {"class": "table-module__row"})

    data = []
    for row in rows:
        cols = row.find_all("div", {"class": "table-module__column"})

        # Column 1: Country
        country = getFirstPContents(cols[0])

        # Column 2: Operation
        op = getFirstPContents(cols[1])

        # Column 3: Ranking
        rank = getFirstH5Contents(cols[2])

        # Column 4: Ranking Date
        rDate = getFirstPContents(cols[3])

        data.append(
            {
                "Country": country,
                "Operation": op,
                "Ranking": rank,
                "Ranking Date": rDate,
            }
        )

    return data


# Pubfin Scraper #######################################################################


def scrapePubfinTable(table) -> List[Dict[str, str]]:
    rows = table.find_all("div", {"class": "table-module__row"})

    data = []
    for row in rows:
        cols = row.find_all("div", {"class": "table-module__column"})

        # Column 1: Class
        clss = getFirstPContents(cols[0])

        # Column 2: Maturity Date
        matDate = getFirstPContents(cols[1])

        # Column 3: Rating Type
        rType = getFirstPContents(cols[2])

        # Column 4: Rating
        rating = getFirstH5Contents(cols[3])

        # Column 5: Rating Date
        ratDate = getFirstPContents(cols[4])

        # Column 6: Last Review Date
        revDate = getFirstPContents(cols[5])

        data.append(
            {
                "Class": clss,
                "Maturity Date": matDate,
                "Rating Type": rType,
                "Rating": rating,
                "Rating Date": ratDate,
                "Last Review Date": revDate,
            }
        )

    return data
