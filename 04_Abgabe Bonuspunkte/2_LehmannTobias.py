from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

driver = webdriver.Firefox()

driver.implicitly_wait(3)

def parse_page(waittime):
    results = []
    content = driver.find_element(By.ID, "site-content")
    time.sleep(waittime)
    elements = driver.find_elements(By.CSS_SELECTOR, ".dir[data-testid]")
    for e in elements:
        try:
            id = e.get_dom_attribute("id")
            if id is not None and id.startswith("title_"):
                try:
                    parent = e.find_element(By.XPATH, "./..")
                    is_in_carousel = False
                    while parent is not None:
                        label = parent.get_dom_attribute("aria-labelledby")
                        if label == "carousel-label":
                            is_in_carousel = True
                            break
                        parent = parent.find_element(By.XPATH, "./..")

                    if is_in_carousel:
                        continue
                except:
                    pass
                parent = e.find_element(By.XPATH, "./..")
                name = parent.find_element(By.CSS_SELECTOR, "[data-testid=listing-card-name]").text
                price = ""
                siblings = parent.find_elements(By.CSS_SELECTOR, ".dir")
                
                for s in siblings:
                    if "CHF" in s.text:
                        price = s.text.split(" ")[0]
                        break

                results.append([name, price])
        except:
            pass

    return results

def parse_link(link):
    driver.get(link)
    print("Page 1")
    results = parse_page(5)

    for i in range(5):

        next_button = driver.find_element(By.CSS_SELECTOR, "[aria-label=Weiter]")
        next_button.click()

        print("Page " + str(i + 2))
        results = results + parse_page(3)

    results = results[:100]
    return results

r1 = parse_link("https://www.airbnb.ch/s/St.-Gallen--Schweiz/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-04-01&monthly_length=3&monthly_end_date=2024-07-01&price_filter_input_type=2&channel=EXPLORE&query=St.%20Gallen%2C%20Schweiz&date_picker_type=calendar&checkin=2024-06-27&checkout=2024-06-30&source=structured_search_input_header&search_type=user_map_move&price_filter_num_nights=3&place_id=ChIJVdgzdikem0cRFGH-HwhQIpo&ne_lat=47.507353470523604&ne_lng=9.479676323362185&sw_lat=47.32056408952527&sw_lng=9.223122283647996&zoom=10.975873511310896&zoom_level=10.975873511310896&search_by_map=true")
r2 = parse_link("https://www.airbnb.ch/s/St.-Gallen--Schweiz/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-04-01&monthly_length=3&monthly_end_date=2024-07-01&price_filter_input_type=2&channel=EXPLORE&query=St.%20Gallen%2C%20Schweiz&date_picker_type=calendar&checkin=2024-10-10&checkout=2024-10-20&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=3&zoom_level=10&place_id=ChIJVdgzdikem0cRFGH-HwhQIpo")

with open("results.csv", "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Price in CHF"])
    writer.writerows(r1)
    writer.writerow([])
    writer.writerows(r2)

