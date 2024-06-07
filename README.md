# SP Global Ratings Scraper

Web-scraping tool for `spglobal.com`'s ratings

## Changelog

### 2024-06-06

- Moved `ENTITIES` to `input.py`.
- Added separate handling of "Issuer Credit Rating"/"Resolution Counterparty Rating" vs. "Servicer Evaluation Rankings".
- Moved table parsing to functions in `scrapeTable.py`
- Changes to pre-empt future downstream processing development:
  - CSV output is toggled with the `writeCSVs` argument to `main()`
  - `main()` collects and returns a big dictionary of everything that's been scraped.
- CSVs are now placed in a `data` folder for better organization
- Full scraped data is saved to a json.
- Moved all constants to `settings.py`
- Broken attempt at auto-login (I think it thinks I'm a robot)
- Handling of Sector Code `PUBFIN` pages
- Refactor of page parsing into `sectorCodeHandlers.py`
- Add `utils.py` for general functions

## Usage

- Run `main.py`
- Login with your S&P Global Ratings account credentials
- Wait

## Notes

- Noticed a hiccup scraping Cortland where records took some time to load, and the script moved along as if no data existed.

## TODO

- [ ] Maybe have `PUBFIN` use the link text for `tbName`.
