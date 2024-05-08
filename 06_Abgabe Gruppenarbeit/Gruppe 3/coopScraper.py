from wine import Wine
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

class CoopScraper:
    def __init__(self, browser) -> None:
        self.browser = browser
    
    def _getWines(self) -> list[Wine]:
        products = self._getProducts()
        results = []
        # Loop through each product and extract details
        for item in products:
            title = self._getTitle(item)
            
            price = self._getPrice(item)

            country, year = self._getCountryYear(item)

            wine = Wine(title, country, "", year, price)
            results.append(wine)

        return results
    
    def _getCountryYear(self, item):
        country_and_year = item.find_element(By.CLASS_NAME, 'productTile__productMeta-value-item').text
        INDEX_COUNTRY = 0
        INDEX_YEAR = 1
        splitted_words = country_and_year.split(',')
        country = splitted_words[INDEX_COUNTRY].strip()

        if len(splitted_words) > 1:
            year = splitted_words[INDEX_YEAR].strip()
        else:
            year = ''

        return [country, year]

    def _getPrice(self, item):
        return item.find_element(By.CLASS_NAME, 'productTile__price-value-lead-price').text

    def _getTitle(self, item):
        return item.find_element(By.CLASS_NAME, 'productTile-details__name-value').text

    def _getProducts(self):
        return self.browser.find_elements(By.CLASS_NAME, 'productTile__wrapper')
    
    def getRedWines(self) -> list[Wine]:
        self.browser.get('https://www.coop.ch/de/weine/alle-weine/rotweine/c/m_0223')
        return self._getWines()

    def getWhiteWines(self) -> list[Wine]:
        self.browser.get('https://www.coop.ch/de/weine/alle-weine/weissweine/c/m_0235')
        return self._getWines()
    
    def getAuctionWines(self) -> list[Wine]:
        self.browser.get('https://www.coop.ch/de/weine/aktionen/c/SPECIAL_OFFERS_WINE')
        return self._getWines()
    
    def hastNextPage(self):
        # Check if the next page button is clickable
        try:
            WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'pagination__next')))
            return True
        except:
            return False

    def nextPage(self):
        next_button = self.browser.find_element(By.CLASS_NAME, 'pagination__next')
        next_button.click()
        # Wait until new products are loaded
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'productTile__wrapper'))
        WebDriverWait(self.browser, 10).until(element_present)          
        return self._getWines()