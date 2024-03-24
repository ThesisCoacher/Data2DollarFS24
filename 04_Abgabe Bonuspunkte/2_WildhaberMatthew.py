scrapy_startproject A2.py from scrapy import Spider, Request

from selenium import webdriver
from scrapy.selector import Selector
from time import sleep

class AirbnbSpider(Spider):
    name = 'airbnb'
    allowed_domains = ['airbnb.com']
    start_urls = ['http://airbnb.com/']

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        self.driver.get(response.url)

        # Input dates
        self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[3]/div[1]/div[1]/div/div/header/div/div[2]/div[1]/div/span[2]/button[2]/div').send_keys('06/27/2024')
        self.driver.find_element_by_xpath('//input[@id="endDate"]').send_keys('06/30/2024')

        # Click search button
        self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[3]/div[1]/div[1]/div/div/header/div/div[2]/div[1]/div/span[2]/button[3]/div[2]/svg').click()

        # Wait for the page to load
        sleep(3)

        # Extract data
        listings = Selector(text=self.driver.page_source).xpath('//*[@id="site-content"]/div/div[2]/div')

        for listing in listings:
            name = listing.xpath('/html/body/div[5]/div/div/div[1]/div/div[3]/div[2]/main/div[2]/div/div[2]/div/div/div/div/div[1]/div[3]/div/div[2]/div/div/div/div/div/div[2]/div[5]/div[2]/div/div/span[2]').get()
            price = listing.xpath('//div[@data-testid="listing-card-subtitle"]/span[@data-testid="listing-card-name"]/text()').get()
            yield {'name': name, 'price': price}

        # Go to the next page
        next_page = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[3]/div[2]/main/div[2]/div/div[3]/div/div/div/nav/div/a[4]')

        if next_page:
            next_page.click()
            sleep(3)
            yield Request(url=self.driver.current_url, callback=self.parse)

    def closed(self, reason):
        self.driver.close()