# Line Travel 機票比價爬蟲✈️ (Air ticket scraper)
## 前言(Introduction)
當初會想要做機票比價爬蟲的起心動念是因為最近有想要出國玩，但也同時希望能省機票錢，剛好朋友傳了 Line Travel 快速比價找出便宜機票網頁，所以想說為何不來寫個機票爬蟲小程式！
加上 Expedia、Skyscanner 這種機票比價網要抓資料的話，可能會比較容易被擋或有雷要踩，所以就試著在 Line Travel 爬想要的便宜機票資料。接著，把機票資料存到 Google Sheet 雲端做備份；最後，把前三筆最便宜的航空公司機票組合/價格/兩人總價/購買連結用 Line Notify 回傳，這樣隨時可以把握最便宜的機票跟航空公司優惠組合啦！

## 功能(Function) 
1. 從[Line Travel](https://travel.line.me/flights)網頁來爬取最新的機票資料 (Scraping Air Ticket Prices)
2. 把爬取的機票資料存成`CSV`檔到本地端 (Saving Air Ticket Price Data as CSV)	
3. 將航空公司機票價格資料上傳至Google Sheets (Uploading Air Ticket Price Data to Google Sheets)
4. 透過 Line Notify 定期傳最低價格的前3家航空公司的通知 (Regular Notifications via Line Notify: Top 3 Airlines with Lowest Prices)

## 事前準備(Prerequisites)
1. 需要安裝 `selenium`、`BeautifulSoup4`、`lxml`、`pandas`、`pygsheets` 和 `schedule` 套件
2. `selenium`、`BeautifulSoup4`和`lxml` 套件是用來爬取機票和解析資料用
3. `pandas`套件是把資料轉成二維並且簡單視覺化用
4. `pygsheets`套件是把資料存到`Google Sheet`，但需要先到 `Google Cloud` 串接`Google Sheet API`，詳細可參考這位大大的[教學](https://www.maxlist.xyz/2018/09/25/python_googlesheet_crud/)，裡面有詳細說明如何 用 Python 連結 Google Sheet API！:)
5. `schedule` 套件是用來執行定時排程任務用的，有多餘的時間/金錢可以選擇部署到雲端上，但其實沒有部署到雲上，也可以把程式改寫成你想要的格式後，直接在本地端執行 `air_ticket_scraper.ipynb` 或是用 CMD 執行 `air_ticket_scraping_main.py` 檔案，只要不把程式關掉就可以一直執行排程功能的！

## 待優化項目(Functions to be optimized) 
  1. 把抓下來的航空公司機會組合資料 URL 轉成 Short URL，解決 Line Notify 字數限制的問題。
  2. 如果預算夠的話，把它部署到雲端上，就可以固定某個時間傳最新的機票優惠方案。

## 參考資料(Reference)
1. [Python 串接 GoogleSheet 新增、讀取、更新和刪除](https://www.maxlist.xyz/2018/09/25/python_googlesheet_crud/)
2. [[爬蟲實戰] 如何抓取廉價航空的機票價格 – 以酷航為例?](https://www.youtube.com/watch?v=gCd3Fh9w3Do)
3. [【Python 網頁爬蟲 #2】透過 pygsheets 操作 google sheet API，讓我們的資料能同步更新至雲端 google sheet 表格 (內含範例程式碼)](https://www.wongwonggoods.com/all-posts/python/python_web_crawler/python-pygsheets/)
4. [Python 一個 line notify，通知今天氣溫。](https://molly1024.medium.com/python-%E4%B8%80%E5%80%8B-line-notify-%E9%80%9A%E7%9F%A5%E4%BB%8A%E5%A4%A9%E6%B0%A3%E6%BA%AB-a7e6fdb08543)
