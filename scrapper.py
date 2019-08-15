# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import datetime

month_to_num = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
currentMonth = datetime.datetime.today().month
currentYear = datetime.datetime.today().year


def get_soup():

    browser = webdriver.Chrome(executable_path='C:/.../chromedriver.exe')#ADD PATH TO THE chromedriver.exe file
    browser.get('https://www.slbenfica.pt/pt-pt/jogos/calendario')

    # Get inicial scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.find_element_by_tag_name("body").send_keys(u'\ue010')
        # Wait to load page
        time.sleep(0.5)
        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    source = browser.page_source.encode('utf-8').strip()

    b_soup = BeautifulSoup(source.decode('utf-8'), 'html.parser')
    browser.quit()
    return b_soup


def get_info(b_soup):
    list_matches = []
    calendar = b_soup.find('div', attrs={'class':'row calendar-items-container'})
    matches = calendar.find_all('div', attrs={
        'class': ['calendar-item col-xs-12 scheduled', 'calendar-item col-xs-12 unscheduled']})

    for match in matches:
        match.find('div', attrs={'class': 'calendar-date'})
        print(match.find('div', attrs={'class': 'calendar-date'}).text)
        date = change_date(match.find('div', attrs={'class': 'calendar-date'}).text[4:])
        hour = match.find('div', attrs={'class': 'calendar-match-hour'}).text
        competition = match.find('div', attrs={'class': 'calendar-competition'}).text
        teams = match.find('div', attrs={'class': 'titleForCalendar'}).text
        key = '-'.join((competition, teams))

        list_matches.append([teams, date, '', date, '', 'TRUE', key, '', 'FALSE'])
    return list_matches


def change_date(text):
    date = text.split()
    print(date)
    month = month_to_num.index(date[1]) + 1

    if month >= currentMonth:
        year = currentYear
    else:
        year = currentYear + 1

    str_month = str(month)
    if len(str_month) == 1:
        str_month = ''.join(('0', str_month))

    return ' '.join((date[0], str_month, str(year)))


soup = get_soup()
list_matches = get_info(soup)
df = pd.DataFrame(list_matches, columns=['Subject', 'Start Date', 'Start Time', 'End Date', 'End Times', 'All Day Event', 'Description', 'Location', 'Private'])
df.to_csv('C:\Users\luiz4\Desktop\test.csv', index = None, header=True)# ADD THE PATH YOU WANT TO CREATE THE CSV FILE
#print(df)

print('FINISHED')
