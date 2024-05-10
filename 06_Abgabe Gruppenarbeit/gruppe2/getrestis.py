import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import csv
import time
import random  
from webdriver_manager.chrome import ChromeDriverManager

class GetrestisSpider(scrapy.Spider):
    name = 'getrestis'
    allowed_domains = ['www.tripadvisor.ch']
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
        self.start_urls = self.load_start_urls()  # Load URLs from the Excel file

    def load_start_urls(self):
        # Load the Excel file
        file_path = 'Tripadvisor_all_restaurants.xlsx'
        data = pd.read_excel(file_path)
        return data['Full_URL'].tolist()  # Assuming the full URLs are stored in the 'Full_URL' column

    def start_requests(self):
        for url in self.start_urls:
            self.driver.get(url)
            time.sleep(random.uniform(5, 13))  # Randomized wait to simulate human behavior
            yield self.scrape_details()  # Use yield to adhere to Scrapy's generator pattern if needed
    def scrape_details(self):
        sel = Selector(text=self.driver.page_source)
        mentioned_kitchens = []

        kitchens = [
            "Europäisch", "Schweizerisch", "Italienisch", "Mediterran",
            "Mitteleuropäisch", "Asiatisch", "Pizza", "Café",
            "Bar", "International", "Pub", "Gesund",
            "Thailändisch", "Fast Food", "Chinesisch", "Amerikanisch",
            "Japanisch", "Orientalisch", "Sushi", "Grillspezialitäten",
            "Indisch", "Speiselokal", "Türkisch", "Französisch",
            "Meeresfrüchte", "Zeitgenössisch", "Spanisch", "Vietnamesisch",
            "Steakhaus", "Barbecue", "Weinbars & Weinstuben", "Fusion",
            "Street Food", "Mexikanisch", "Deutsch", "Libanesisch",
            "Süditalienisch", "Suppen", "Griechisch", "Südamerikanisch",
            "Lateinamerikanisch", "Deli", "Österreichisch", "Restaurantbars",
            "Neapolitanisch", "Kampanisch", "Tibetisch", "Srilankisch",
            "Toskanisch", "Gastropub", "Einheimisch", "Afrikanisch",
            "Portugiesisch", "Japanische Fusion-Küche", "Arabisch",
            "Koreanisch", "Argentinisch", "Gasthausbrauerei", "Hawaiianisch",
            "Britisch", "Schanghai", "Äthiopisch", "Norditalienisch",
            "Irisch", "Peruanisch", "Szechuan", "Pakistanisch",
            "Hongkong", "Persisch", "Marokkanisch", "Malaysisch",
            "Osteuropäisch", "Taiwanesisch", "Sizilianisch", "Karibisch",
            "South-Western", "Albanisch", "Chilenisch", "Ungarisch",
            "Schwedisch", "Skandinavisch", "Dänisch", "Bangladeschisch",
            "Israelisch", "Indonesisch", "Polynesisch", "Chinesisch (Imperial)",
            "Kroatisch", "Mongolisch", "Belgisch", "Philippinisch",
            "Indianisch", "Nepalesisch", "Norwegisch", "Afghanisch"
            ]
        
        for kitchen in kitchens:
            # Check if the kitchen type is mentioned in the page source
            if sel.css(f'span.biGQs._P.pZUbB.hmDzD:contains("{kitchen}")::text').get():
                mentioned_kitchens.append(kitchen)

        # Join all found kitchens into a single string
        kitchens_string = ", ".join(mentioned_kitchens)

        # Continue with other details extraction and store them
        restaurant_name = sel.css('h1.biGQs._P.egaXP.rRtyp::text').getall()
        reviews_count = sel.css('span.GPKsO::text').getall()
        price_range = sel.css('span.biGQs._P.pZUbB.hmDzD:contains("€")::text').getall()
        address = sel.css('button.UikNM._G.B-._S._W._T.c.G_.wSSLS.TXrCr div.biGQs._P.pZUbB.hmDzD::text').get()
        rating = sel.css('title:contains("Punkten")::text').re_first(r'\d+\.\d+')

        # Append to file each time or collect to a list and write at end depending on your preference
        with open('Restaurantinfo7.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([restaurant_name, reviews_count, price_range, kitchens_string, address, rating])

    def closed(self, reason):
        self.driver.quit()  # Close the driver when spider is closed
