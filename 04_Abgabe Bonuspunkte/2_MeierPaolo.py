import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import csv
from time import sleep
import csv
from selenium.webdriver.common.by import By
from scrapy import Selector
from selenium import webdriver

class GetDataSpider(scrapy.Spider):
    name = 'getdata'
    allowed_domains = ['www.airbnb.com']
    start_urls = [
        'https://www.airbnb.ch/s/St.-Gallen--Schweiz/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-04-01&monthly_length=3&monthly_end_date=2024-07-01&price_filter_input_type=2&channel=EXPLORE&query=St.%20Gallen%2C%20Schweiz&place_id=ChIJVdgzdikem0cRFGH-HwhQIpo&date_picker_type=calendar&checkin=2024-06-27&checkout=2024-06-30&source=structured_search_input_header&search_type=filter_change&price_filter_num_nights=3'
    ]    

    def __init__(self):
        self.csvfile = open('titles.csv', 'w', newline='', encoding='utf-8')
        self.fieldnames = ['title', 'price', 'newprice']  # Add 'newprice' here
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)
        self.writer.writeheader()
    def parse(self, response):
        url = response.url
        options = Options()
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)
        self.scrape_page()

    def scrape_page(self):
        # Sleep/wait for 5 seconds to allow the page to load (especially useful for dynamic content)
        sleep(5)
        
        # Create a Selector object from the page source, allowing Scrapy to parse the HTML
        sel = Selector(text=self.driver.page_source)
        
        # Find the common parent div
        parent_divs = sel.css('div.g1qv1ctd.atm_u80d3j_1lqfgyr.atm_c8_o7aogt.atm_g3_8jkm7i.c1v0rf5q.atm_9s_11p5wf0.atm_cx_d64hb6.atm_dz_7esijk.atm_e0_1lo05zz.dir.dir-ltr')

        # Loop through each parent div
        for div in parent_divs:
            # Extract the title
            title = div.css('span[data-testid="listing-card-name"]::text').get()  # Use div instead of sel

            # Extract the price
            price = div.css('span._14y1gc span.a8jt5op.atm_3f_idpfg4.atm_7h_hxbz6r.atm_7i_ysn8ba.atm_e2_t94yts.atm_ks_zryt35.atm_l8_idpfg4.atm_mk_stnw88.atm_vv_1q9ccgz.atm_vy_t94yts.dir.dir-ltr::text').get()  # Use div instead of sel

            # Extract the new price
            newprice = div.css('span._1y74zjx::text').get()  # Use div instead of sel

            # Print the title, price, and new price
            print(title, price, newprice)

            # Write the title, price, and new price to the CSV file
            self.writer.writerow({'title': title, 'price': price, 'newprice': newprice})

        # Check if there is a next page
        next_button = self.driver.find_elements(By.CSS_SELECTOR, 'a[aria-label="Weiter"]')
        if next_button:
            next_button[0].click()
            # Recursively call scrape_page to scrape the next page
            self.scrape_page()


    def close(self, reason):
        # Close the CSV file when the spider is closed
        self.csvfile.close()
        # Close the driver
