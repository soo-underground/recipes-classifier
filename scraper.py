from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome('D:\curl\chromedriver.exe')

tags0=[] 
tags1=[]
tags2=[]
descriptions=[] 



df = pd.DataFrame({'Text':descriptions,'Tag 0':tags0,'Tag 1':tags1,'Tag 2':tags2}) 
df.to_csv('products.csv', index=False, encoding='utf-8')

for i in range (2,300):
    driver.get("..." % i)
    
    time.sleep(5)
    
    content = driver.page_source
    soup = BeautifulSoup(content)
    
    for a in soup.findAll('article', attrs={'class':'...'}):
        tag_all=a.find('div', attrs={'class':'...'})
        
        all_tags=tag_all.find_all('a')
        num_elem = len(all_tags)
        
        if num_elem > 0:
            tag0 = all_tags[0].text
        else:
            tag0 = ' '
        
        if num_elem > 1:
            tag1 = all_tags[1].text
        else: 
            tag1 = ' '
        
        if num_elem > 2: 
            tag2 = all_tags[2].text
        else:
            tag2 = ' '
        
        description=a.find_all('p')[1]
        tags0.append(tag0)
        tags1.append(tag1)
        tags2.append(tag2)
        
        descriptions.append(description.text)
    
    print('page %d processed' %i)
        
df = pd.DataFrame({'Text':descriptions,'Tag0':tags0,'Tag1':tags1,'Tag2':tags2}) 
df = df.replace(r'\n',' ', regex=True) 
df.to_csv('products.csv', index=False, encoding='utf-8', sep='|')