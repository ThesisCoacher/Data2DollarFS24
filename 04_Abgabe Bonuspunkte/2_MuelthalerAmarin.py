"""
Before you start, it is very important to note that the code right now is not supposed to be run from the terminal, but
rather the code can be directly run through the main function from your interpreter of choice. If you desire to run the
spider from the terminal, please comment out the code block at the very bottom, that starts with
"if __name__ == "__main__":"
"""
import scrapy
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from time import sleep
from urllib.parse import urlparse, parse_qs
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


"""
Here the spider class is created. We define the name of the spider "airspider", the domain that is to be scraped and
the links from where the scraping should be started from, in this case the date-ranges 10.-20.10. and 27.-30.6. 
"""
class AirbnbSpider(scrapy.Spider):
    name = "airspider"
    allowed_domains = ["airbnb.com"]
    start_urls = ["https://www.airbnb.com/s/St-Gallen--Switzerland/homes?checkin=2024-06-27&checkout=2024-06-30",
                  "https://www.airbnb.com/s/St-Gallen--Switzerland/homes?checkin=2024-10-10&checkout=2024-10-20"]

    def __init__(self):
        super(AirbnbSpider, self).__init__()
        # first we initialise the Browser options
        chrome_options = Options()
        # this line makes it so the browser does not open during the scraping process
        chrome_options.add_argument("--headless")
        # Initialize the WebDriver with the specified options
        self.driver = webdriver.Chrome(options=chrome_options)
        # Next, a csv file is created in utf-8 encoding so there are no UnicodeEncodingErrors
        self.csvfile = open("assignment_2.csv", "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.csvfile)
        # Next to the relevant data I've added a "Date Range" column to more transparently show for which time window
        # the individual bookings are available
        self.writer.writerow(["Date Range", "Short Description", "Price per Night"])
        # setting the counter to 0 for each url
        self.counters = {url: 0 for url in self.start_urls}

# starts the scraping for each url
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

# responsible for the parsing
    def parse(self, response):
        self.driver.get(response.url)
        query = parse_qs(urlparse(response.url).query)
        # gets the checkin and checkout dates, so it is clear
        checkin = query.get("checkin", [""])[0]
        checkout = query.get("checkout", [""])[0]
        date_range = f"{checkin} – {checkout}"
        self.navigate_and_scrape(date_range, response.url)

# this function is responsible for navigating to the next page, if there have not yet been 100 entries scraped
    def navigate_and_scrape(self, date_range, url):
        while self.counters[url] < 100:
            self.scrape_page(date_range, url)
            if self.counters[url] >= 100:
                break
            try:
                wait = WebDriverWait(self.driver, 10)
                # navigation to the next page
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next']")))
                next_button.click()
                # here the scraper should wait until the element of the places have loaded
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.g1qv1ctd")))
            # error handling
            except (NoSuchElementException, TimeoutException) as e:
                self.logger.info(f"No more pages to navigate or error occurred: {e}")
                break
            except Exception as e:
                self.logger.error(f"An unexpected error occurred while navigating: {e}")
                break

# this is the main scraping function which defines which info is supposed to be scraped
    def scrape_page(self, date_range, url):
        sleep(5)
        sel = Selector(text=self.driver.page_source)
        places = sel.css("div.g1qv1ctd")

        for place in places:
            if self.counters[url] >= 100:
                break
            # getting the description of the place
            place_name = place.css("span.dir.dir-ltr::text").get()
            # getting the price: when the price is reduced, it has to be taken from a different selector.
            price_per_night = place.css("span._tyxjp1::text").get() or place.css("span._1y74zjx::text").get()

            try:
                self.writer.writerow([date_range, place_name, price_per_night])
            # error handling
            except UnicodeEncodeError as e:
                print(f"Encoding error while writing to CSV: {e}")
            except Exception as e:
                print(f"Unexpected error while writing to CSV: {e}")
            self.counters[url] += 1

    # While this function should handle the close_spider that happens at end of the scraping, however the function does
    # not seem to run which is shown by the print statement not being executed.
    # Since everything else seems to work I will not adjust this right now
    def close_spider(self):
        print("***** Closing Spider *****")
        self.logger.critical("***** Closing Spider *****")
        total_scraped = sum(self.counters.values())
        self.logger.info(f"Total scraped listings: {total_scraped}")
        self.driver.quit()
        self.csvfile.close()


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(AirbnbSpider)
    process.start()

#comment this code snippet out if the spider should be run from the terminal
if __name__ == "__main__":
    main()