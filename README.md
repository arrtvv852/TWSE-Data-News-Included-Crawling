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
- **Feature.verify():**
  Check if attributes data, target, dataset of Feature object reasonable. Print reason if not unreasonable.
- **Feature.Reset(n, date, data):**
  Give another set of inputs n, date, and data. (new input should also follow the format or might lead to errors)
- **Feature.AddLabel(n_day):**
  Add additional features corresponding to the given n_day value. (ex. 10 days Simple Moving Average, 10 days ...)
- **getSMA(n, close):
  given n days closing price (close), calculate the n-days Simple Moving Average and add as feature self.SMA.
- **Feature.getWMA(n, close)**
  given n days closing price (close), calculate the n-days Weighted Moving Average and add as feature self.WMA.
- **Feature.M(n, close, low, high):**
  given n days closing price (close), highest price (high), and lowest price (low), calculate the n-days Momentum value and add as feature self.M.
- **getK(close, low, high):**
  given current closing price (close), highest price (high), and lowest price (low), calculate the Stochastic-K value and add as feature self.K.
- **getD(n, close, low, high):**
  given n days closing price (close), highest price (high), and lowest price (low), calculate the n-days Stochastic-D value and add as feature self.D.
-- **getRSI(n, close):**
  given n days closing price (close), calculate the n-days Related Strengh Index and add as feature self.RSI.
-- **getMACD(close, long = 26, short = 12):
  given L days closing price (close) and parameters long-L and short-S (L>S), calculate the n-days Moving Average Convergence Divergence and add as feature self.MACD.
-- **getLW(n, close, low, high):**
  given n days closing price (close), highest price (high), and lowest price (low), calculate the n-days Larry William's R value and add as feature self.LW.
-- **getAD(close, low, high):
  given current closing price (close), highest price (high), and lowest price (low), calculate the A/D (Accumulation/Distribution) Oscillator value and add as feature self.AD.
-- **getCCI(n, close, low, high):**
  given n days closing price (close), highest price (high), and lowest price (low), calculate the n-days Commodity Channel Index value and add as feature self.CCI.
  
## class TrainGenerate
Load the stock data you just download by Download.py and transform it to ML training data format(.csv).
### Input
- **file_name (str)**
  Give the file name you download by Download.py (with the format like 'Stock-2468days-to-20190521.txt')
- **start (str)**
  The start date you want to generate training data (with format "YYYYMMDD" or "YYYY-MM-DD" or "YYYY/MM/DD", and shold be included in your txt file)
- **end (str)**
  The end date you want to generate training data (with format "YYYYMMDD" or "YYYY-MM-DD" or "YYYY/MM/DD", and shold be included in your txt file)
- **N (list)**
  Default with N = [10, 30], the list including the n-days parameters you want features in your training data.

### Functions
-- **loadfile(file_name):**
  Give the file name you download by Download.py, read it and return with a Data Frame(with the format like 'Stock-2468days-to-20190521.txt')
-- **Set_param(self, start, end, N):**
  Reset the parameters start, end, and N (please reference in inputs of class TrainGenerate).
-- **generate()**
  Generate the desired training data with given parameters Data Frame as self.Data.
-- **save()**
  Save the data you just generated as "20090901-to-20180831-training".

(continue...)


