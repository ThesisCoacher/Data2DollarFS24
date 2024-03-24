from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json



waitingtime=6 # Time used for loading the page completely
driver = webdriver.Chrome()
#driver = webdriver.Firefox()

def scrapeinfo_from_page(driver,scrapecounter,listing_all,Timeperiod):
    elements = driver.find_elements(By.XPATH, './/div[contains(@class, "lxq01kf")]')
    for element in elements:
        if scrapecounter<100:
            listing = {}  # Dictionary to store the current listing's data
            print("----------------")
            #Looking for Apartment-Title
            #subelements = element.find_elements(By.XPATH, './/div[@data-testid="listing-card-title"]')
            cardname_list = element.find_elements(By.XPATH, './/span[@data-testid="listing-card-name"]')
            for cardname_element in cardname_list:
                print(cardname_element.text)  # Or any other attribute you wish to extract
                listing['Apartment-Title'] = cardname_element.text  # Assume one title per listing for simplicity
                #if price is reduced, class _1y74zjx is used instead of _tyxjp1
            price_elements = element.find_elements(By.XPATH, './/span[contains(@class, "_tyxjp1") or contains(@class, "_1y74zjx")]')
            for price_element in price_elements:
                print(price_element.text)  # This should print something like "77 CHF"
                listing['pricepernight'] = price_element.text  # Assume one price per listing for simplicity
                # maybe cutoff " CHF"  ant typecast to number
            listing['timeperiod'] = Timeperiod  # Saving Timeperiod

            # Add the listing to the list of all listings
            listing_all.append(listing)

            scrapecounter+=1
        else:
            break

    return scrapecounter, listing_all


#START MAIN Routing

scrapecounter=0
full_list = []  # Initialize the list to store listings data



Timeperiod="27.-30. June 2024"
url='https://www.airbnb.ch/s/St.-Gallen--Schweiz/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-04-01&monthly_length=3&monthly_end_date=2024-07-01&price_filter_input_type=2&channel=EXPLORE&query=St.%20Gallen%2C%20Schweiz&place_id=ChIJoR85ryDimkcRmxnF_e9vd4A&date_picker_type=calendar&source=structured_search_input_header&search_type=filter_change&price_filter_num_nights=10&checkin=2024-06-27&checkout=2024-06-30'
driver.get(url)
time.sleep(waitingtime)



scrapecounter, full_list = scrapeinfo_from_page(driver, scrapecounter, full_list,Timeperiod)
        
print("page1 done")
while scrapecounter<100:    
    next_page_button = driver.find_element(By.XPATH, '//a[@aria-label="Weiter"]')
    #print(next_page_button.get_attribute('href'))
    print("loading next page")
    print("---------------------------")
    next_page_button.click()
    print("---------------------------")

    
    # Wait for a specific element on the next page to be visible before continuing
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, './/div[contains(@class, "lxq01kf")]'))
    )
    
    print("---------------------------")
    time.sleep(waitingtime)
    # alterlative: wait for an element at the end of the page to be loaded: WebDriverWait

    
    scrapecounter,full_list =scrapeinfo_from_page(driver,scrapecounter,full_list,Timeperiod)

    print("-------------12345--------------")

    
#Loading second Timeperiod
Timeperiod="10.-20. October 2024"

url='https://www.airbnb.ch/s/St.-Gallen--Schweiz/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-04-01&monthly_length=3&monthly_end_date=2024-07-01&price_filter_input_type=2&channel=EXPLORE&query=St.%20Gallen%2C%20Schweiz&place_id=ChIJoR85ryDimkcRmxnF_e9vd4A&date_picker_type=calendar&source=structured_search_input_header&search_type=filter_change&price_filter_num_nights=3&checkin=2024-10-10&checkout=2024-10-20'
driver.get(url)
time.sleep(waitingtime) 


scrapecounter=0
scrapecounter, full_list = scrapeinfo_from_page(driver, scrapecounter, full_list,Timeperiod)
while scrapecounter<100:    
    next_page_button = driver.find_element(By.XPATH, '//a[@aria-label="Weiter"]')
    #print(next_page_button.get_attribute('href'))
    next_page_button.click()
    
    # Wait for a specific element on the next page to be visible before continuing
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, './/div[contains(@class, "lxq01kf")]'))
    )
    time.sleep(waitingtime)
    scrapecounter,full_list =scrapeinfo_from_page(driver,scrapecounter,full_list,Timeperiod)




## Write to JSON after completing scraping
with open('2_ConradinWyss.json', 'w', encoding='utf-8') as f:
    json.dump(full_list, f, ensure_ascii=False, indent=4)