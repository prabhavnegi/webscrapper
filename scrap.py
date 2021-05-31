import cloudscraper as cs
import pandas as pd
from bs4 import BeautifulSoup
from mysql.connector import connect, Error

scraper = cs.create_scraper()
driver = scraper.get('https://bank-code.net/')

soup = BeautifulSoup(driver.content,'html.parser')

data = []
user = ## add your username
password = ## add password of the db


for row in soup.find('table',class_='table').find_all('tr'):
    temp = [x.text for x in row.find_all('td')]
    data.append(temp)
    
for i in range(len(data[0])):
    x=data[0][i].replace(' ','_')
    data[0][i]=x
    

df = pd.DataFrame(data[1:], columns=data[0])

with open('swiftcodeTable.txt','w') as fs:
    df.to_csv(fs,sep='\t',header=True,index=False)
fs.close()

try :
    cnx = connect(user=user, password=password, host='localhost',database='swiftcode')
except Error as err :
    print('Connection Failed')
    print(err)

cursor = cnx.cursor()

cols = ",".join([str(i) for i in df.columns.tolist()])

try :
    query = "TRUNCATE TABLE swiftcode"
    cursor.execute(query)
    for index,row in df.iterrows():
        query = "INSERT INTO swiftcode "+"("+cols+") "+"VALUES (%s,%s,%s,%s)"
        cursor.execute(query,tuple(row))
    cnx.commit()
    cursor.close()
    cnx.close()
    print('Added to database Successfuly')
except:
    print('Inserting to DB failed')
    if Error :
        print(Error)
    cnx.rollback()
    cursor.close()
    cnx.close()


