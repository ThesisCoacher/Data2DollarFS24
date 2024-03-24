
import scrapy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
from urllib.parse import parse_qs, urlparse
from time import sleep
import csv


class GetdataSpider(scrapy.Spider):
    name = "getdata"
    allowed_domains = ["www.airbnb.com"]
    # List to start the URLs
    start_urls = ["https://www.airbnb.com/s/St.-Gallen--Switzerland/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-04-01&monthly_length=3&monthly_end_date=2024-07-01&price_filter_input_type=2&channel=EXPLORE&query=St.%20Gallen%2C%20Switzerland&place_id=ChIJVdgzdikem0cRFGH-HwhQIpo&date_picker_type=calendar&checkin=2024-06-27&checkout=2024-06-30&source=structured_search_input_header&search_type=filter_change&price_filter_num_nights=10", 
                  "https://www.airbnb.com/s/St.-Gallen--Switzerland/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-04-01&monthly_length=3&monthly_end_date=2024-07-01&price_filter_input_type=2&channel=EXPLORE&query=St.%20Gallen%2C%20Switzerland&place_id=ChIJVdgzdikem0cRFGH-HwhQIpo&date_picker_type=calendar&checkin=2024-10-10&checkout=2024-10-20&source=structured_search_input_header&search_type=autocomplete_click"]

    def __init__(self):
        # Initialize a new Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.csvfile = open('scraped_listings.csv', 'w', newline='')
        self.writer = csv.writer(self.csvfile)
        self.global_count = 0

    def start_requests(self):
        try:
            for url in self.start_urls:
                self.global_count = 0
                self.driver.get(url)
            
                from urllib.parse import urlparse, parse_qs
                checkin_date, checkout_date = parse_qs(urlparse(url).query).get('checkin', [''])[0], parse_qs(urlparse(url).query).get('checkout', [''])[0]
                dates = "({} - {})".format(checkin_date, checkout_date)

                
                self.writer.writerow(['Name der Unterkunft', 'Preis pro Nacht'])

                while self.global_count < 100:
                    self.scrape_page()

                    try:
                        wait = WebDriverWait(self.driver, 5)
                        next_button = wait.until(
                            EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Weiter" or @aria-label="Next"]'))
                        )
                        next_button.click()
                        sleep(10)
                    except NoSuchElementException:
                        break  
        finally:
            self.driver.quit()
            self.csvfile.close()

    def scrape_page(self):
        sleep(10)
        
        sel = Selector(text=self.driver.page_source)
        
        houses = sel.css('div.g1qv1ctd')

        # Iterate over the houses and extract the required information
        for house in houses:
            if self.global_count >= 100:
                break
            if house.xpath('ancestor::div[contains(@class, "fj2orl9") and contains(@class, "atm_da_cbdd7d") and contains(@class, "dir") and contains(@class, "dir-ltr")]'):
                continue
            house_name = house.css('span.dir.dir-ltr::text').get()

            price_per_night = house.css('span._tyxjp1::text').get()
            if price_per_night is None:
                price_per_night = house.css('span._1y74zjx::text').get()

            
            self.writer.writerow([house_name, price_per_night])


    def parse(self, response):
        pass
