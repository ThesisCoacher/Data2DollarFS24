# Import the necessary libraries from Scrapy and Selenium
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import csv
from urllib.parse import parse_qs, urlparse

# Define a new Spider class that inherits from scrapy.Spider
class GetDataSpider(scrapy.Spider):
    # Name your spider 'getdata'ss
    name = 'getdata3'
    # Define the domain(s) that the spider is allowed to scrape
    allowed_domains = ['www.airbnb.com']
    # List the URL(s) the spider will start from
    start_urls = ["https://www.airbnb.com/s/St.-Gallen--Switzerland/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-04-01&monthly_length=3&monthly_end_date=2024-07-01&price_filter_input_type=2&channel=EXPLORE&query=St.%20Gallen%2C%20Switzerland&place_id=ChIJVdgzdikem0cRFGH-HwhQIpo&date_picker_type=calendar&checkin=2024-06-27&checkout=2024-06-30&source=structured_search_input_header&search_type=filter_change&price_filter_num_nights=10", "https://www.airbnb.com/s/St.-Gallen--Switzerland/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-04-01&monthly_length=3&monthly_end_date=2024-07-01&price_filter_input_type=2&channel=EXPLORE&query=St.%20Gallen%2C%20Switzerland&place_id=ChIJVdgzdikem0cRFGH-HwhQIpo&date_picker_type=calendar&checkin=2024-10-10&checkout=2024-10-20&source=structured_search_input_header&search_type=autocomplete_click"]


    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.csvfile = open('Alle100Unterkuenfte.csv', 'w', newline='')
        self.writer = csv.writer(self.csvfile)
        self.id_counter = 1
        self.global_count = 0

    def start_requests(self):
        try:
            for url in self.start_urls:
                self.id_counter = 1
                self.global_count = 0
                self.driver.get(url)
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)
                checkin_date = query_params.get('checkin', [''])[0]
                checkout_date = query_params.get('checkout', [''])[0]
                dates = f"({checkin_date} - {checkout_date})"
                self.writer.writerow([dates])
                self.writer.writerow(['Nummer', 'Name der Unterkunft', 'Preis pro Nacht'])
                while True:
                    self.scrape_page()
                    if self.global_count >= 100:
                        break
                    try:
                        wait = WebDriverWait(self.driver, 5)
                        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Weiter" or @aria-label="Next"]')))
                        next_button.click()
                        sleep(5)
                    except NoSuchElementException:
                        break 
        finally:
            self.driver.quit()
            self.csvfile.close()

    def scrape_page(self):
        sleep(5)
        
        sel = Selector(text=self.driver.page_source)
        
        # CSS selectors to extract the unterkunft elements from the page
        unterkuenfte = sel.css('div.g1qv1ctd')

        # Iterate over the unterkuenfte and extract the required information
        for unterkunft in unterkuenfte:
            # Check if we have already written 100 entries to the CSV file
            if self.global_count >= 100:
                break

            # Check if the unterkunft has an ancestor with the specified class to be excluded
            if unterkunft.xpath('ancestor::div[contains(@class, "fj2orl9") and contains(@class, "atm_da_cbdd7d") and contains(@class, "dir") and contains(@class, "dir-ltr")]'):
                continue

            # Extract the name of the unterkunft
            unterkunft_name = unterkunft.css('span.dir.dir-ltr::text').get()

            # Extract the preis pro nacht
            preis_pro_nacht = unterkunft.css('span._tyxjp1::text').get()
            # If the original price selector didn't find anything, try to get the sale price
            if preis_pro_nacht is None:
                preis_pro_nacht = unterkunft.css('span._1y74zjx::text').get()

            # Write the Nummer, Name der Unterkunft, and Preis pro Nacht to the CSV file
            self.writer.writerow([self.id_counter, unterkunft_name, preis_pro_nacht])
            # Increment the ID counter and the global counter
            self.id_counter += 1
            self.global_count += 1

    def parse(self, response):
        pass
