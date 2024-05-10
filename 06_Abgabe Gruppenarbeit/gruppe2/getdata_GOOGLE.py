#Bibliotheken
import csv
import scrapy
import time
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
import random
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class GetDataSpider(scrapy.Spider):
    name = "getdata"
    allowed_domains = ['www.google.com']
    start_urls = [
        'https://www.google.com/search?sca_esv=dc1b946dcae22bbc&sca_upv=1&tbs=lf:1,lf_ui:9&tbm=lcl&sxsrf=ADLYWILIgqiFfGZwlodaokAvBKGEmm9mkw:1715279819135&q=restaurant+z%C3%BCrich+kreis+1&rflfq=1&num=10&sa=X&ved=2ahUKEwi5_7yim4GGAxUc7bsIHeX4DxcQjGp6BAglEAE&biw=1920&bih=1065&dpr=1#rlfi=hd:;si:;mv:[[47.3776691,8.545093699999999],[47.367321499999996,8.536996]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:9',
        'https://www.google.com/search?q=restaurant+z%C3%BCrich+kreis+2&sca_esv=dc1b946dcae22bbc&sca_upv=1&biw=1920&bih=1065&tbm=lcl&sxsrf=ADLYWIKS-wFdI4Qv9Ru3Kt7ojQEMAF0mpA%3A1715279822477&ei=zhc9ZrvUHJON9u8P87GbkAc&ved=0ahUKEwi784ikm4GGAxWThv0HHfPYBnIQ4dUDCAk&uact=5&oq=restaurant+z%C3%BCrich+kreis+2&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhpyZXN0YXVyYW50IHrDvHJpY2gga3JlaXMgMjIEECMYJzIGEAAYFhgeMggQABiABBiiBDIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiiBBiJBUiwFVDUBFiOEHAAeACQAQCYAW6gAZsCqgEDMi4xuAEDyAEA-AEBmAIDoAK7AsICBRAAGIAEmAMAiAYBkgcDMS4yoAfnGA&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[47.3685696,8.5414925],[47.3366796,8.5234325]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:9',
        'https://www.google.com/search?q=restaurant+z%C3%BCrich+kreis+3&sca_esv=dc1b946dcae22bbc&sca_upv=1&biw=1920&bih=1065&tbm=lcl&sxsrf=ADLYWIJFvHpPH-VNmzpV0TF1mJ9d2sIHFA%3A1715279840021&ei=4Bc9ZnDLivbvD7K0tYAK&ved=0ahUKEwjw8Lasm4GGAxVLhf0HHTJaDaAQ4dUDCAk&uact=5&oq=restaurant+z%C3%BCrich+kreis+3&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhpyZXN0YXVyYW50IHrDvHJpY2gga3JlaXMgMzIEECMYJzIGEAAYFhgeMgYQABgWGB4yCBAAGKIEGIkFMggQABiABBiiBEjIH1C9BVjMHHABeACQAQCYAWOgAYkCqgEBM7gBA8gBAPgBAfgBApgCBKACqgLCAgUQABiABJgDAIgGAZIHAzIuMqAHshI&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[47.3766069,8.526444999999999],[47.3634409,8.500197]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:9',
        'https://www.google.com/search?q=restaurant+z%C3%BCrich+kreis+4&sca_esv=dc1b946dcae22bbc&sca_upv=1&biw=1920&bih=1065&tbm=lcl&sxsrf=ADLYWIKcR4eAajvjym5Kk9C0H5HvUJFlrA%3A1715279909966&ei=JRg9ZqKyOtOA9u8P2bau-As&ved=0ahUKEwji2OTNm4GGAxVTgP0HHVmbC78Q4dUDCAk&uact=5&oq=restaurant+z%C3%BCrich+kreis+4&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhpyZXN0YXVyYW50IHrDvHJpY2gga3JlaXMgNDIEECMYJzIFEAAYgAQyBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeSIINUP0EWL4KcAB4AJABAJgBY6ABkgKqAQEzuAEDyAEA-AEBmAIDoAKzAsICCBAAGKIEGIkFwgIIEAAYgAQYogSYAwCIBgGSBwMxLjKgB6YX&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[47.381356100000005,8.5356568],[47.3710987,8.520306699999999]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:9',
        'https://www.google.com/search?q=restaurant+z%C3%BCrich+kreis+5&sca_esv=dc1b946dcae22bbc&sca_upv=1&biw=1920&bih=1065&tbm=lcl&sxsrf=ADLYWIJTc0--mp8onasTCzcvPjdRL2PUkQ%3A1715279930906&ei=Ohg9ZqzwNuuA9u8P0tO82AE&ved=0ahUKEwis9eLXm4GGAxVrgP0HHdIpDxsQ4dUDCAk&uact=5&oq=restaurant+z%C3%BCrich+kreis+5&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhpyZXN0YXVyYW50IHrDvHJpY2gga3JlaXMgNTIEECMYJzIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHkjgDFChBlixCnAAeACQAQCYAWagAY4CqgEDMi4xuAEDyAEA-AEBmAIDoAKlAsICBRAAGIAEmAMAiAYBkgcDMS4yoAeiGQ&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[47.3944857,8.5301114],[47.3833073,8.508627299999999]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:9',
        'https://www.google.com/search?q=restaurant+z%C3%BCrich+kreis+6&sca_esv=dc1b946dcae22bbc&sca_upv=1&biw=1920&bih=1065&tbm=lcl&sxsrf=ADLYWIKu5Iw7WDvmewmR_01FJv7i3wMbgw%3A1715279944088&ei=SBg9Zt3wBNmP9u8P_qm7uAI&ved=0ahUKEwjdtIfem4GGAxXZh_0HHf7UDicQ4dUDCAk&uact=5&oq=restaurant+z%C3%BCrich+kreis+6&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhpyZXN0YXVyYW50IHrDvHJpY2gga3JlaXMgNjIEECMYJzIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIIEAAYgAQYogQyCBAAGKIEGIkFSKoPUPwEWOAJcAB4AJABAJgBa6ABigKqAQMyLjG4AQPIAQD4AQGYAgOgAqMCwgIFEAAYgASYAwCIBgGSBwMyLjGgB-QW&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[47.400587099999996,8.5488705],[47.37619610000001,8.539106]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:9',
        'https://www.google.com/search?q=restaurant+z%C3%BCrich+kreis+7&sca_esv=dc1b946dcae22bbc&sca_upv=1&biw=1920&bih=1065&tbm=lcl&sxsrf=ADLYWILWW2UWsNaQ05xHFXpLjbRcTEJmag%3A1715279956284&ei=VBg9ZtaTEOOP9u8P-96msAM&ved=0ahUKEwjWje_jm4GGAxXjh_0HHXuvCTYQ4dUDCAk&uact=5&oq=restaurant+z%C3%BCrich+kreis+7&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhpyZXN0YXVyYW50IHrDvHJpY2gga3JlaXMgNzIEECMYJzICECYyAhAmMgIQJjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBEjMC1DXBVjXCXAAeACQAQCYAXugAa8CqgEDMS4yuAEDyAEA-AEBmAIDoALFAsICBhAAGBYYHsICBRAAGIAEmAMAiAYBkgcDMS4yoAfGFQ&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[47.3886804,8.590422199999999],[47.358881,8.547192299999999]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:9',
        'https://www.google.com/search?q=restaurant+z%C3%BCrich+kreis+8&sca_esv=dc1b946dcae22bbc&sca_upv=1&biw=1920&bih=1065&tbm=lcl&sxsrf=ADLYWIL_JHGLjuF6KpngP5PZk10wlkvLrA%3A1715279969988&ei=YRg9ZpnqO_397_UPip6K0Ag&ved=0ahUKEwjZnrTqm4GGAxX9_rsIHQqPAooQ4dUDCAk&uact=5&oq=restaurant+z%C3%BCrich+kreis+8&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhpyZXN0YXVyYW50IHrDvHJpY2gga3JlaXMgODIEECMYJzICECYyCBAAGKIEGIkFMggQABiABBiiBDIIEAAYgAQYogQyCBAAGIAEGKIESMgVUJ0FWIoJcAB4AJABAJgBWKAB-AGqAQEzuAEDyAEA-AEBmAIDoAKQAsICBRAAGIAEwgIGEAAYFhgemAMAiAYBkgcBM6AHkhQ&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[47.3669825,8.5666808],[47.3478772,8.5459547]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:9',
        'https://www.google.com/search?q=restaurant+z%C3%BCrich+kreis+9&sca_esv=dc1b946dcae22bbc&sca_upv=1&biw=1920&bih=1065&tbm=lcl&sxsrf=ADLYWIJwaPLXSTeRxD2yEIwYP_77Mjrsag%3A1715279982139&ei=bhg9ZsGECPD-7_UPh-6S4AM&ved=0ahUKEwjB85nwm4GGAxVw_7sIHQe3BDwQ4dUDCAk&uact=5&oq=restaurant+z%C3%BCrich+kreis+9&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhpyZXN0YXVyYW50IHrDvHJpY2gga3JlaXMgOTIEECMYJzIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRI6AtQ8wVY5wlwAHgAkAEAmAH_BaABpgeqAQcxLjEuNi0xuAEDyAEA-AEBmAICoAK3AcICBRAAGIAEwgIGEAAYFhgemAMAiAYBkgcDMS4xoAecEw&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[47.394470999999996,8.503078499999999],[47.3653142,8.4726045]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:9',
        'https://www.google.com/search?q=restaurant+z%C3%BCrich+kreis+10&sca_esv=dc1b946dcae22bbc&sca_upv=1&biw=1920&bih=1065&tbm=lcl&sxsrf=ADLYWIK8IntvyLExbKs1UsLFuLXheysjfA%3A1715279997895&ei=fRg9ZsaSNtKI9u8Phuu72AM&ved=0ahUKEwiGxdv3m4GGAxVShP0HHYb1DjsQ4dUDCAk&uact=5&oq=restaurant+z%C3%BCrich+kreis+10&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhtyZXN0YXVyYW50IHrDvHJpY2gga3JlaXMgMTAyBBAjGCcyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogQyCBAAGKIEGIkFSPYNUL4FWLYLcAB4AJABAJgBtgKgAekEqgEHMi4xLjAuMbgBA8gBAPgBAZgCBKACgwXCAgUQABiABMICBhAAGBYYHpgDAIgGAZIHBzIuMS4wLjGgB-4c&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[47.4198549,8.5491201],[47.3842438,8.476295]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:9',
        'https://www.google.com/search?q=restaurant+z%C3%BCrich+kreis+11&sca_esv=dc1b946dcae22bbc&sca_upv=1&biw=1920&bih=1065&tbm=lcl&sxsrf=ADLYWIKXxR2tRfpZ_LoT67FD_6bkb6ekfg%3A1715280009890&ei=iRg9ZrPkNaaN9u8Pk7mEsAU&ved=0ahUKEwjzzLf9m4GGAxWmhv0HHZMcAVYQ4dUDCAk&uact=5&oq=restaurant+z%C3%BCrich+kreis+11&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhtyZXN0YXVyYW50IHrDvHJpY2gga3JlaXMgMTEyBBAjGCcyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiiBBiJBUjkDFCzBljFCnAAeACQAQCYAWigAZQCqgEDMi4xuAEDyAEA-AEBmAIDoAKnAsICBhAAGBYYHpgDAIgGAZIHAzIuMaAH1BM&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[47.4153306,8.553521],[47.406279,8.5367404]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:9',
        'https://www.google.com/search?q=restaurant+z%C3%BCrich+kreis+12&sca_esv=dc1b946dcae22bbc&sca_upv=1&biw=1920&bih=1065&tbm=lcl&sxsrf=ADLYWIINqQr7xifQ_D4p4ga2V-x6-enrWg%3A1715280022239&ei=lhg9ZpqUDpr97_UPi4290As&ved=0ahUKEwiat6mDnIGGAxWa_rsIHYtGD7oQ4dUDCAk&uact=5&oq=restaurant+z%C3%BCrich+kreis+12&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhtyZXN0YXVyYW50IHrDvHJpY2gga3JlaXMgMTIyBBAjGCcyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBEixIlDQBlihIHADeACQAQCYAYQBoAH6AqoBAzMuMbgBA8gBAPgBAZgCB6ACsQPCAgYQABgWGB7CAgUQIRigAZgDAIgGAZIHAzYuMaAHgBU&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[47.411392899999996,8.5877197],[47.3988753,8.5554314]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:9'
    ]

    def __init__(self):
        self.csvfile = open('titles.csv', 'w', newline='', encoding='utf-8')
        self.fieldnames = ['title', 'average_review', 'address', 'kitchen', 'price', 'number_reviews', 'price_sign']
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)
        self.writer.writeheader()
        self.options = Options()
        self.driver = webdriver.Chrome(options=self.options)
   #Lädt die URL's und ruft den Scraper auf (scrape page)     
    def parse(self, response):
        self.driver.get(response.url)
        self.scrape_page()
   #Ist zwar in dieser Version nicht mehr genauso notwenig, da die review_dates nicht mehr extrahiert werden, aber ich lasse es trotzdem drin, da er zum einen menschlicheres Verhalten animiert und zum anderen bruacht es die TimeoutException
    def click_reviews_tab(self):
        try:
            tabs = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.aYI8We.ero3Ve a[role="tab"]'))
            )
            #hier wird der Tab "Rezensionen" angeklickt dadurch dass er sucht, wo das Wort steht. Die Schleife brauchts, da die Seite immmer neu aufgebaut ist.
            for tab in tabs:
                if tab.text == "Rezensionen":
                    tab.click()
                    sleep(2)
                    return True
            return False
        except TimeoutException:
            return False
# Der eigentliche Scraper, der die Daten extrahiert und in die CSV schreibt
    def scrape_page(self):
        self.driver.implicitly_wait(5) 
        last_restaurant_count = 0

        while True:
            # Re-find the divs to avoid stale element reference
            parent_divs = self.driver.find_elements(By.CSS_SELECTOR, 'div.rllt__details') #Crawler sucht die Parent_elements (Die Kacheln)
            current_restaurant_count = len(parent_divs)

            if last_restaurant_count == current_restaurant_count:
                break
# Iteriert über die Kacheln und extrahiert die Daten
            for i in range(current_restaurant_count):
                # Re-find the divs and get the current div to avoid stale element reference
                parent_divs = self.driver.find_elements(By.CSS_SELECTOR, 'div.rllt__details')
                if i >= len(parent_divs):
                    break
                div = parent_divs[i]

                try:
                    title = div.find_element(By.CSS_SELECTOR, 'div.dbg0pd > span.OSrXXb').text
                    average_review = div.find_element(By.CSS_SELECTOR, 'span.z3HNkc').get_attribute('aria-label')
                    number_reviews = div.find_element(By.CSS_SELECTOR, 'span.RDApEe.YrbPuc').text.strip('()')
                    price_sign = div.find_element(By.CSS_SELECTOR, 'span[aria-label][role="img"]').get_attribute('aria-label') #Nur zur Kontrolle, dass auch die Daten des entsp. Restaurants gezogen wurden.
                    price = self.extract_price(div) 
                    kitchen = self.extract_kitchen(div)
                    
                    # If kitchen or price information is missing, assign 'Not Available'
                    kitchen = kitchen if kitchen is not None else 'Not Available'
                    price = price if price is not None else 'Not Available'
                    
                    div.click()
                    sleep (random.uniform(3, 6))  # Adjust this wait time as necessary

                    address_element = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.LrzXr'))
                    )
                    address = address_element.text

                    if self.click_reviews_tab():
                        #self.scroll_to_load_reviews()
                        # review_dates = self.extract_review_dates()  # überspringt das, da das Scrollen nicht funktioniert
                        self.writer.writerow({
                            'title': title,
                            'average_review': average_review,
                            'address': address,
                            'kitchen': kitchen,
                            'price': price,
                            'number_reviews': number_reviews,
                            'price_sign': price_sign
                        })


                    self.driver.back()  #Züruck zu den Restaurantkacheln
                    sleep(random.uniform(3, 6))                   
                except (NoSuchElementException, StaleElementReferenceException) as e:
                    print(f"Error encountered: {e}")
                    self.driver.back()
                    sleep(2)
                    continue  # Skip to the next iteration            
            
            last_restaurant_count = current_restaurant_count
            # Am Ende der Iteration wird geschaut, ob es eine nächste Seite gibt und wenn ja wird sie angeklickt
            try:
                next_button = self.driver.find_element(By.CSS_SELECTOR, '#pnnext')
                if next_button:
                     next_button.click()
                     time.sleep(random.uniform(3, 6))  # Adjust this wait time as necessary
                     self.scrape_page()
            except:
                 print("No next button found or element is stale.")
                 break
# Preis und Küche wird extra extrahiert, da sie nicht immer in der gleichen Reihenfolge stehen und die Span-ELemente verauscht waren.
    def extract_price(self, div):
        try:
        # Sucht 'aria-label' und 'role="img"', und schliesst diese aus mit 'Bewertung' in 'aria-label'
            price_elements = div.find_elements(By.CSS_SELECTOR, 'span[aria-label][role="img"]')
            for price_element in price_elements:
                aria_label = price_element.get_attribute('aria-label')
                if "Bewertung" not in aria_label:  # Ausschluss von 'Bewertung'
                    return aria_label  # Wenn vorhande, wir nund bspw: "Mäßig teuer", "Teuer", etc. ausgegebn.
        except NoSuchElementException:
            return 'Price information not available'  # Falls nichts gefuenden wird, wird dies ausgegeben

        return 'Price information not available'  # Wenn kein Span gefunden.  
# Küche wird extra extrahiert, da sie nicht immer in der gleichen Reihenfolge stehen und die Span-ELemente verauscht waren.
    def extract_kitchen(self, div):
        try:
            details_div = div.find_element(By.CSS_SELECTOR, 'div.rllt__details div:nth-of-type(2)')
            details = details_div.text.split('·')
            price_sign = self.extract_price(div)   #Kontrolle   
            kitchen = None
    
            for detail in details:
                detail = detail.strip()
                if not any(char.isdigit() for char in detail):
                    kitchen = detail    
            return kitchen
        except NoSuchElementException:
            return None
# Diese Methode wird nicht verwendet. Das Scrollen funktioniert innerhalb der Seite nicht. Er soll zuerst alles Scrollen, damit die Daten geeladen werden und dann soll er das letzte Datum extrahieren. Wenn die Die Funnktion (mit oben), dann werden nur die Review_dates der aktuellen Seite gespeichert.
    def scroll_to_load_reviews(self):
        try:
            reviews_container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="akp_tsuid_34"]/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[6]/g-flippy-carousel/div/div/ol/li[3]/span/div/div/div/div[2]/c-wiz/div/div[6]'))
            )
            last_height = self.driver.execute_script("return arguments[0].scrollHeight", reviews_container)
            while True:
                self.driver.execute_script("arguments[0].scrollBy(0, arguments[0].scrollHeight)", reviews_container)
                sleep(2)
                new_height = self.driver.execute_script("return arguments[0].scrollHeight", reviews_container)
                if new_height == last_height:
                    break
                last_height = new_height
        except Exception as e:
            print(f"Error scrolling to load reviews: {e}")

    def close(self, reason):
        self.csvfile.close()
        self.driver.quit()

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(GetDataSpider)
    process.start()

