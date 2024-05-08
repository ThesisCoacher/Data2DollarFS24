from wine import Wine
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

URL = 'https://www.vivino.com/DE/de/'
# Define a class to handle scraping from the Vivino website
class VivinoScraper:
  def __init__(self, browser) -> None:
    self.browser = browser
  
  def _getRating(self) -> float:
      try:
        # Wait until the rating element is visible on the page
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'average__number'))
        WebDriverWait(self.browser, 10).until(element_present)
        rating = self.browser.find_element(By.CLASS_NAME, 'average__number').text
        value = 0.00
        try:
          value = float(rating)
        except ValueError:
          print("Error converting to float")
          value = 0.00
      except Exception:
        print("Faulty wine")
        value = 0.00
      return value
  
  def _searchWine(self, title: str):
    self.browser.get(URL)
    # Find the search input field and submit a search query
    search_input = self.browser.find_element(By.CLASS_NAME, 'searchBar_searchInput__Jje-K')
    search_input.send_keys(title)
    search_input.submit()


  def _countRatings(self) -> int:
      # Wait for the element to be visible on the page
      try:
          WebDriverWait(self.browser, 10).until(
              EC.presence_of_element_located((By.CLASS_NAME, 'text-micro'))
          )
          # Extract the number of ratings from the element's text
          ratingCounter = self.browser.find_element(By.CLASS_NAME, 'text-micro').text
          counter = ratingCounter.split(' ')[0].strip()
          value = 0
          try:
              value = int(counter)
          except ValueError:
              print("Error converting to int")
              value = 0
      except Exception:
          print("Element with class 'text-micro' not found after waiting")
          value = 0

      return value

  def _getTastes(self):
    try:
      self.browser.find_element(By.CLASS_NAME, 'link-color-alt-grey').click()
      # Scroll down to ensure taste elements are visible
      self.browser.execute_script('scroll(0, 1000);')
      # Wait until taste indicators are visible
      element_present = EC.visibility_of_element_located((By.CLASS_NAME, 'indicatorBar__progress--3aXLX'))
      WebDriverWait(self.browser, 10).until(element_present)
      tasteRows = self.browser.find_elements(By.CLASS_NAME, 'indicatorBar__progress--3aXLX')
      print("Tastes found")
      tastes = []
      index_word = 'left: '
      time.sleep(10)
      for row in tasteRows:
        value = row.get_dom_attribute('style')
        index = value.index(index_word)
        start = index + len(index_word)
        tastes.append(value[start:-1])
      print(tastes)
      return tastes
    except Exception as e:
      print("Tastes not found!")



  def getWinesWithRating(self, wines: list[Wine], threshold: float) -> list[Wine]:
    results = []

    for wine in wines:
      self._searchWine(wine.name)
      rating = self._getRating()
      ratingCounter = self._countRatings()
      if rating >= threshold:
        wine.setRating(rating)
        wine.setRatingCounter(ratingCounter)
        tastes = self._getTastes()
        wine.setTastes(tastes)
        results.append(wine)

    return results