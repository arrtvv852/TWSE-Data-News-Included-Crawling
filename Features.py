# -*- coding: utf-8 -*-
"""
Created on Tue May 21 20:45:13 2019

@author: user
"""

import pickle
import pandas as pd
import datetime
import copy
import io
import os


class Feature:
    def __init__(self, date, target, dataset, features = range(10), n = 10):
        self.date = date
        self.target = target
        self.features = features
        self.dataset = dataset
        
        self.n = n
        
        if self.verify():
            self.Reset(n, date, dataset)
        
        
    def verify(self):
        Pass = True
        reason = ''
        if type(self.date) != type('') or len(self.date) < 8:
            Pass = False
            reason = reason + 'Date format(ex."20180328") not satisfied; '
        if type(self.target) != type(pd.DataFrame([])):
            Pass = False
            reason = reason + 'Target format(DataFrame) not satisfied; '
        if type(self.dataset) != type({}) or len(self.dataset) < max(26, self.n):
            Pass = False
            reason = reason + 'Dataset format not satisfied; '
        if not Pass:
            reason = reason + 'Please Give Correct Input!'
            print(reason)
        return Pass
        
    def Reset(self, n, date, data):
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:8])
        time = datetime.date(year, month, day)
        dataset = {}
        i = 0
        cnt = 0
        while cnt < max(27, n+1):
            t = str(time-datetime.timedelta(i)).replace("-", "")
            i += 1
            if t in data.keys():
                dataset[t] = data[t]
                cnt += 1
        
        self.date = date
        self.n = n
        self.dataset = data
        
        self.close = pd.DataFrame({k:d['收盤價'] for k,d in dataset.items()})
        self.open = pd.DataFrame({k:d['開盤價'] for k,d in dataset.items()})
        self.high = pd.DataFrame({k:d['最高價'] for k,d in dataset.items()})
        self.low = pd.DataFrame({k:d['最低價'] for k,d in dataset.items()})
        self.volume = pd.DataFrame({k:d['成交股數'] for k,d in dataset.items()})
        
    def addLabel(self, n_day = 1):
        year = int(self.date[:4])
        month = int(self.date[4:6])
        day = int(self.date[6:8])
        time = datetime.date(year, month, day)
        future = str(time + datetime.timedelta(n_day)).replace("-", "")
        while future not in self.dataset.keys():
            year = int(future[:4])
            month = int(future[4:6])
            day = int(future[6:8])
            time = datetime.date(year, month, day)
            if time >= datetime.date.today():
                print("label not exist yet!")
                break
            else:
                future = str(time + datetime.timedelta(1)).replace("-", "")
        self.target["future_"+str(n_day)+"_price"] = self.dataset[future]["收盤價"]
        
    
    def getFeatures(self):
        for f in self.features:
            if f == 0:
                self.getSMA(self.n, self.close)
            elif f == 1:
                self.getWMA(self.n, self.close)
            elif f == 2:
                self.getM(self.n, self.close)
            elif f == 3:
                self.getK(self.close, self.low, self.high)
            elif f == 4:
                self.getD(self.n, self.close, self.low, self.high)
            elif f == 5:
                self.getRSI(self.n, self.close)
            elif f == 6:
                self.getMACD(self.close, long = 26, short = 12)
            elif f == 7:
                self.getLW(self.n, self.close, self.low, self.high)
            elif f == 8:
                self.getAD(self.close, self.low, self.high)
            elif f == 9:
                self.getCCI(self.n, self.close, self.low, self.high)
            else:
                print(f, "th feature not availible yet")
                
    def addFeature(self):
        for f in self.features:
            if f == 0:
                self.target["SMA"+str(self.n)] = self.SMA
            elif f == 1:
                self.target["WMA"+str(self.n)] = self.WMA
            elif f == 2:
                self.target["M"+str(self.n)] = self.M
            elif f == 3:
                if not("K" in self.target.keys()):
                    self.target["K"] = self.K
            elif f == 4:
                self.target["D"+str(self.n)] = self.D
            elif f == 5:
                self.target["RSI"+str(self.n)] = self.RSI
            elif f == 6:
                self.target["MACD"+str(self.n)] = self.MACD
            elif f == 7:
                self.target["LW"+str(self.n)] = self.LW
            elif f == 8:
                if not("AD" in self.target.keys()):
                    self.target["AD"] = self.AD
            elif f == 9:
                self.target["CCI"+str(self.n)] = self.CCI
                
        self.addLabel()
        self.addLabel(7)
                
        
    def getSMA(self, n, close):
        #Simple Moving Average
        self.SMA = close.iloc[:, :n].sum(axis = 1)/n
    
    def getWMA(self, n, close):
        #Weited Moving Average
        value = 0
        div = 0
        for i in range(n):
            value += close.iloc[:, :(n-i)].sum(axis = 1)
            div += n-i
        self.WMA = value/div
    
    def getM(self, n, close):
        #Momentum
        self.M = close.iloc[:, 0]-close.iloc[:, n-1]
    
    def getK(self, close, low, high):
        #Stochastic K
        self.K = (close.iloc[:, 0] - low.min(axis = 1)) / (high.max(axis = 1) - low.min(axis = 1))
    
    def getD(self, n, close, low, high):
        #Stochastic D
        if not(hasattr(self, "K")):
            self.getK(close, low, high)
        value = copy.copy(self.K)
        for i in range(n-1):
            value += (close.iloc[:, i+1] - low.iloc[:, (i+1):(i+n)].min(axis = 1)) / (high.iloc[:, (i+1):(i+n)].max(axis = 1) - low.iloc[:, (i+1):(i+n)].min(axis = 1))
        self.D = value / n
    
    def getRSI(self, n, close):
        #Relative Strength Index
        UP = 0
        DW = 0
        for i in range(n):
            value = close.iloc[:, i] - close.iloc[:, i+1]
            up = copy.copy(value)
            up[up<0] = 0
            dw = copy.copy(value)
            dw[dw>0] = 0
            UP += up
            DW -= dw
        self.RSI = 100 - 100/(1+UP/DW)
    
    def getMACD(self, close, long = 26, short = 12):
        #Moving Average Convergence Divergece
        EMA_long = close.iloc[:, :long].sum(axis = 1)/long
        k = 2/(long+1)
        for i in range(long):
            EMA_long = close.iloc[:, long-i-1]*k + EMA_long*(1-k)
        EMA_short = close.iloc[:, :short].sum(axis = 1)/short
        k = 2/(short+1)
        for i in range(short):
            EMA_short = close.iloc[:, short-i-1]*k + EMA_short*(1-k)
        self.MACD = EMA_short - EMA_long
    
    def getLW(self, n, close, low, high):
        #Larry Williams's R
        self.LW = (high.iloc[:, n-1] - close.iloc[:, 0])/(high.iloc[:, n-1] - low.iloc[:, n-1])
    
    def getAD(self, close, low, high):
        #A/D (Accumulation/Distribution) Oscillator
        self.AD = (high.iloc[:, 0] - close.iloc[:, 1])/(high.iloc[:, 0] - low.iloc[:, 0])
    
    def getCCI(self, n, close, low, high):
        #Commodity Channel Index
        Mt = (high.iloc[:, 0] + close.iloc[:, 0] + low.iloc[:, 0])/3
        value = 0
        for i in range(n):
            value += (high.iloc[:, i] + close.iloc[:, i] + low.iloc[:, i])/3
        SM = value/n
        value = 0
        for i in range(n):
            value += ((high.iloc[:, i] + close.iloc[:, i] + low.iloc[:, i])/3-SM).abs()
        D = value/n
        self.CCI = (Mt - SM)/0.015/D
        
class TrainGenerate:
    def __init__(self, file_name, start, end, N = [10, 30]):
        self.File = self.loadfile(file_name)
        self.Set_param(start, end, N)
        self.Data = pd.DataFrame([])
        
    def loadfile(self, file_name):
        with io.open(file_name, 'rb') as outfile:  
            File = pickle.load(outfile)
        return File
    
    def Set_param(self, start, end, N):
        start = str(start).split(' ')[0].replace('-','').replace('/','')
        end = str(end).split(' ')[0].replace('-','').replace('/','')
        reason = ""
        Pass = True
        if start not in self.File.keys():
            reason = reason + 'Start time incorrect!'
            Pass = False
        if end not in self.File.keys():
            reason = reason + 'End time incorrect!'  
            Pass = False
        if hasattr(N, "__iter__") and Pass:
            year = int(start[:4])
            month = int(start[4:6])
            day = int(start[6:8])
            Time = datetime.date(year, month, day)
            Time = Time - datetime.timedelta(max(26, max(N)))
            t1 = str(Time).replace("-", "")
            Time = Time - datetime.timedelta(1)
            t2 = str(Time).replace("-", "")
            Time = Time - datetime.timedelta(1)
            t3 = str(Time).replace("-", "")
            if t1 not in self.File.keys() and t2 not in self.File.keys() and t3 not in self.File.keys():
                reason = reason + 'Too less data downloaded!'
                Pass = False
        else:
            reason = reason + 'N is not iterable!'
            Pass = False
            
        if Pass:
            self.trainS = start
            self.trainE = end
            self.N = N
            print("Reset parameters successfully!")
        else:
            reason = reason + 'Please retry!'
            print(reason)
            
    def generate(self):
        year = int(self.trainS[:4])
        month = int(self.trainS[4:6])
        day = int(self.trainS[6:8])
        D = datetime.date(year, month, day)
        year = int(self.trainE[:4])
        month = int(self.trainE[4:6])
        day = int(self.trainE[6:8])
        end = datetime.date(year, month, day)
        while D <= end:
            print(str(D))
            date = str(D).replace('-','').replace('/','')
            while date not in self.File.keys():
                D = D + datetime.timedelta(1)
                date = str(D).replace('-','').replace('/','')
                if D > end:
                    break
            target = self.File[date]
            for n in self.N:
                F = Feature(date, target, self.File, n = n)
                F.getFeatures()
                F.addFeature()
                F.target["Date"] = date
            self.Data = pd.concat([self.Data, F.target])
            D = D + datetime.timedelta(1)

    def save(self):
        self.Data = self.Data.iloc[:, [0, 28, 26, 27] + list(range(1, 15)) + list(range(16, 26)) + list(range(29, len(self.Data.columns)))]
        col = ['stock_name', 'Date', 'future_1_price', 'future_7_price', 'shares_sold_volumne', 'transactions_volumne',
       'Turnover', 'opening', 'highest', 'lowest', 'closing', 'up_down', 'difference', 'final_buying_price',
       'final_buying_amount', 'final_selling_price', 'final_selling_amount', 'PE_ratio', 'SMA10', 'WMA10', 'M10', 'K',
       'D10', 'RSI10', 'MACD10', 'LW10', 'AD', 'CCI10', 'SMA30', 'WMA30',
       'M30', 'D30', 'RSI30', 'MACD30', 'LW30', 'CCI30']
        self.Data.columns = col
        self.Data.index.name = "stock_id"
        name = self.trainS+"-to-"+self.trainE+"-training"
        self.Data.to_csv(name + ".csv")




print("Please Give Input File Name")
file = input()
while not os.path.isfile(file):
    print("File not exist! Please Retry!")
    file = input()
print("Start date of your expected period? (formate like '20190530')")
start = input()
while len(start)<8:
    print("please give a right format (formate like '20190530')...")
    start = input()
print("End date of your expected period? (formate like '20190530')")
end = input()
while len(end)<8:
    print("please give a right format (formate like '20190530')...")
    end = input()
#GF = TrainGenerate("Stock-2468days-to-20190521.txt", "20090901", "20180831")
GF = TrainGenerate(file, start, end)
GF.generate()
GF.save()