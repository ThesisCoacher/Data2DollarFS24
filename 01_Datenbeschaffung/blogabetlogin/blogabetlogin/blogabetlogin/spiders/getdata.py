# -*- coding: utf-8 -*-
import scrapy  # Import the Scrapy library for web scraping
from scrapy.selector import Selector  # Import Selector for parsing HTML content
from selenium import webdriver  # Import the Selenium WebDriver for controlling the browser
from selenium.webdriver.chrome.options import Options  # Import Options to customize the Chrome browser
from selenium.webdriver.common.by import By  # Import the By class to specify how to locate elements on the page
from webdriver_manager.chrome import ChromeDriverManager  # Automatically manage ChromeDriver binaries
from time import sleep  # Import sleep to pause the execution of the script

# Define a new Scrapy spider class
class GetdataSpider(scrapy.Spider):
    name = 'getdata'  # Unique name for the Spider
    allowed_domains = ['www.blogabet.com']  # Domain(s) the Spider is allowed to scrape
    start_urls = ['https://blogabet.com']  # Initial URL(s) to begin scraping from

    # The parse method processes the HTTP response and extracts data or follows links
    def parse(self, response):
        url = 'http://www.blogabet.com'  # Target URL to scrape
        
        # Set up Chrome browser options for WebDriver
        options = Options()
        # Uncomment below to run Chrome in headless mode (browser UI won't be displayed)
        # options.add_argument('--headless')

        # Initialize the WebDriver with the specified options
        self.driver = webdriver.Chrome(options=options)

        # Navigate to the specified URL with the WebDriver
        self.driver.get(url)

        # Pause execution for 5 seconds to allow page elements to load
        sleep(5)
        # Find and click the button with class 'btn-outline' (e.g., a login or continue button)
        self.driver.find_element(By.CLASS_NAME, 'btn-outline').click()
        
        # Pause for another 5 seconds
        sleep(5)
        # Find the username and password input fields by their HTML element IDs
        username = self.driver.find_element(By.ID, 'email')
        password = self.driver.find_element(By.ID, 'password')
        # Enter the username and password into the respective fields
        username.send_keys("lucasdautz@gmx.de")  # Replace with the actual username or email
        sleep(5)  # Wait for 5 seconds
        password.send_keys("IC2023,")  # Replace with the actual password
        
        # Find and click the login button with class 'btn-danger'
        self.driver.find_element(By.CLASS_NAME, 'btn-danger').click()
        # Wait for 5 seconds to ensure any post-login processes complete
        sleep(5)

        # Close the WebDriver session, effectively closing the browser window
        self.driver.close()
