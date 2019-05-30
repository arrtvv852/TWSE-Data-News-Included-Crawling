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


class Feature:
    def __init__(self, date, target, dataset, features = range(10)):
        self.date = date
        self.target = target
        self.dataset = dataset
        self.features = features
        
        self.n = 10
        
        if self.verify():
            self.Reset(self.n, self.date, self.dataset)
        
        
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
        if Pass:
            print("Input Verified!")
        else:
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
        while cnt < max(26, n):
            t = str(time-datetime.timedelta(i)).replace("-", "")
            i += 1
            if t in data.keys():
                dataset[t] = data[t]
                cnt += 1
                
        self.close = pd.DataFrame({k:d['收盤價'] for k,d in dataset.items()})
        self.open = pd.DataFrame({k:d['開盤價'] for k,d in dataset.items()})
        self.high = pd.DataFrame({k:d['最高價'] for k,d in dataset.items()})
        self.low = pd.DataFrame({k:d['最低價'] for k,d in dataset.items()})
        self.volume = pd.DataFrame({k:d['成交股數'] for k,d in dataset.items()})
    
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
                
    def getFile(self):
        return self.target
        
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
        self.Data = self.loadfile(file_name)
        self.Set_param(start, end, N)
        
    def loadfile(self, file_name):
        with io.open(file_name, 'rb') as outfile:  
            Data = pickle.load(outfile)
        return Data
    
    def Set_param(self, start, end, N = [10, 30]):
        start = str(start).split(' ')[0].replace('-','').replace('/','')
        end = str(end).split(' ')[0].replace('-','').replace('/','')
        reason = ""
        Pass = True
        if start not in self.Data.keys():
            reason = reason + 'Start time incorrect!'
            Pass = False
        if end not in self.Data.keys():
            reason = reason + 'Start time incorrect!'  
        if hasattr(N, "__iter__") and Pass:
            Pass = False
            year = int(start[:4])
            month = int(start[4:6])
            day = int(start[6:8])
            Time = datetime.date(year, month, day)
            Time = Time - datetime.timedelta(max(26, max(N)))
            t = str(Time).replace("-", "")
            if t not in self.Data.keys():
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


with io.open('onemonth.txt', 'rb') as outfile:  
        Data = pickle.load(outfile)
        
F = Feature("20190524", Data["20190524"], Data)
F.getFeatures()
F.addFeature()
test = F.getFile()