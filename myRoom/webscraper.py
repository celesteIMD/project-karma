import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

def get_rooms():

    # create list of rooms to store data in
    room_list = []

    # access carleton web content using Google Chrome browser
    browser = webdriver.Chrome()
    url = 'https://booking.carleton.ca/index.php?p=RoomSearch&r=1'
    browser.get(url)

    for i in range(1, 9): #collect result from each page

        # wait for content to load
        time.sleep(5)

        #scrape data
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        tbody = soup.find_all('tbody') #finds all tables

        # looks through table to access relevant data
        # column 0 is building name, column 2 is room number
        for table in tbody:
            tr_tags = table.find_all('tr')
            for tr in tr_tags:
                td_tags = tr.find_all('td')
                if len(td_tags) != 1:
                    #for some reason there is a login/loading table on this page.
                    #this 'if' condition prevents collecting data from that table, since those rows only have 1 column
                    data = td_tags[0].text + "?" + td_tags[2].text
                    #print(data)
                    room_list.append(data)
        browser.find_element(By.CLASS_NAME, "imgNextArrow").click() #go to next page

    browser.close()
    return room_list

def get_buildings():
    # access carleton web content using Google Chrome browser
    browser = webdriver.Chrome()
    url = 'https://booking.carleton.ca/index.php?p=RoomSearch&r=1'
    browser.get(url)

    # wait for content to load
    time.sleep(5)

    html = browser.page_source
    browser.close()

    # scrape data
    soup = BeautifulSoup(html, 'html.parser')
    b_list = soup.find('select', id='cboLocation')  # collects list of all buildings

    buildings = []

    # collects list of buildings from location drop down
    listitems = b_list.find_all('option')
    for option in listitems:
        building_name = option.text
        if building_name == "•M - Carleton Main Campus":
            continue
        building_name = building_name[9:]
        buildings.append(building_name)
    return buildings