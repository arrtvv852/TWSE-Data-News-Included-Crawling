# TWSE-Data-Scraping
Scrap stock related data from twse website. **(The program is under developing, so be aware of some possible incorrect value in it if you want to use it...)**

# Download.py
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
- 證券名稱 (Stock Name)
- 成交股數 (Volume of Shares Sold)
- 成交筆數 (Volume of Transactions)
- 成交金額 (Turnover)
- 開盤價 (Opening Price)
- 最高價 (Highest Price)
- 最低價 (Lowest Price)
- 收盤價 (Closing Price)
- 漲跌(+/-) (Ups Downs)
- 漲跌價差 (Ups & Downs Difference)
- 最後揭示買價 (Final Purchasing Price)
- 最後揭示買量 (Final Purchasing Amount)
- 最後揭示賣價 (Final Selling Price)
- 最後揭示賣量 (Final Selling Amount)
- 本益比 (PE ratio)
### reference
The source code of the Download is original based on finlab website (https://www.finlab.tw/categories/%E8%B2%A1%E5%A0%B1%E7%8B%97%E5%88%86%E6%9E%90/index.html)

# Features.py (Still developing...)
Generate stock training data with correspond features from the input of dictionary files obtained by Download.py.

## class Feature
Given the corresponding input, get some financial features added.
### Input
- **date (str)**
  with format "YYYYMMDD" or "YYYY-MM-DD" or "YYYY/MM/DD"
- **target (pandas.DataFrame)**
  with basic stock attributes columns including closing price, opening price, highest price, lowest price & volume of transactions
- **dataset (dictionary)**
  obtained by output of Download.py
- **features (iterable object)**
  including # corresponding to a feature - currently 0~9 developed, default: range(10)
- **n (int)**
  parameter to calculate the features means how many days previous than the target data day you want to observe
### Functions
- **Feature.verify:**
  Check if attributes data, target, dataset of Feature object reasonable. Print reason if not unreasonable.
(continue...)


