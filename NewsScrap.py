# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 22:12:37 2019

@author: user
"""



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re
import time
import pandas as pd



class ScrapNews:
    def __init__(self, ID, start, end):
        self.ID = ID
        self.start = start
        self.end = end
        
    def scrap(self):
        driver = webdriver.Chrome()
        driver.get('https://mops.twse.com.tw/mops/web/t05st01')
        driver.find_element_by_id("co_id").send_keys(self.ID)
        driver.implicitly_wait(30)
        
        Date = []
        Time = []
        Title = []
        Content = []
        for y in range(self.start, self.end+1):
            year = int(y)
            driver.find_element_by_id("year").clear()
            driver.find_element_by_id("year").send_keys(year)
            
            driver.find_element_by_xpath('//input[@value=" 查詢 "]').click()
            
            table = driver.find_element_by_class_name("hasBorder")
            
            rows = table.find_elements_by_tag_name("tr")
            for r in range(1, len(rows)):
                table = driver.find_element_by_class_name("hasBorder")
                rows = table.find_elements_by_tag_name("tr")
                try:
                    row = rows[r].find_element_by_tag_name("input")
                    ActionChains(driver).key_down(Keys.CONTROL).click(row).key_up(Keys.CONTROL).perform()
                    driver.switch_to_window(driver.window_handles[1])
                except:
                    continue
                time.sleep(1)
                table = driver.find_element_by_class_name("hasBorder")
                timeInfo = table.find_elements_by_tag_name("tr")[0]
                titleInfo = table.find_elements_by_tag_name("tr")[2]
                info = table.find_elements_by_tag_name("tr")[4]
                
                
                date = timeInfo.find_elements_by_class_name("odd")[1].text.replace(" ", "")
                t = timeInfo.find_elements_by_class_name("odd")[2].text.replace(" ", "")
                title = titleInfo.find_element_by_class_name("odd").text.replace(" ", "")
                content = re.sub(r"\n", "", info.find_element_by_class_name("odd").text)
                
                Date.append(date)
                Time.append(t)
                Title.append(title)
                Content.append(content)
                
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
                time.sleep(1)
                
        driver.close()
        self.data = pd.DataFrame({"Date": Date, "Time": Time, "Title": Title, "Content": Content})
        
    def save(self):
        self.data.to_csv(str(ID)+"_News.csv", index=False, encoding="utf_8_sig")
        
print("Stock ID:")
while True:
    ID = input()
    try:
        ID = int(ID)
        break
    except:
        print("Input not correct, please give an integer!")
        
print("Start Year (In Republic Era with format like\"103\", 81~current:")
ey = int(time.ctime()[-4:])-1911
sy = 81
while True:
    start = input()
    try:
        start = int(start)
        if start < sy:
            print("Too many years ago!(81~current year)")
        elif start > ey:
            print("It just "+str(ey)+" Republic Era now!")
        else:
            break
    except:
        print("Input not correct, please give an integer!")
        
print("End Year (In Republic Era with format like\"108\", 81~current:")
ey = int(time.ctime()[-4:])-1911
sy = 81
while True:
    end = input()
    try:
        end = int(end)
        if start > end:
            print("End year must not less than start year("+str(start)+")")
        elif end < sy:
            print("Too many years ago!(81~current year)")
        elif end > ey:
            print("It just "+str(ey)+" Republic Era now!")
        else:
            break
    except:
        print("Input not correct, please give an integer!")
        
sn = ScrapNews(ID, start, end)
sn.scrap()
sn.save()
