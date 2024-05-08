# Import necessary classes and modules
from coopScraper import CoopScraper
from vivinoScraper import VivinoScraper
from wine import Wine
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import logging
import csv
import time

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
# Set Firefox options for the browser
opts = Options()
opts.arguments.append('--ignore-certificate-errors')  # Ignore certificate errors
opts.arguments.append('--headless')  # Run browser in headless mode
opts.set_preference('network.http.use-cache', False) # Disable cache to ensure fresh data is loaded
opts.set_preference('permissions.default.image', 2)  # Disable loading images to speed up the process

# assert opts.headless  # Operating in headless mode
browser = Firefox(options=opts)

# Define a function to write wine data to a CSV file
def write_results_to_csv(wines, filename="wine_ratings_red_2.csv", mode='a'):
    with open(filename, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write a header row if the mode is 'write'
        if (mode == 'w'):
            # Write the header row
            writer.writerow(['Name', 'Country', 'Year', 'Price', 'Rating', 'Rating Counter', 'Tastes'])

        # Write each wine's information as a row in the CSV
        for wine in wines:
            writer.writerow([wine.name, wine.country, wine.year, wine.price, wine.rating, wine.ratingCounter, str(wine.tastes)])

# Define a function to process and save wine data
def saveWines(browser, ratingScraper: VivinoScraper, wines: list[Wine], mode='a'):
    current_url = browser.current_url
    logging.info("Finished scraping wines on page")
    rated_wines = ratingScraper.getWinesWithRating(wines,1)
    logging.info("Finished scraping ratings")
    write_results_to_csv(rated_wines, mode=mode)
    logging.info("Saved wines")
    browser.get(current_url)

scraper = CoopScraper(browser)
ratingScraper = VivinoScraper(browser)
pageCounter = 1


try:
    wines = scraper.getRedWines()
    saveWines(browser, ratingScraper, wines, mode='w')
    print(pageCounter)

    while(scraper.hastNextPage()):
        wines = scraper.nextPage()
        saveWines(browser, ratingScraper, wines)
        pageCounter += 1
        print(pageCounter)
except Exception as e:
    print(e)
finally:
    print("done")

# for rating in ratings:
#     print(rating)
browser.quit()
quit()