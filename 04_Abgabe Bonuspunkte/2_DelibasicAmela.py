# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
from time import sleep

# Define a class for the web scraper
class GetDataSpider:
    def __init__(self):
        # Initialize the webdriver
        self.driver = webdriver.Chrome(options=Options())
        # URL to scrape
        self.url = 'https://www.airbnb.ch/s/St.-Gallen--Schweiz/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-04-01&monthly_length=3&monthly_end_date=2024-07-01&price_filter_input_type=2&channel=EXPLORE&query=St.%20Gallen%2C%20Schweiz&place_id=ChIJVdgzdikem0cRFGH-HwhQIpo&date_picker_type=calendar&source=structured_search_input_header&search_type=filter_change&price_filter_num_nights=5&checkin=2024-10-10&checkout=2024-10-20'
        # Counter to keep track of the number of items scraped
        self.counter = 0

    def scrape(self):
        # Load the webpage
        self.driver.get(self.url)
        # Wait for the page to load
        sleep(10)
        # Open a CSV file to write the scraped data
        with open('titles.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['title', 'price'])
            writer.writeheader()
            # Loop until 100 items are scraped
            while self.counter < 100:
                # Parse the page source with BeautifulSoup
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                # Scrape the current page
                self.scrape_page(soup, writer)
                # If less than 100 items are scraped, go to the next page
                if self.counter < 100:
                    next_button = self.driver.find_elements(By.CSS_SELECTOR, 'a[aria-label="Weiter"]')
                    if next_button:
                        next_button[0].click()
                        # Wait for the new page to load
                        sleep(5)

    def scrape_page(self, soup, writer):
        try:
            # Find the parent divs of the items
            parent_divs = soup.select('div.g1qv1ctd.atm_u80d3j_1lqfgyr.atm_c8_o7aogt.atm_g3_8jkm7i.c1v0rf5q.atm_9s_11p5wf0.atm_cx_d64hb6.atm_dz_7esijk.atm_e0_1lo05zz.dir.dir-ltr')

            # Loop through the parent divs
            for div in parent_divs:
                # Stop if 100 items are already scraped
                if self.counter >= 100:
                    break

                # Find the title and price elements and get their text
                title = div.select_one('div[data-testid="listing-card-subtitle"] span[data-testid="listing-card-name"]').text
                price = div.select_one('span._14y1gc span._tyxjp1').text

                # Print the title and price
                print(f"Title: {title}, Price: {price}")
                # Write the title and price to the CSV file
                writer.writerow({'title': title, 'price': price})
                # Increment the counter
                self.counter += 1
        except Exception as e:
            # Print any errors that occur
            print(f"An error occurred: {e}")

    def close(self):
        # Close the webdriver
        self.driver.quit()

# Create an instance of the scraper
spider = GetDataSpider()
# Start the scraper
spider.scrape()
# Close the scraper
spider.close()