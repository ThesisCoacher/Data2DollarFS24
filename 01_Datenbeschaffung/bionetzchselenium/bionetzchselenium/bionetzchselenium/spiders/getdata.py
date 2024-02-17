# -*- coding: utf-8 -*-
import scrapy  # Importing the Scrapy library for web scraping
from scrapy.selector import Selector  # Import Selector for parsing HTML content
from selenium import webdriver  # Import webdriver for controlling the browser
from selenium.webdriver.chrome.options import Options  # Import Options to specify Chrome settings
from selenium.webdriver.common.by import By  # Import the By class for locating elements
from webdriver_manager.chrome import ChromeDriverManager  # Import ChromeDriverManager to manage the ChromeDriver binary
from time import sleep  # Import sleep to pause execution for a specified amount of time

# Define a new Scrapy spider class
class GetdataSpider(scrapy.Spider):
    name = 'getdata'  # Name of the spider
    allowed_domains = ['www.bionetz.ch']  # List of domains the spider is allowed to scrape
    start_urls = ['http://www.bionetz.ch']  # List of starting URLs for the spider

    # The parse method is called with the response object when the spider starts scraping
    def parse(self, response):
        url = 'https://bionetz.ch/adressen/detailhandel/bio-fachgeschaefte.html'  # The URL to scrape

        # Initialize Chrome options for the WebDriver
        options = Options()
        # Uncomment the next line to run Chrome in headless mode (without opening a UI window)
        # options.add_argument('--headless')

        # Initialize the WebDriver with the specified options
        self.driver = webdriver.Chrome(options=options)

        # Open the specified URL in the browser
        self.driver.get(url)

        # Loop as long as there are elements with the title "Weiter" (indicating a "Next" button)
        while self.driver.find_elements(By.XPATH, '//*[@title="Weiter"]'):
            # Create a Selector with the current page source (HTML content)
            sel = Selector(text=self.driver.page_source)
            # Find all elements with the class "listing-summary col-xs-12 col-sm-6"
            single_etikette = sel.xpath('//*[@class="listing-summary col-xs-12 col-sm-6"]')
            # Loop through each element found
            for etikette in single_etikette:
                # Extract the name of the company using the itemprop attribute
                unternehmens_name = etikette.xpath('.//*[@itemprop="name"]/text()').extract()
                # Extract the first address found within the element
                unternehmens_adresse = etikette.xpath('.//*[@class="address"]/text()').extract_first()
                # Yield (return) a dictionary with the company name and address
                yield {'Name': unternehmens_name, 'Adresse': unternehmens_adresse}

            # Find the footer element by its ID to scroll into view (necessary for loading the "Next" button)
            element = self.driver.find_element(By.ID, 'footer1')
            # Execute JavaScript to scroll the footer element into view
            self.driver.execute_script("arguments[0].scrollIntoView(0, document.documentElement.scrollHeight-5);", element)
            sleep(3)  # Wait for 3 seconds to ensure the page has loaded
            # Find the "Next" button by its XPath and click it to load the next page of results
            self.driver.find_element(By.XPATH, '//*[@title="Weiter"]').click()

        # Close the WebDriver session and the browser window after scraping is complete
        self.driver.close()
