
# imports some libraries from Scrapy and Selenium and others that are required for the spider
import csv
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import parse_qs, urlparse
from time import sleep


# defines a new Spider class that inherites from scrapy.Spider
class AirbnbSpider(scrapy.Spider):
    name = 'myspider'  # names my spider 'myspider'
    allowed_domains = ['airbnb.com']  # defines the domain that the spider is allowed to scrape
    # lists the URL(s) the spider will start from; already filtered for St. Gallen, Switzerland, and the two different date ranges
    start_urls = ['https://www.airbnb.com/s/St-Gallen--Switzerland/homes?checkin=2024-06-27&checkout=2024-06-30',
                  'https://www.airbnb.com/s/St-Gallen--Switzerland/homes?checkin=2024-10-10&checkout=2024-10-20']


    # initializes the spider
    def __init__(self):
        self.driver = webdriver.Chrome()  # initializes the Chrome web driver
        self.driver.maximize_window()
        self.csvfile = open('2_SpoerryGraciela.csv', 'w', newline='', encoding='utf-8') # opens the CSV file in write mode
        self.writer = csv.writer(self.csvfile)  # creates a CSV writer object
        self.writer.writerow(['Zeitraum', 'Name', 'Preis pro Nacht']) # writes the header row to the CSV file
        self.counters = {url: 0 for url in self.start_urls}  # initializes a counter for each start URL


    # sends a request to each start URL
    def start_requests(self): 
        for url in self.start_urls:  # loops through the start URLs
            yield scrapy.Request(url=url, callback=self.parse)  # sends a request to each start URL


    # extracts the check-in and check-out dates from the URL and creates a date range string
    def parse(self, response):
        self.driver.get(response.url)
        query = parse_qs(urlparse(response.url).query)  # parses the query parameters from the URL
        checkin = query.get('checkin', [''])[0]  # extracts the check-in date
        checkout = query.get('checkout', [''])[0]  # extracts the check-out date
        date_range = f"{checkin} – {checkout}"  # creates a date range string; called Zeitraum s. above
        self.navigate_and_scrape(date_range, response.url)


    # navigates to the next page and scrapes the data
    def navigate_and_scrape(self, date_range, url):
        while self.counters[url] < 100:  # loops until 100 listings are scraped
            self.scrape_page(date_range, url)  
            if self.counters[url] >= 100:  # breaks the loop if 100 listings are scraped
                break
            try:
                wait = WebDriverWait(self.driver, 10)   # waits for the next button to be clickable
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Next"]'))) # finds the next button with the specified XPath
                next_button.click() # clicks the next button
                sleep(5)
            except (NoSuchElementException, TimeoutException):  # breaks the loop if the next button is not found
                break


    # scrapes the data from the current page
    def scrape_page(self, date_range, url):
        sleep(5)
        sel = Selector(text=self.driver.page_source)  # creates a Selector object from the page source
        apts = sel.css('div.g1qv1ctd')  # selects the apartment listings

        for apt in apts:
            if self.counters[url] >= 100:  # breaks the loop if 100 listings are scraped
                break
            apt_name = apt.css('span.dir.dir-ltr::text').get()  # extracts the apartment name with the specified CSS selector; called Name s. above
            price_per_night = apt.css('span._tyxjp1::text').get()  # extracts the price per night with the specified CSS selector; called Preis pro Nacht s. above
            if price_per_night is None:
                price_per_night = apt.css('span._1y74zjx::text').get()  # extracts the price per night with the specified CSS selector if the first one is None
            self.writer.writerow([date_range, apt_name, price_per_night])  # writes the data to the CSV file
            self.counters[url] += 1  # increments the counter for the current URL


    # closes the web driver after scraping is complete
    def close_spider(self):
        self.driver.quit()  # closes the web driver
        self.csvfile.close()  # closes the CSV file
        total_scraped = sum(self.counters.values())  # calculates the total number of listings scraped
        self.logger.info(f"Total scraped listings: {total_scraped}") 

