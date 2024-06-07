# Settings and Constants

LOGIN_URL = "https://www.spglobal.com/ratings/en/login"
DONE_LOGIN_URL = "https://www.spglobal.com/ratings/en/"

FI_CORP_BASE_URL = "https://disclosure.spglobal.com/ratings/en/regulatory/org-details/sectorCode/{sectorCode}/entityId/{entityId}"
PUBFIN_BASE_URL = "https://disclosure.spglobal.com/ratings/en/regulatory/entity/org-details/sectorCode/{sectorCode}/entityId/{entityId}"

RATING_TABLE_HEADERS = ["Type", "Rating", "Rating Date", "Review Date"]
RANKING_TABLE_HEADERS = ["Country", "Operation", "Ranking", "Ranking Date"]
ISSUE_TABLE_HEADERS = ["Class", "Maturity Date", "Rating Type", "Rating", "Rating Date"]

OUTPUT_PREFIX = "data"

INDIVIDUAL_CSVS = True
