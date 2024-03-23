import scrapy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
from time import sleep
import csv
from urllib.parse import parse_qs, urlparse

class GetdataSpider(scrapy.Spider):
    name = "assign2"
    allowed_domains = ["www.airbnb.com"]
    # List to start the URLs
    start_urls = ["https://www.airbnb.com/s/St.-Gallen--Switzerland/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-04-01&monthly_length=3&monthly_end_date=2024-07-01&price_filter_input_type=2&channel=EXPLORE&query=St.%20Gallen%2C%20Switzerland&place_id=ChIJVdgzdikem0cRFGH-HwhQIpo&date_picker_type=calendar&checkin=2024-06-27&checkout=2024-06-30&source=structured_search_input_header&search_type=filter_change&price_filter_num_nights=10", 
                  "https://www.airbnb.com/s/St.-Gallen--Switzerland/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-04-01&monthly_length=3&monthly_end_date=2024-07-01&price_filter_input_type=2&channel=EXPLORE&query=St.%20Gallen%2C%20Switzerland&place_id=ChIJVdgzdikem0cRFGH-HwhQIpo&date_picker_type=calendar&checkin=2024-10-10&checkout=2024-10-20&source=structured_search_input_header&search_type=autocomplete_click"]

    def __init__(self):
        # Initialize a new Chrome WebDriver
        self.driver = webdriver.Chrome()
        # Maximize the Chrome window
        self.driver.maximize_window()
        # Open the CSV file for writing
        self.csvfile = open('houses3.csv', 'w', newline='')
        self.writer = csv.writer(self.csvfile)
        # Initialize the ID counter
        self.id_counter = 1
        # Initialize the global counter
        self.global_count = 0

    def start_requests(self):
        try:
            # Start the WebDriver and get the start URLs
            for url in self.start_urls:
                self.id_counter = 1 # Reset the ID counter for each URL
                self.global_count = 0 # Reset the global counter for each URL
                self.driver.get(url)
                # Parse the URL to get the check-in and check-out dates
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)
                checkin_date = query_params.get('checkin', [''])[0]
                checkout_date = query_params.get('checkout', [''])[0]
                dates = f"({checkin_date} - {checkout_date})"
                # Write the dates and the header row to the CSV file
                self.writer.writerow([dates])
                self.writer.writerow(['ID', 'House Name', 'Price per Night'])
                while True:
                    # Scrape the data from the current page
                    self.scrape_page()
                    if self.global_count >= 100:
                        break
                    try:
                        wait = WebDriverWait(self.driver, 5)
                        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Weiter" or @aria-label="Next"]')))
                        next_button.click()
                        sleep(5)  # wait for the next page to load
                    except NoSuchElementException:
                        break  # no more pages
        finally:
            # Close the Chrome window
            self.driver.quit()
            # Close the CSV file
            self.csvfile.close()

    # Define the method for scraping the page
    def scrape_page(self):
        # Sleep/wait for 5 seconds to allow the page to load
        sleep(5)
        
        # Create a Selector object from the page source, allowing Scrapy to parse the HTML
        sel = Selector(text=self.driver.page_source)
        
        # Use CSS selectors to extract the house elements from the page
        houses = sel.css('div.g1qv1ctd')

        # Iterate over the houses and extract the required information
        for house in houses:
            # Check if 100 entries are written to the CSV file
            if self.global_count >= 100:
                break

            # Check if the house has an ancestor with the specified class to be excluded
            if house.xpath('ancestor::div[contains(@class, "fj2orl9") and contains(@class, "atm_da_cbdd7d") and contains(@class, "dir") and contains(@class, "dir-ltr")]'):
                continue

            # Extract the house name
            house_name = house.css('span.dir.dir-ltr::text').get()

            # Extract the price per night
            price_per_night = house.css('span._tyxjp1::text').get()
            # If the original price selector didn't find anything, try to get the sale price
            if price_per_night is None:
                price_per_night = house.css('span._1y74zjx::text').get()

            # Write the ID, house name, and price to the CSV file
            self.writer.writerow([self.id_counter, house_name, price_per_night])
            # Increment the ID counter and the global counter
            self.id_counter += 1
            self.global_count += 1

    def parse(self, response):
        pass