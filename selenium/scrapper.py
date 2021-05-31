import os
from selenium import webdriver
import pandas as pd

driver = os.getcwd()+'\chromedriver'

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
browser = webdriver.Chrome(executable_path=driver,chrome_options=options)

try:
    browser.set_page_load_timeout(10)
    browser.get('https://bank-code.net/')
except TimeoutException as ex:
    print("Exception has been thrown. " + str(ex))
    browser.close()


# exctracting title and description
title = browser.title
description = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]').text

link_dict = {}
table = []

# exctracting all the link for each alphabest
for link in browser.find_elements_by_css_selector('.nav-pills > li > a'):
    link_dict[link.text] = link.get_attribute('href')


# exctracting table of swift codes    
data_table = browser.find_element_by_xpath('/html/body/div[1]/div[4]/div[5]/div/div/table') 

for table_row in data_table.find_elements_by_tag_name('tr'):
    temp = [x.text for x in table_row.find_elements_by_tag_name('td')]
    table.append(temp)
  
# the list of table data is converted to Pandas Data Frame
df = pd.DataFrame(table[1:], columns = table[0])
df.set_index('No')



# The values exctracted are saved in a .txt file
with open('swiftcode.txt','w') as fs:
    fs.write(title+'\n'+description+'\n')
    fs.write("Link: \n")
    fs.write('\n'.join(str(x) for x in link_dict.items()))
    fs.write('\n\nSwift Code Table:\n\n')
    df.to_csv(fs,sep='\t',header=True,index=False)
fs.close()
browser.close()
# end of program
    
    

