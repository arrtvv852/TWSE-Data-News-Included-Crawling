# TWSE-Data-Scraping
Scrap stock related data from twse website.

## Download.py
Excute and give the period you want to download from (http://www.twse.com.tw/en/).
### input
- days (int or float)
- end date (str with format "YYYYMMDD" or "YYYY-MM-DD" or "YYYY/MM/DD")
ex. scaping stocks data within 2018/05/22 to 2019/05/21
  -> days = 365, end date = "20190521"
### output
output data with the dictionary data as a txt file.
structure: {"20190521": DataFrame(), "20190520": DataFrame(), ..}
DataFrame with the columns:
- 證券名稱
- 成交股數
- 成交筆數
- 成交金額
- 開盤價
- 最高價
- 最低價
- 收盤價
- 漲跌(+/-)
- 漲跌價差
- 最後揭示買價
- 最後揭示買量
- 最後揭示賣價
- 最後揭示賣量
- 本益比
### reference
The source code of the Download is original based on finlab website (https://www.finlab.tw/categories/%E8%B2%A1%E5%A0%B1%E7%8B%97%E5%88%86%E6%9E%90/index.html)
