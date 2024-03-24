# Import the necessary libraries from Scrapy and Selenium
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
import csv

# Define a new Spider class that inherits from scrapy.Spider
class GetDataSpider(scrapy.Spider):
    # Name your spider 'getdata'
    name = 'getdata'
    # Define the domain(s) that the spider is allowed to scrape
    allowed_domains = ['www.airbnb.com']
    # List the URL(s) the spider will start from
    start_urls = ['https://www.airbnb.ch/s/St.-Gallen--Schweiz/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-04-01&monthly_length=3&monthly_end_date=2024-07-01&price_filter_input_type=2&channel=EXPLORE&query=St.%20Gallen%2C%20Schweiz&place_id=ChIJoR85ryDimkcRmxnF_e9vd4A&date_picker_type=calendar&checkin=2024-06-27&checkout=2024-06-30&source=structured_search_input_header&search_type=autocomplete_click',
                  'https://www.airbnb.ch/s/St.-Gallen--Schweiz/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_end_date=2024-07-01&price_filter_input_type=2&channel=EXPLORE&query=St.%20Gallen%2C%20Schweiz&place_id=ChIJoR85ryDimkcRmxnF_e9vd4A&date_picker_type=calendar&source=structured_search_input_header&search_type=filter_change&price_filter_num_nights=3&checkin=2024-10-10&checkout=2024-10-20']
    
    # Create a new instance of Chrome WebDriver with the specified options
    def __init__(self):
        options = Options()
        options.headless = True  # Run Chrome in headless mode.
        self.driver = webdriver.Chrome(options=options)
        
    
    # The parse method is the callback function that gets called on each URL in start_urls
    def parse(self, response):
        # Reset counters for each URL processed.
        self.counter = 0
        
        self.current_url = response.url  # Keep track of the current URL being processed.
        self.driver.get(self.current_url)
        self.scrape_page()

    # Define the method for scraping the page
    def scrape_page(self):
        # Sleep/wait for 5 seconds to allow the page to load (especially useful for dynamic content)
        sleep(5)
        
        # Create a Selector object from the page source, allowing Scrapy to parse the HTML
        sel = Selector(text=self.driver.page_source)
        
        # Extract houses and prices from the page
        houses = sel.css('span[data-testid="listing-card-name"]::text').getall()
        prices = sel.css('span._tyxjp1::text').getall() or sel.css('span._1y74zjx::text').getall()

        # Proceed if data was extracted
        if houses and prices:
            # Open CSV file for appending data
            with open('2_MorozKatja.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Write headers if this is the first page
                if self.counter == 0:
                    writer.writerow(["House", "Price"])
                # Write extracted data to CSV
                for house, price in zip(houses, prices):
                    if self.counter < 100:
                        writer.writerow([house, price])
                        self.counter += 1
        else:
            print("No data extracted. Check selectors.")
    
        # Try to find and click the next page button using WebDriverWait and expected_conditions to wait until the element is clickable
        if self.counter < 100:
            try:
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="Weiter"]'))
                )
                # Click the next page button
                next_button.click()
                # Recursively call scrape_page to scrape the next page
                self.scrape_page()
            
            # If an exception occurs (e.g., the button is not found), quit the WebDriver
            except (NoSuchElementException, TimeoutException) as e:
                # Print error message and quit the driver if navigation fails
                print(f"Navigation error: {e}")
                self.driver.quit()
        elif self.counter >= 100:
            # Reset the counters if needed or handle completion of current URL.
            print(f"Completed scraping 100 listings for {self.current_url}")