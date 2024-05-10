# This is a webscraption script for get your guide
#it uses the provided list of links to scrape the data from the webpages
from selenium import webdriver
import time
import re
import csv
import random


def webscraping():
    #basic idea from https://pythonbasics.org/selenium-get-html/
    #importing libraries

    link_list = ['https://www.airbnb.com/experiences/742435?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8', 
'https://www.airbnb.com/experiences/3664407?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8', 
'https://www.airbnb.com/experiences/4288140?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=0eaf44d1-67a1-4ffa-a17c-358a50807443&searchId=8e18fa11-fbce-42f3-bc6f-b64337a542cf&sectionId=932113b9-fd5f-453b-b031-3805bc80ca47',
'https://www.airbnb.com/experiences/3646788?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/3417662?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/4823601?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/2336395?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/4164596?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/4029481?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1495556?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1216588?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/3674134?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/3623131?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=0eaf44d1-67a1-4ffa-a17c-358a50807443&searchId=8e18fa11-fbce-42f3-bc6f-b64337a542cf&sectionId=932113b9-fd5f-453b-b031-3805bc80ca47',
'https://www.airbnb.com/experiences/4466692?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/4863367?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/3482610?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/700707?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/669902?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1207128?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1236643?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=0eaf44d1-67a1-4ffa-a17c-358a50807443&searchId=8e18fa11-fbce-42f3-bc6f-b64337a542cf&sectionId=932113b9-fd5f-453b-b031-3805bc80ca47',
'https://www.airbnb.com/experiences/4560533?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/278796?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/4696077?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/3656164?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/820923?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/3777246?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/579300?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/3166506?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/4619112?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1154871?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/4020137?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1395119?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/4296630?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/661879?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/3896425?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/4625130?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1597047?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=0eaf44d1-67a1-4ffa-a17c-358a50807443&searchId=8e18fa11-fbce-42f3-bc6f-b64337a542cf&sectionId=932113b9-fd5f-453b-b031-3805bc80ca47',
'https://www.airbnb.com/experiences/3773041?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/4449831?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/4553917?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/2481370?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/681535?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/4215483?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1215456?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=0eaf44d1-67a1-4ffa-a17c-358a50807443&searchId=8e18fa11-fbce-42f3-bc6f-b64337a542cf&sectionId=932113b9-fd5f-453b-b031-3805bc80ca47',
'https://www.airbnb.com/experiences/4390788?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1182860?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/4496855?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1515347?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/3762084?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/4682316?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/4134708?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=0eaf44d1-67a1-4ffa-a17c-358a50807443&searchId=8e18fa11-fbce-42f3-bc6f-b64337a542cf&sectionId=932113b9-fd5f-453b-b031-3805bc80ca47',
'https://www.airbnb.com/experiences/4581340?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1137127?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/3898172?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/4464922?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1512267?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1234128?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1063170?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/661863?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=0eaf44d1-67a1-4ffa-a17c-358a50807443&searchId=8e18fa11-fbce-42f3-bc6f-b64337a542cf&sectionId=932113b9-fd5f-453b-b031-3805bc80ca47',
'https://www.airbnb.com/experiences/201641?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1364471?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/3358733?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/281220?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/3720501?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/4304705?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/4449679?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/796520?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/2158834?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/2456270?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/4845026?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/4401103?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/3416324?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/679086?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/829385?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/279031?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/952800?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/679084?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/1753409?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/3712985?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/1329564?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/3490103?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/3749898?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/387115?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/3478800?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/3139107?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/4079305?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/2641226?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/2201461?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/2599805?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/1097192?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/3090265?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/4137748?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/3421445?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/1505659?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/3479508?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/2910603?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/1496468?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/187682?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/1262410?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/3282091?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/3123118?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=031742ae-c760-4d1c-9d66-43aab4b745fe&searchId=f875ebf6-347c-421a-b33d-f55e2f31a5ed&sectionId=d6211bd6-4379-44e8-a967-a9be20e481b1',
'https://www.airbnb.com/experiences/2852836?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=031742ae-c760-4d1c-9d66-43aab4b745fe&searchId=f875ebf6-347c-421a-b33d-f55e2f31a5ed&sectionId=d6211bd6-4379-44e8-a967-a9be20e481b1',
'https://www.airbnb.com/experiences/3068641?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=031742ae-c760-4d1c-9d66-43aab4b745fe&searchId=f875ebf6-347c-421a-b33d-f55e2f31a5ed&sectionId=d6211bd6-4379-44e8-a967-a9be20e481b1',
'https://www.airbnb.com/experiences/1267835?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=031742ae-c760-4d1c-9d66-43aab4b745fe&searchId=f875ebf6-347c-421a-b33d-f55e2f31a5ed&sectionId=d6211bd6-4379-44e8-a967-a9be20e481b1',
'https://www.airbnb.com/experiences/2031119?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=031742ae-c760-4d1c-9d66-43aab4b745fe&searchId=f875ebf6-347c-421a-b33d-f55e2f31a5ed&sectionId=d6211bd6-4379-44e8-a967-a9be20e481b1',
'https://www.airbnb.com/experiences/125150?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=031742ae-c760-4d1c-9d66-43aab4b745fe&searchId=f875ebf6-347c-421a-b33d-f55e2f31a5ed&sectionId=d6211bd6-4379-44e8-a967-a9be20e481b1',
'https://www.airbnb.com/experiences/3476120?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=031742ae-c760-4d1c-9d66-43aab4b745fe&searchId=f875ebf6-347c-421a-b33d-f55e2f31a5ed&sectionId=d6211bd6-4379-44e8-a967-a9be20e481b1',
'https://www.airbnb.com/experiences/4883862?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=031742ae-c760-4d1c-9d66-43aab4b745fe&searchId=f875ebf6-347c-421a-b33d-f55e2f31a5ed&sectionId=d6211bd6-4379-44e8-a967-a9be20e481b1',
'https://www.airbnb.com/experiences/3749476?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=57b2776c-f7c3-4f13-a41c-bd6e8454b812&searchId=41928aa4-bd1f-4137-ac56-f1fd52786c74&sectionId=6938cd5c-c7a2-44ec-9095-8d5a27177e04',
'https://www.airbnb.com/experiences/3589012?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=57b2776c-f7c3-4f13-a41c-bd6e8454b812&searchId=41928aa4-bd1f-4137-ac56-f1fd52786c74&sectionId=6938cd5c-c7a2-44ec-9095-8d5a27177e04',
'https://www.airbnb.com/experiences/262605?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=57b2776c-f7c3-4f13-a41c-bd6e8454b812&searchId=41928aa4-bd1f-4137-ac56-f1fd52786c74&sectionId=6938cd5c-c7a2-44ec-9095-8d5a27177e04',
'https://www.airbnb.com/experiences/4436082?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=dd0abbf1-ff83-4886-a0fa-2be24940a61b&searchId=21509724-2e38-475c-b3e0-a414744f17fc&sectionId=f3145ec7-f937-450c-8315-406c3ea192d2',
'https://www.airbnb.com/experiences/4644262?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=dd0abbf1-ff83-4886-a0fa-2be24940a61b&searchId=21509724-2e38-475c-b3e0-a414744f17fc&sectionId=f3145ec7-f937-450c-8315-406c3ea192d2',
'https://www.airbnb.com/experiences/1573799?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=dd0abbf1-ff83-4886-a0fa-2be24940a61b&searchId=21509724-2e38-475c-b3e0-a414744f17fc&sectionId=f3145ec7-f937-450c-8315-406c3ea192d2',
'https://www.airbnb.com/experiences/1176794?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=dd0abbf1-ff83-4886-a0fa-2be24940a61b&searchId=21509724-2e38-475c-b3e0-a414744f17fc&sectionId=f3145ec7-f937-450c-8315-406c3ea192d2',
'https://www.airbnb.com/experiences/349332?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=dd0abbf1-ff83-4886-a0fa-2be24940a61b&searchId=21509724-2e38-475c-b3e0-a414744f17fc&sectionId=f3145ec7-f937-450c-8315-406c3ea192d2',
'https://www.airbnb.com/experiences/1018710?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=dd0abbf1-ff83-4886-a0fa-2be24940a61b&searchId=21509724-2e38-475c-b3e0-a414744f17fc&sectionId=f3145ec7-f937-450c-8315-406c3ea192d2',
'https://www.airbnb.com/experiences/4739370?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=dd0abbf1-ff83-4886-a0fa-2be24940a61b&searchId=21509724-2e38-475c-b3e0-a414744f17fc&sectionId=f3145ec7-f937-450c-8315-406c3ea192d2',
'https://www.airbnb.com/experiences/1812748?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=ed26f160-a298-463e-b608-807b39a52033&searchId=b63405ec-e1a0-46f7-9478-dffabebe5474&sectionId=cb45931f-8017-4453-a642-ac676124c2e8',
'https://www.airbnb.com/experiences/1533530?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=ed26f160-a298-463e-b608-807b39a52033&searchId=b63405ec-e1a0-46f7-9478-dffabebe5474&sectionId=cb45931f-8017-4453-a642-ac676124c2e8',
'https://www.airbnb.com/experiences/851555?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=ed26f160-a298-463e-b608-807b39a52033&searchId=b63405ec-e1a0-46f7-9478-dffabebe5474&sectionId=cb45931f-8017-4453-a642-ac676124c2e8',
'https://www.airbnb.com/experiences/3640113?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=ed26f160-a298-463e-b608-807b39a52033&searchId=b63405ec-e1a0-46f7-9478-dffabebe5474&sectionId=cb45931f-8017-4453-a642-ac676124c2e8',
'https://www.airbnb.com/experiences/2938054?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=ed26f160-a298-463e-b608-807b39a52033&searchId=b63405ec-e1a0-46f7-9478-dffabebe5474&sectionId=cb45931f-8017-4453-a642-ac676124c2e8',
'https://www.airbnb.com/experiences/3698714?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=ed26f160-a298-463e-b608-807b39a52033&searchId=b63405ec-e1a0-46f7-9478-dffabebe5474&sectionId=cb45931f-8017-4453-a642-ac676124c2e8',
'https://www.airbnb.com/experiences/1471616?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=ed26f160-a298-463e-b608-807b39a52033&searchId=b63405ec-e1a0-46f7-9478-dffabebe5474&sectionId=cb45931f-8017-4453-a642-ac676124c2e8',
'https://www.airbnb.com/experiences/432940?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=ed26f160-a298-463e-b608-807b39a52033&searchId=b63405ec-e1a0-46f7-9478-dffabebe5474&sectionId=cb45931f-8017-4453-a642-ac676124c2e8',
'https://www.airbnb.com/experiences/4486471?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=ed26f160-a298-463e-b608-807b39a52033&searchId=b63405ec-e1a0-46f7-9478-dffabebe5474&sectionId=cb45931f-8017-4453-a642-ac676124c2e8',
'https://www.airbnb.com/experiences/1417401?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=120934c4-ce90-4538-ac15-dae02b27d77d&searchId=920d765a-dc55-45d4-9f17-00fb8b35e2f7&sectionId=aff7c83c-c7d9-4df6-9e51-95675616988d',
'https://www.airbnb.com/experiences/3483920?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=120934c4-ce90-4538-ac15-dae02b27d77d&searchId=920d765a-dc55-45d4-9f17-00fb8b35e2f7&sectionId=aff7c83c-c7d9-4df6-9e51-95675616988d',
'https://www.airbnb.com/experiences/3665755?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=120934c4-ce90-4538-ac15-dae02b27d77d&searchId=920d765a-dc55-45d4-9f17-00fb8b35e2f7&sectionId=aff7c83c-c7d9-4df6-9e51-95675616988d',
'https://www.airbnb.com/experiences/371834?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=120934c4-ce90-4538-ac15-dae02b27d77d&searchId=920d765a-dc55-45d4-9f17-00fb8b35e2f7&sectionId=aff7c83c-c7d9-4df6-9e51-95675616988d',
'https://www.airbnb.com/experiences/4494264?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=a60bb004-9323-4f42-a141-c48f2ac66c85&searchId=941cf844-af88-483a-8255-7b08e06eef56&sectionId=54ce7fa8-d4c0-464e-ae48-a7d3d099fde8',
'https://www.airbnb.com/experiences/4018986?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=a60bb004-9323-4f42-a141-c48f2ac66c85&searchId=941cf844-af88-483a-8255-7b08e06eef56&sectionId=54ce7fa8-d4c0-464e-ae48-a7d3d099fde8',
'https://www.airbnb.com/experiences/3004718?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=a60bb004-9323-4f42-a141-c48f2ac66c85&searchId=941cf844-af88-483a-8255-7b08e06eef56&sectionId=54ce7fa8-d4c0-464e-ae48-a7d3d099fde8',
'https://www.airbnb.com/experiences/182323?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=a60bb004-9323-4f42-a141-c48f2ac66c85&searchId=941cf844-af88-483a-8255-7b08e06eef56&sectionId=54ce7fa8-d4c0-464e-ae48-a7d3d099fde8',
'https://www.airbnb.com/experiences/2219129?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=a60bb004-9323-4f42-a141-c48f2ac66c85&searchId=941cf844-af88-483a-8255-7b08e06eef56&sectionId=54ce7fa8-d4c0-464e-ae48-a7d3d099fde8',
'https://www.airbnb.com/experiences/1527020?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=a60bb004-9323-4f42-a141-c48f2ac66c85&searchId=941cf844-af88-483a-8255-7b08e06eef56&sectionId=54ce7fa8-d4c0-464e-ae48-a7d3d099fde8',
'https://www.airbnb.com/experiences/2981713?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/2970081?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/164127?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/876586?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1399873?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/380236?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=0eaf44d1-67a1-4ffa-a17c-358a50807443&searchId=8e18fa11-fbce-42f3-bc6f-b64337a542cf&sectionId=932113b9-fd5f-453b-b031-3805bc80ca47',
'https://www.airbnb.com/experiences/2011027?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=0eaf44d1-67a1-4ffa-a17c-358a50807443&searchId=8e18fa11-fbce-42f3-bc6f-b64337a542cf&sectionId=932113b9-fd5f-453b-b031-3805bc80ca47',
'https://www.airbnb.com/experiences/4683493?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=0eaf44d1-67a1-4ffa-a17c-358a50807443&searchId=8e18fa11-fbce-42f3-bc6f-b64337a542cf&sectionId=932113b9-fd5f-453b-b031-3805bc80ca47',
'https://www.airbnb.com/experiences/576789?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=0eaf44d1-67a1-4ffa-a17c-358a50807443&searchId=8e18fa11-fbce-42f3-bc6f-b64337a542cf&sectionId=932113b9-fd5f-453b-b031-3805bc80ca47',
'https://www.airbnb.com/experiences/3687031?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/500361?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/207157?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/690043?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/2598776?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/188587?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/139031?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/1323659?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/396676?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/3130593?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/2448604?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/1072035?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/1089631?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/445486?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/210126?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/392248?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/1166516?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/1041942?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/1100342?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/873918?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/150648?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/244023?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=031742ae-c760-4d1c-9d66-43aab4b745fe&searchId=f875ebf6-347c-421a-b33d-f55e2f31a5ed&sectionId=d6211bd6-4379-44e8-a967-a9be20e481b1',
'https://www.airbnb.com/experiences/143920?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=57b2776c-f7c3-4f13-a41c-bd6e8454b812&searchId=41928aa4-bd1f-4137-ac56-f1fd52786c74&sectionId=6938cd5c-c7a2-44ec-9095-8d5a27177e04',
'https://www.airbnb.com/experiences/832544?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=a60bb004-9323-4f42-a141-c48f2ac66c85&searchId=941cf844-af88-483a-8255-7b08e06eef56&sectionId=54ce7fa8-d4c0-464e-ae48-a7d3d099fde8',
'https://www.airbnb.com/experiences/250241?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/972608?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/74748?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/4218000?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/438902?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/262429?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/263550?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/1474583?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/259740?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/120361?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=57b2776c-f7c3-4f13-a41c-bd6e8454b812&searchId=41928aa4-bd1f-4137-ac56-f1fd52786c74&sectionId=6938cd5c-c7a2-44ec-9095-8d5a27177e04',
'https://www.airbnb.com/experiences/3903437?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=ed26f160-a298-463e-b608-807b39a52033&searchId=b63405ec-e1a0-46f7-9478-dffabebe5474&sectionId=cb45931f-8017-4453-a642-ac676124c2e8',
'https://www.airbnb.com/experiences/885043?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=120934c4-ce90-4538-ac15-dae02b27d77d&searchId=920d765a-dc55-45d4-9f17-00fb8b35e2f7&sectionId=aff7c83c-c7d9-4df6-9e51-95675616988d',
'https://www.airbnb.com/experiences/528247?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=a60bb004-9323-4f42-a141-c48f2ac66c85&searchId=941cf844-af88-483a-8255-7b08e06eef56&sectionId=54ce7fa8-d4c0-464e-ae48-a7d3d099fde8',
'https://www.airbnb.com/experiences/269716?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/298126?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/3671959?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/1464413?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/317319?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/1069143?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/338002?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/1338042?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/1302489?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/111307?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/921146?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/242509?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/2152652?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/1439194?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/4130627?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/2445471?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/133519?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/98988?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/1326396?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/101160?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/3552802?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=031742ae-c760-4d1c-9d66-43aab4b745fe&searchId=f875ebf6-347c-421a-b33d-f55e2f31a5ed&sectionId=d6211bd6-4379-44e8-a967-a9be20e481b1',
'https://www.airbnb.com/experiences/2395344?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/80034?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/4500619?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/3501810?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/156739?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/95224?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/692852?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/158314?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/90081?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/135716?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=dd0abbf1-ff83-4886-a0fa-2be24940a61b&searchId=21509724-2e38-475c-b3e0-a414744f17fc&sectionId=f3145ec7-f937-450c-8315-406c3ea192d2',
'https://www.airbnb.com/experiences/4734889?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/706356?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/1118125?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/2443302?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=57b2776c-f7c3-4f13-a41c-bd6e8454b812&searchId=41928aa4-bd1f-4137-ac56-f1fd52786c74&sectionId=6938cd5c-c7a2-44ec-9095-8d5a27177e04',
'https://www.airbnb.com/experiences/106901?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/462923?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/3264998?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=120934c4-ce90-4538-ac15-dae02b27d77d&searchId=920d765a-dc55-45d4-9f17-00fb8b35e2f7&sectionId=aff7c83c-c7d9-4df6-9e51-95675616988d',
'https://www.airbnb.com/experiences/102778?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/4135674?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/1222576?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/390592?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/968040?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/3623673?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=57b2776c-f7c3-4f13-a41c-bd6e8454b812&searchId=41928aa4-bd1f-4137-ac56-f1fd52786c74&sectionId=6938cd5c-c7a2-44ec-9095-8d5a27177e04',
'https://www.airbnb.com/experiences/256706?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=57b2776c-f7c3-4f13-a41c-bd6e8454b812&searchId=41928aa4-bd1f-4137-ac56-f1fd52786c74&sectionId=6938cd5c-c7a2-44ec-9095-8d5a27177e04',
'https://www.airbnb.com/experiences/2318215?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/599107?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/79145?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/164829?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/354676?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=57b2776c-f7c3-4f13-a41c-bd6e8454b812&searchId=41928aa4-bd1f-4137-ac56-f1fd52786c74&sectionId=6938cd5c-c7a2-44ec-9095-8d5a27177e04',
'https://www.airbnb.com/experiences/3479653?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=dd0abbf1-ff83-4886-a0fa-2be24940a61b&searchId=21509724-2e38-475c-b3e0-a414744f17fc&sectionId=f3145ec7-f937-450c-8315-406c3ea192d2',
'https://www.airbnb.com/experiences/363152?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=ed26f160-a298-463e-b608-807b39a52033&searchId=b63405ec-e1a0-46f7-9478-dffabebe5474&sectionId=cb45931f-8017-4453-a642-ac676124c2e8',
'https://www.airbnb.com/experiences/2635092?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=a60bb004-9323-4f42-a141-c48f2ac66c85&searchId=941cf844-af88-483a-8255-7b08e06eef56&sectionId=54ce7fa8-d4c0-464e-ae48-a7d3d099fde8',
'https://www.airbnb.com/experiences/1567840?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/1528657?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/577058?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/356565?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=120934c4-ce90-4538-ac15-dae02b27d77d&searchId=920d765a-dc55-45d4-9f17-00fb8b35e2f7&sectionId=aff7c83c-c7d9-4df6-9e51-95675616988d',
'https://www.airbnb.com/experiences/3903535?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=a60bb004-9323-4f42-a141-c48f2ac66c85&searchId=941cf844-af88-483a-8255-7b08e06eef56&sectionId=54ce7fa8-d4c0-464e-ae48-a7d3d099fde8',
'https://www.airbnb.com/experiences/2938500?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=a60bb004-9323-4f42-a141-c48f2ac66c85&searchId=941cf844-af88-483a-8255-7b08e06eef56&sectionId=54ce7fa8-d4c0-464e-ae48-a7d3d099fde8',
'https://www.airbnb.com/experiences/244996?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=a60bb004-9323-4f42-a141-c48f2ac66c85&searchId=941cf844-af88-483a-8255-7b08e06eef56&sectionId=54ce7fa8-d4c0-464e-ae48-a7d3d099fde8',
'https://www.airbnb.com/experiences/1443665?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/394446?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/269616?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=120934c4-ce90-4538-ac15-dae02b27d77d&searchId=920d765a-dc55-45d4-9f17-00fb8b35e2f7&sectionId=aff7c83c-c7d9-4df6-9e51-95675616988d',
'https://www.airbnb.com/experiences/73865?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/2257518?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/503918?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/757903?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/731215?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=120934c4-ce90-4538-ac15-dae02b27d77d&searchId=920d765a-dc55-45d4-9f17-00fb8b35e2f7&sectionId=aff7c83c-c7d9-4df6-9e51-95675616988d',
'https://www.airbnb.com/experiences/189912?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=0eaf44d1-67a1-4ffa-a17c-358a50807443&searchId=8e18fa11-fbce-42f3-bc6f-b64337a542cf&sectionId=932113b9-fd5f-453b-b031-3805bc80ca47',
'https://www.airbnb.com/experiences/659908?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/106510?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/240574?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/2316091?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/351924?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=ed26f160-a298-463e-b608-807b39a52033&searchId=b63405ec-e1a0-46f7-9478-dffabebe5474&sectionId=cb45931f-8017-4453-a642-ac676124c2e8',
'https://www.airbnb.com/experiences/123876?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/598678?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/1006557?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/888274?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/46202?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=dd0abbf1-ff83-4886-a0fa-2be24940a61b&searchId=21509724-2e38-475c-b3e0-a414744f17fc&sectionId=f3145ec7-f937-450c-8315-406c3ea192d2',
'https://www.airbnb.com/experiences/232387?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=120934c4-ce90-4538-ac15-dae02b27d77d&searchId=920d765a-dc55-45d4-9f17-00fb8b35e2f7&sectionId=aff7c83c-c7d9-4df6-9e51-95675616988d',
'https://www.airbnb.com/experiences/1413504?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/848299?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=3e5c0aa3-088c-4916-9313-cf48aba06e7b&searchId=597d2331-e72c-461e-bb4a-e7e6be450f81&sectionId=f9856952-954e-479f-ac04-c59da751a55b',
'https://www.airbnb.com/experiences/311122?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/847787?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/1395028?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=57b2776c-f7c3-4f13-a41c-bd6e8454b812&searchId=41928aa4-bd1f-4137-ac56-f1fd52786c74&sectionId=6938cd5c-c7a2-44ec-9095-8d5a27177e04',
'https://www.airbnb.com/experiences/92344?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/842735?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/565385?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=dd0abbf1-ff83-4886-a0fa-2be24940a61b&searchId=21509724-2e38-475c-b3e0-a414744f17fc&sectionId=f3145ec7-f937-450c-8315-406c3ea192d2',
'https://www.airbnb.com/experiences/2720397?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/1530170?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/714299?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/85642?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=57b2776c-f7c3-4f13-a41c-bd6e8454b812&searchId=41928aa4-bd1f-4137-ac56-f1fd52786c74&sectionId=6938cd5c-c7a2-44ec-9095-8d5a27177e04',
'https://www.airbnb.com/experiences/99094?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=44796828-c0df-4309-95ba-967f5eb6947d&searchId=e72b11ed-167b-47d4-b038-e7066f83feca&sectionId=e43ffeda-c498-4a35-80d5-36c5542f57f3',
'https://www.airbnb.com/experiences/3727498?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/853747?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/88519?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/992747?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/4888466?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=57b2776c-f7c3-4f13-a41c-bd6e8454b812&searchId=41928aa4-bd1f-4137-ac56-f1fd52786c74&sectionId=6938cd5c-c7a2-44ec-9095-8d5a27177e04',
'https://www.airbnb.com/experiences/1305139?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=68bdb554-b339-4041-9694-e5f2c40cf4d7&searchId=885ac543-a5b1-4f6f-96c4-f1449b6fcbc3&sectionId=52cca717-b38f-4c47-9bb5-232dee5f1bfd',
'https://www.airbnb.com/experiences/346987?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/1071278?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/1079648?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=031742ae-c760-4d1c-9d66-43aab4b745fe&searchId=f875ebf6-347c-421a-b33d-f55e2f31a5ed&sectionId=d6211bd6-4379-44e8-a967-a9be20e481b1',
'https://www.airbnb.com/experiences/598649?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/418104?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/94326?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=ed26f160-a298-463e-b608-807b39a52033&searchId=b63405ec-e1a0-46f7-9478-dffabebe5474&sectionId=cb45931f-8017-4453-a642-ac676124c2e8',
'https://www.airbnb.com/experiences/403234?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/4581299?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=dd0abbf1-ff83-4886-a0fa-2be24940a61b&searchId=21509724-2e38-475c-b3e0-a414744f17fc&sectionId=f3145ec7-f937-450c-8315-406c3ea192d2',
'https://www.airbnb.com/experiences/4423042?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=763e5883-cd15-41cc-90c2-9273bfebac1d&searchId=600e29fb-d46b-466a-9313-53109c05a7c8&sectionId=480e00d6-4226-4874-884d-245433a01fc5',
'https://www.airbnb.com/experiences/992847?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=031742ae-c760-4d1c-9d66-43aab4b745fe&searchId=f875ebf6-347c-421a-b33d-f55e2f31a5ed&sectionId=d6211bd6-4379-44e8-a967-a9be20e481b1',
'https://www.airbnb.com/experiences/185749?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=031742ae-c760-4d1c-9d66-43aab4b745fe&searchId=f875ebf6-347c-421a-b33d-f55e2f31a5ed&sectionId=d6211bd6-4379-44e8-a967-a9be20e481b1',
'https://www.airbnb.com/experiences/2164870?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/179865?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5591d7ff-0e73-4ddf-90f3-6d8985771231&searchId=42ce9647-9b1b-47fb-9da8-5e1c24efb645&sectionId=c177fc47-35e6-43a0-8ee9-e7131eae0a49',
'https://www.airbnb.com/experiences/194337?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=57b2776c-f7c3-4f13-a41c-bd6e8454b812&searchId=41928aa4-bd1f-4137-ac56-f1fd52786c74&sectionId=6938cd5c-c7a2-44ec-9095-8d5a27177e04',
'https://www.airbnb.com/experiences/873943?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=57b2776c-f7c3-4f13-a41c-bd6e8454b812&searchId=41928aa4-bd1f-4137-ac56-f1fd52786c74&sectionId=6938cd5c-c7a2-44ec-9095-8d5a27177e04',
'https://www.airbnb.com/experiences/392961?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=14360057-058b-4163-ab0a-f726bcc5d8f0&searchId=0da25746-4218-45de-b7ec-5e9d16ffe4f8&sectionId=a327a493-fdbb-4aae-8e58-8415d75a137b',
'https://www.airbnb.com/experiences/661866?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=a60bb004-9323-4f42-a141-c48f2ac66c85&searchId=941cf844-af88-483a-8255-7b08e06eef56&sectionId=54ce7fa8-d4c0-464e-ae48-a7d3d099fde8',
'https://www.airbnb.com/experiences/1086276?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1463716?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559',
'https://www.airbnb.com/experiences/779455?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=96101f26-db0f-4bc8-8ab1-9eee4df23b17&searchId=ccf4c5f4-145e-48a9-91bf-e40e90cd8087&sectionId=44999ff3-4004-4be4-b67b-d66562a0dc52',
'https://www.airbnb.com/experiences/316457?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=031742ae-c760-4d1c-9d66-43aab4b745fe&searchId=f875ebf6-347c-421a-b33d-f55e2f31a5ed&sectionId=d6211bd6-4379-44e8-a967-a9be20e481b1',
'https://www.airbnb.com/experiences/2775154?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=031742ae-c760-4d1c-9d66-43aab4b745fe&searchId=f875ebf6-347c-421a-b33d-f55e2f31a5ed&sectionId=d6211bd6-4379-44e8-a967-a9be20e481b1',
'https://www.airbnb.com/experiences/992569?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=ed26f160-a298-463e-b608-807b39a52033&searchId=b63405ec-e1a0-46f7-9478-dffabebe5474&sectionId=cb45931f-8017-4453-a642-ac676124c2e8',
'https://www.airbnb.com/experiences/1398046?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/65826?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=a60bb004-9323-4f42-a141-c48f2ac66c85&searchId=941cf844-af88-483a-8255-7b08e06eef56&sectionId=54ce7fa8-d4c0-464e-ae48-a7d3d099fde8',
'https://www.airbnb.com/experiences/1571409?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=a60bb004-9323-4f42-a141-c48f2ac66c85&searchId=941cf844-af88-483a-8255-7b08e06eef56&sectionId=54ce7fa8-d4c0-464e-ae48-a7d3d099fde8',
'https://www.airbnb.com/experiences/1373740?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=fb9a8f77-70b8-494c-b4ea-1cdcf3384bed&searchId=953c8476-6ec9-40cd-a3a1-43f478d23017&sectionId=598cadf6-c503-4a2f-8aea-9047eeb226a8',
'https://www.airbnb.com/experiences/1345158?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=57b2776c-f7c3-4f13-a41c-bd6e8454b812&searchId=41928aa4-bd1f-4137-ac56-f1fd52786c74&sectionId=6938cd5c-c7a2-44ec-9095-8d5a27177e04]']
     
    #link_list = ['https://www.airbnb.com/experiences/2158834?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=5ede4bf8-0001-4f11-9d73-3cd9f37387d5&searchId=7f3a971f-a0a1-4920-912d-bf3bb2ba830e&sectionId=682e1afc-c097-460b-a047-d497557c9559', 'https://www.airbnb.com/experiences/1345158?location=New%20York%2C%20United%20States&currentTab=experience_tab&federatedSearchId=57b2776c-f7c3-4f13-a41c-bd6e8454b812&searchId=41928aa4-bd1f-4137-ac56-f1fd52786c74&sectionId=6938cd5c-c7a2-44ec-9095-8d5a27177e04]']

    #ref: for csv: https://www.geeksforgeeks.org/working-csv-files-python/
    #define fields to save data
    fields = ['link', 'name', 'price', 'avg_rating', 'number_ratings', 'description']
         #'price','description','total_rating','number_of_ratings','category','guide_rating','transportation_rating','value_for_money_rating','service_rating','organization_rating']
    filename = "airbnb_full_tour_data.csv"
    rows = []
    #use index so start by 0
    start_scrape_number = 0
    end_scrape_number = 309 #anzahl links minus 1; wenn ganze Liste dann 309 (falls nur Test dann 2)

    #open browser
    browser = webdriver.Firefox()
    time.sleep(1)
    print("Start webscraping now!")

    #start the iterations of scraping
    for i in range(start_scrape_number, end_scrape_number):
        #define standard values
        link = link_list[i]
        name=""
        price=""
        avg_rating=""
        number_ratings=""
        description=""

        print("scraping page:"+str(i))
        #wait random time
        wait_random_time()
        #open website
        browser.get(link_list[i]+ '&enable_auto_translate=false&locale=en') #NEU damit es auf Englisch bleibt statt DE
        
        #save html code
        html = browser.page_source
        #print(html)
        #find name
        try:
            name_list = re.findall(r'{"__typename":"PdpTitleSection","title".*"logo":null,"kicker":null,"overviewItems"', html)
            name = name_list[0]
            name = name[41:-43]
            print(name)
        except:
            pass
        #find price
        try:
            price_pattern = r'{"__typename":"QualifiedDisplayPriceLine","price"(.*?),"accessibilityLabel"'
            price_list = re.findall(price_pattern, html)
            price = price_list[0]
            price = price[6:-4]
            if not price[0].isdigit():
                price=price[1:]
            print(price)
        except:
            pass
        # find average rating
        try:
            average_rating = r'"overallRating"(.*?),"seeAllReviewsButton"'
            avg_rating_list = re.findall(average_rating, html)
            avg_rating = avg_rating_list[0]
            avg_rating = avg_rating[1:]
            #if not avg_rating[0].isdigit():
               # avg_rating=avg_rating[1:]
            print(avg_rating)
        except:
            pass
        #find number of ratings
        try:
            number_ratings = r'"starRating":\d+(\.\d+)?,"reviewCount"(.*?),"posterPictures"'
            number_ratings_list = re.findall(number_ratings, html)
            number_ratings = number_ratings_list[-1]
            number_ratings = number_ratings[1]
            number_ratings = number_ratings[1:]
            print(number_ratings)
        except:
            pass
        #find description
        try:
            description_pattern = r'"htmlDescription":{"__typename":"ReadMoreHtml","recommendedNumberOfLines":5,"htmlText"(.*?)","readMoreButton"'
            description_list = re.findall(description_pattern, html, re.DOTALL)
            description = description_list[0]
            description = description[2:]
            print(description)
        except:
            pass
        finally:
            pass
        
        #append values to rows
        rows.append([link, name, price, avg_rating, number_ratings, description])
    browser.quit()
    #write data to csv after finishing all iterations
    with open("scrapped_data", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

data = ['link', 'name', 'price', 'avg_rating', 'number_ratings', 'description']

# Open (or create) the CSV file in write mode
with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)

    # Write the data
        writer.writerow(data)   

def wait_random_time():
    time.sleep(random.randint(10, 20))

if __name__ == '__main__':
    webscraping()

