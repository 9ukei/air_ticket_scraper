from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd

driver = webdriver.Chrome('/your_path/your_project/driver/chromedriver')
# url of Line Travel
air_ticket_url = '''
https://travel.line.me/flights/list?roundType=1&cabinClass=1&numOfAdult=2&numOfChildren=0&numOfBaby=0&linePointsRebateOnly=1&departureAirports=&departureCities=TPE&departureDates=1694390400000&arrivalAirports=&arrivalCities=OSA&departureAirports=&departureCities=OSA&departureDates=1694822400000&arrivalAirports=&arrivalCities=TPE
'''
# This number of seconds can be adjusted and increased according to the network delay problem. 
# It is recommended to stay at least 10 seconds or more.
driver.implicitly_wait(10)
driver.get(air_ticket_url)

# load more results to maximize the scraping
def page_scrolldown():
    try:
        for i in range(1,20):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(0.7)
    except:
        print('Check to see if any code is causing the error.')
        pass
page_scrolldown()

# view the html source code of the website
driver.page_source

html_source_code = driver.page_source

driver.close()

soup = BeautifulSoup(html_source_code, 'html.parser')

# check source code without tags
# print(soup.text)

# Display the total number of tickets found
record = soup.select_one('#__next > div.css-1cp3u8n.e1ugfpty0 > div:nth-child(2) > span')
print('搜尋的機票比價總筆數：',record.text)
#

time_loc_list = []

for time_loc_info in soup.select('#__next > div.css-1cp3u8n.e1ugfpty0 > div:nth-child(2)'):
    for tl in time_loc_info.select('.css-nkthol.ejxn77z1, .css-1qzlsgj.e1fe20ih2'):
        time = tl.text
        time_loc_list.append(time)

# Iterate through the elements in the time_loc_list, taking eight elements at a time to form a tuple, 
# and place these tuples into the tuple_list.
tuple_list = [tuple(time_loc_list[i:i+8]) for i in range(0, len(time_loc_list), 8)]
# print(tuple_list)

df_time = pd.DataFrame(tuple_list, columns=["起飛時間(出發)","起飛地點(出發)","抵達時間(出發)","抵達地點(出發)", "起飛時間(回程)","起飛地點(回程)", "抵達時間(回程)","抵達地點(回程)"])

result = []

# Depart/Arrived time + location (aboard/arrived)
for time_loc_info in soup.select('#__next > div.css-1cp3u8n.e1ugfpty0 > div:nth-child(2)'):
    for tl in time_loc_info.select('.css-1eowobi .css-j7qwjs'):
        time_loc = tl.text
        # print(time_loc)

air_ticket_info = soup.find_all(class_='css-1eowobi')

for ticket_info in air_ticket_info:
    # airline company
    airline = ticket_info.find(class_='css-84a4s3 e1fe20ih3').getText().strip()
    # air ticket provider
    ticket_site = ticket_info.find(class_='css-6x2xcr e1fe20ih2').getText().strip()   
    # ticket per price
    ticket_per_price = ticket_info.find(class_='css-iw7h7v ejxn77z0').getText().strip().replace(',', '')
    # total ticket price(2 ppl)
    total_price = ticket_info.find(class_='css-wycfi3 e1fe20ih3').getText().strip('')[9:].replace(',', '')
    # ticket purchase url
    ticket_purchase_url = 'https://travel.line.me/' + ticket_info.find('a').get('href')

    result.append((airline,ticket_site,int(ticket_per_price),int(total_price), ticket_purchase_url))

    #print(airline,ticket_site, ticket_per_price, total_price)

df = pd.DataFrame(result, columns=["航空公司", "購買網站", "一人價格(TWD)", "兩人總價(TWD)", "買票去！"])

# print(result) 

# If df1 and df2 have the same number of rows but different column names, you can use the concat function to merge them together. 
# The concat function allows you to concatenate multiple DataFrames along a specified axis. 
# In this case, you can choose to concatenate along the row axis.

ticket_full_info = pd.concat([df_time, df], axis=1)
ticket_full_info.align
ticket_full_info.index +=1
print(ticket_full_info.head(5))

now = datetime.datetime.now()
# If the month is not in the range of 10 to 12, then add a 0 after 1 to 9 months.
if now.month <= 10:
    date = str(now.year)+'0'+str(now.month)+str(now.day)
else:
    pass

# Current time
loc_dt = datetime.datetime.today() 
loc_dt_format = loc_dt.strftime("%Y/%m/%d %H:%M:%S")

# dataframe to csv
scapring_date = date
ticket_full_info.to_csv(f"{scapring_date}_air_ticket_full_info.csv")

import pygsheets

auth_file = "credentials.json"
gc = pygsheets.authorize(service_file = auth_file)

# sheet read by pygsheets
sheet_url = "https://docs.google.com/spreadsheets/yoursheeturlnamexxxxx" 
sheet = gc.open_by_url(sheet_url)

# Select by name
air_ticket_sheet_01 = sheet.worksheet_by_title("air ticket price comparison")

# Update values in the worksheet
# title_date = 'A1'
# air_ticket_sheet_01.update_values(title_date, [['9/11 ~ 9/16 台灣大阪來回機票即時比價報表' + '\n' + loc_dt_format]])
attributes = 'A1'
air_ticket_sheet_01.update_values(attributes, [["起飛時間(出發)","起飛地點(出發)","抵達時間(出發)","抵達地點(出發)", "起飛時間(回程)","起飛地點(回程)", "抵達時間(回程)","抵達地點(回程)","航空公司", "購買網站", "一人價格(TWD)", "兩人總價(TWD)", "買票去！"]])
start_record = 'A2'
# `df.values.tolist()` method can transform the data type `dataframe` to `list`
air_ticket_sheet_01.update_values(start_record, ticket_full_info.values.tolist())

import requests
import schedule
import time

def send_notification():

    # Read the data from Google Sheets
    data = air_ticket_sheet_01.get_all_records()

    # Extract the top three combinations of airlines with the lowest prices
    top_three_rows = data[:3]
    
    # Send LINE Notify notification   
    line_notify_url = "https://notify-api.line.me/api/notify"

    msg = '\n9/11 ~ 9/16 台灣大阪來回機票\n即時比價報表\n\n'
    for row in top_three_rows:
        msg += f'''💎航空公司: {row["航空公司"]}\n💎一人價格(TWD): {row["一人價格(TWD)"]}元\n💎兩人總價(TWD): {row["兩人總價(TWD)"]}元\n✈️哪次不衝了，買票去！\n{row["買票去！"]}\n\n'''
    
    payload={'message':{msg}}
    headers = {'Authorization': 'Bearer ' + 'yourtokenhere'}
    # Status code
    response = requests.request("POST", line_notify_url, headers=headers, data=payload)
    print(response.text)

# Set the time for sending notifications (Example: Every day at 10 AM)
schedule.every().day.at("10:00").do(send_notification)

# Infinite loop to keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
