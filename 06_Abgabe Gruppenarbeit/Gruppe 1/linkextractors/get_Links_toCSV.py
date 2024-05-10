# This is a sample Python script.
import re
import csv
import pandas as pd
#ref: https://www.geeksforgeeks.org/python-save-list-to-csv/
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def scraper():
    fields = ['Link']
    filename = "getyourguide_list.csv"
    # Use a breakpoint in the code line below to debug your script.

    # Press ⌘F8 to toggle the breakpoint./Users/louishuber/Downloads
    with open('/Users/louishuber/Downloads/The BEST New York City Tours and Things to Do in 2024 - FREE Cancellation _ GetYourGuide-27-3-24.html', 'r') as file:  # scr:https://stackoverflow.com/questions/68351484/easiest-way-to-open-an-html-file-and-save-it-as-a-string-variable
        html_as_string = file.read()
        link_list = []
        #print(html_as_string)
        res = re.findall(r'(https://www.getyourguide.com/new-york-city-l59/[\w*-]+)', html_as_string)
        #res = re.findall(r'(https://www.getyourguide.com/new-york-city-l59/(\w*)-(\w*))', html_as_string)

        #res = re.search(r'^"https://www.getyourguide.com/new-york-city-l59/".*\', html_as_string)
        #r'^ftp://.*\.jpg$'

        #https: // www.getyourguide.com / new - york - city - l59 /.
        #cut first 14 elements
        res = res[14:]
        #remove duplicates ref: https://www.w3schools.com/python/python_howto_remove_duplicates.asp
        res = list(dict.fromkeys(res))
        print(res)
        print(len(res))
        #print(html_as_string)
    dict1 = {'link': res}

    df = pd.DataFrame(dict1)

    # saving the dataframe
    df.to_csv('gygNewYork.csv')
if __name__ == '__main__':
    scraper()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
