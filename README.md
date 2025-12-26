Review Scraper

step-1:
Project Description:
This project is a Python-based review scraping script that collects user reviews
from G2, Capterra, and TrustRadius based on a given company name
and time period.
The script parses reviews, handles pagination, filters by date range, and stores
the results in a structured JSON format.

step-2:
Features
* Scrape reviews by company name
* Filter reviews by start and end date
* Supports multiple sources:
  * G2
  * Capterra
  * TrustRadius
* Handles pagination automatically
* Outputs data in structured JSON format
* Graceful handling of invalid inputs and empty results

step-3:
Technologies Used:
* Python
* requests
* BeautifulSoup
* JSON
* datetime

step-4:
To run the script:
python review_scraper.py

step-5:
Enter details when prompted:
*Company name (slug):
*Source (g2 / capterra / trustradius):
*Start date (YYYY-MM-DD):
*End date (YYYY-MM-DD):

step-6:
After that the output will looks like that in json file
