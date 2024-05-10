import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
import time
import random  
from webdriver_manager.chrome import ChromeDriverManager

class GetDataSpider(scrapy.Spider):
    name = 'getdata'
    allowed_domains = ['www.tripadvisor.ch']
    start_urls = ['http://api.scraperapi.com?api_key=e505ae2b312baadea71783d34cc4b2a5&url=https://www.tripadvisor.ch/FindRestaurants?geo=188113&offset=0&establishmentTypes=10591&minimumTravelerRating=TRAVELER_RATING_LOW&broadened=true']
    handle_httpstatus_list = list(range(400, 600))

    def __init__(self):
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-webrtc")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def parse(self, response):
        base_url = 'http://api.scraperapi.com?api_key=e505ae2b312baadea71783d34cc4b2a5&url=https://www.tripadvisor.ch/FindRestaurants?geo=188113&offset={offset}&establishmentTypes=10591&minimumTravelerRating=TRAVELER_RATING_LOW&broadened=true'
        for offset in range(0, 2490, 30):  # Handling pagination through URL modification
            full_url = base_url.format(offset=offset)
            self.driver.get(full_url)
            time.sleep(random.uniform(5, 15))  # Randomized wait to simulate human behavior
            self.scrape_page()

    def scrape_page(self):
        sel = Selector(text=self.driver.page_source)
        restaurant_entries = sel.css('div.qeraN._T.qMONr.iOIte.iJfMg.ndRxi.CpYrl.rcibp.FKwyn')
        restaurants_data = []

        for entry in restaurant_entries:
            restaurant_name = entry.css('a.BMQDV._F.Gv.wSSLS.SwZTJ.FGwzt.ukgoS::text').getall()
            restaurant_url = entry.css('a.BMQDV._F.Gv.wSSLS.SwZTJ.FGwzt.ukgoS::attr(href)').get()
            if restaurant_url:
                restaurant_url = f"https://www.tripadvisor.ch{restaurant_url}"
            restaurants_data.append((restaurant_name, restaurant_url))

        with open('Restaurants.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for data in restaurants_data:
                writer.writerow(data)