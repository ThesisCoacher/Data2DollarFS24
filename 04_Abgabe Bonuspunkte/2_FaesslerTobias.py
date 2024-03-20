import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GetDataSpider(scrapy.Spider):
    name = 'getdata'
    allowed_domains = ['www.airbnb.com']
    start_urls = ['https://www.airbnb.ch/s/St.-Gallen--Schweiz/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-04-01&monthly_length=3&monthly_end_date=2024-07-01&price_filter_input_type=2&channel=EXPLORE&query=St.%20Gallen%2C%20Schweiz&place_id=ChIJoR85ryDimkcRmxnF_e9vd4A&date_picker_type=calendar&checkin=2024-10-10&checkout=2024-10-20&source=structured_search_input_header&search_type=filter_change&price_filter_num_nights=3']

    def __init__(self):
        self.page_count = 0  # Counter for the number of pages scraped
        self.titles = []  # Initialize titles list as an instance variable
        self.prices = []  # Initialize prices list as an instance variable

    def parse(self, response):
        options = Options()
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(response.url)
        self.scrape_page()

    def scrape_page(self):
        if self.page_count < 6:
            self.page_count += 1
            sleep(5)
            
            sel = Selector(text=self.driver.page_source)

            for block in sel.css('div[data-testid="listing-card-title"] + div[data-testid="listing-card-subtitle"]'):
                title = block.css('*::text').get()
                if title:
                    self.titles.append(title.strip())  # Append to the instance variable

            for price_block in sel.css('._1jo4hgw'):
                price = price_block.xpath('following-sibling::span[1]/text()').get()
                if price:
                    self.prices.append(price.strip())  # Append to the instance variable

            assert len(self.titles) == len(self.prices), "The lengths of titles and prices do not match."

            for title in self.titles:
                print(title)
            for price in self.prices:
                print(price)

            if self.page_count < 6:
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="Weiter"]')))
                next_button.click()
                sleep(5)
                self.scrape_page()
            else:
                self.driver.quit()
                if self.titles and self.prices:
                    print("Saving data to CSV...")
                    self.save_to_csv()
    
    def save_to_csv(self):
        # Define the file path
        file_path = 'C:\\Users\\tobia\\OneDrive\\Master MBI\\Data2Dollar\\airbnb_inclass\\listings.csv'
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Price'])
            for title, price in zip(self.titles, self.prices):
                writer.writerow([title, price])
        
        print(f"Data saved to {file_path}")