# -*- coding: utf-8 -*-
"""
Created on Tue May 21 20:45:13 2019

@author: user
"""

import pickle
import numpy as np
import requests
import time
from io import StringIO
import pandas as pd
import io
import datetime


class Crawl:
    def __init__(self, days, date, All = False):
        self.days = days
        self.date = date
        self.All = All
        self.Data = []
        
    def crawl_price(self, date):
        r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + str(date).split(' ')[0].replace('-','') + '&type=ALL')
        if r.text == '':
            print(str(date).split(' ')[0] + ' is holiday')
            return []
        else:
            print(str(date).split(' ')[0])
        if self.All:
            ret = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                            for i in r.text.split('\n') 
                                            if len(i.split('",')) == 17])), header=0)
        else:
            ret = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                            for i in r.text.split('\n') 
                                            if len(i.split('",')) == 17 and i[0] != '='])), header=0)
        ret['證券代號'] = ret['證券代號'].astype(str).str.replace('=','')
        ret['證券代號'] = ret['證券代號'].astype(str).str.replace('"','')
        ret = ret.set_index('證券代號')
        #ret["證券代號"] = ret.index
        ret['成交金額'] = ret['成交金額'].astype(str).str.replace(',','')
        ret['成交股數'] = ret['成交股數'].astype(str).str.replace(',','')
        ret['成交筆數'] = ret['成交筆數'].astype(str).str.replace(',','')
        ret['最後揭示買量'] = ret['最後揭示買量'].astype(str).str.replace(',','')
        ret['最後揭示賣量'] = ret['最後揭示賣量'].astype(str).str.replace(',','')
        ret['開盤價'] = ret['開盤價'].astype(str).str.replace(',','')
        ret['最高價'] = ret['最高價'].astype(str).str.replace(',','')
        ret['最低價'] = ret['最低價'].astype(str).str.replace(',','')
        ret['收盤價'] = ret['收盤價'].astype(str).str.replace(',','')
        ret['本益比'] = ret['本益比'].astype(str).str.replace(',','')
        
        ret[ret.開盤價 == '--'] = np.nan
        ret[ret.最高價 == '--'] = np.nan
        ret[ret.最低價 == '--'] = np.nan
        ret[ret.收盤價 == '--'] = np.nan
        
        ret.成交金額 = pd.to_numeric(ret.成交金額)
        ret.成交股數 = pd.to_numeric(ret.成交股數)
        ret.成交筆數 = pd.to_numeric(ret.成交筆數)
        ret.最後揭示買量 = pd.to_numeric(ret.最後揭示買量)
        ret.最後揭示賣量 = pd.to_numeric(ret.最後揭示賣量)
        ret.開盤價 = pd.to_numeric(ret.開盤價)
        ret.最高價 = pd.to_numeric(ret.最高價)
        ret.最低價 = pd.to_numeric(ret.最低價)
        ret.收盤價 = pd.to_numeric(ret.收盤價)
        ret.本益比 = pd.to_numeric(ret.本益比)
        
        return ret

    def download(self, break_time = 3):
        Data = {}
        self.date.replace("-", "")
        self.date.replace("/", "")
        year = int(self.date[:4])
        month = int(self.date[4:6])
        day = int(self.date[6:8])
        date = datetime.date(year, month, day)
        for d in range(self.days):
            D = date - datetime.timedelta(days = d)
            D = str(D).split(' ')[0].replace('-','')
            ret = self.crawl_price(D)
            if type(ret) == type(pd.DataFrame()):
                Data[D] = ret
            time.sleep(break_time)
        self.Data = Data
            
    def save(self):
        if self.All:
            name = 'All-'
        else:
            name = 'Stock-'
        name = name + str(self.days) + 'days-to-' + str(self.date)
        with io.open(name + '.txt', 'wb') as outfile:  
            pickle.dump(self.Data, outfile, protocol=pickle.HIGHEST_PROTOCOL)
            
def merge_file(file_list):
    File = {}
    for f in file_list:
        with io.open(f, 'rb') as outfile:  
            file = pickle.load(outfile)
        File.update(file)
    file_name = "Stock-"+str(len(File))+"days-to-"+str(max(np.array(list(File.keys())).astype(int)))
    with io.open(file_name + '.txt', 'wb') as outfile:  
        pickle.dump(File, outfile, protocol=pickle.HIGHEST_PROTOCOL)


print("How many days you want to scrap?")

D = int(input())
print("End date of your scraping period? (formate like '20190530')")
end = input()
while len(end)<8:
    print("please give a right format (formate like '20190530')...")
    end = input()
crawl = Crawl(D, end) #20170521
crawl.download()
crawl.save()
'''
Files = ["Stock-365days-to-20190521.txt", "Stock-365days-to-20180521.txt", "Stock-365days-to-20170521.txt", "Stock-365days-to-20160522.txt", "Stock-1460days-to-20150523.txt"]
merge_file(Files)'''
