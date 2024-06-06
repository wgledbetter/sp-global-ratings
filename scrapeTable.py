from typing import List

from bs4 import BeautifulSoup


def scrapeTableStyle1(table: BeautifulSoup) -> List[List[str]]:
    rows = table.find_all("div", {"class": "table-module__row"})

    data = []
    for row in rows:
        cols = row.find_all("div", {"class": "table-module__column"})
        # Column 1: Type
        type = cols[0].find_all("p")[0].contents[0]

        # Column 2: Rating
        rating = cols[1].find_all("h5")[0].contents[0]

        # Column 3: Rating Date
        ratingDate = cols[2].find_all("p")[0].contents[0]

        # Column 4: Review Date
        reviewDate = cols[3].find_all("p")[0].contents[0]

        data.append([type, rating, ratingDate, reviewDate])

    return data
