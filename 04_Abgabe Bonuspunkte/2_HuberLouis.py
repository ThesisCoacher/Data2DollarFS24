# This is a webscraption script for airbnb
#unfortunately, it is not always working and I had to try it multiple times


def webscraping():
    #basic idea from https://pythonbasics.org/selenium-get-html/
    #importing libraries
    from selenium import webdriver
    import time
    import re
    import csv


    #ref: for csv: https://www.geeksforgeeks.org/working-csv-files-python/
    #define fields to save data
    fields = ['Preis', 'Name']
    filename = "2_HuberLouis.csv"
    rows = []

    #open browser
    browser = webdriver.Firefox()
    browser.get("https://www.airbnb.ch/s/St.-Gallen--Schweiz/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-04-01&monthly_length=3&monthly_end_date=2024-07-01&price_filter_input_type=2&channel=EXPLORE&query=St.%20Gallen%2C%20Schweiz&place_id=ChIJoR85ryDimkcRmxnF_e9vd4A&date_picker_type=calendar&checkin=2024-10-10&checkout=2024-10-20&source=structured_search_input_header&search_type=filter_change&price_filter_num_nights=3")
    time.sleep(10)
    print("Start webscraping now!")


    #start the iterations of scraping
    for i in range(0, 7):
        time.sleep(20)
        #save html code
        html = browser.page_source
        print(html)
        pattern = "CHF pro Nacht"
        findings = []
        #based on finding in html code, the the price
        # ref: https://blog.finxter.com/how-to-find-multiple-occurrences-of-a-string-within-a-string-in-python/
        for m in re.finditer(pattern, html):
            start = (m.start() - 10)
            end = start + 5
            findings.append(html[start:end])

        #as we have some more characters, we filter them out, we want only the numbers and cut out empty strings
        findings_list = []
        for words in findings:
            findings_list.append(''.join(filter(str.isdigit, words)))
        findings_list = list(filter(None, findings_list))

        #we do the same thing for the names of the listings
        pattern_2 = 'data-testid="listing-card-name">'
        findings_2 = []
        for m in re.finditer(pattern_2, html):
            start = (m.start() + 32)
            end = start + 60
            # ref: cut until < : https://stackoverflow.com/questions/27387415/how-would-i-get-everything-before-a-in-a-string-python
            #the 60 is just a random number, we just cut the rest of until the next < appears
            findings_2.append(html[start:end].split('<')[0])

        #the print statements are just for debugging
        print(findings_2)
        print(len(findings_2))

        print(findings_list)
        print(len(findings_list))


        #sometimes, airbnb shows some additional listings in between, so we cut them off
        #the first and last 9 listings are the one we want to scrape
        finding_cut = findings_list[0:9]
        finding_cut = finding_cut + findings_list[-9:]

        findings_cut_2 = findings_2[0:9]
        findings_cut_2 = findings_cut_2 + findings_2[-9:]

        #more print debugging (please don't tell my former professors)
        print(finding_cut)
        print(len(finding_cut))
        print(findings_cut_2)
        print(len(findings_cut_2))

        #we just combine the two list and append them to the rows with each iteration
        for i in finding_cut:
            rows.append([i, findings_cut_2[finding_cut.index(i)]])
        print(rows)

        #we click to the next button so we can scrape the next page
        #IMPORTANT: Sometimes the button is called "Weiter" and sometimes "Nächste Seite" in mobile mode maybe?
        button = browser.find_element("css selector", '[aria-label="Weiter"]')
        button.click()

    #write data to csv after finishing all iterations
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)


if __name__ == '__main__':
    webscraping()

