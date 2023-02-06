import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup

domain = 'https://motor.ru'

date_in = ''
end_loop = False
while not end_loop:
    try:
        datetime.strptime(date_in, '%Y/%m/%d')
        end_loop = True
    except:
        date_in = input('Введите дату за которую необходимы новости в формате YYYY/MM/DD: ')

url = f'{domain}/pulse/{date_in}'

response = requests.get(url)
#print(response.status_code)

soup = BeautifulSoup(response.text, 'html.parser')
link_list = soup.findAll('a', class_ = 'jsx-353754120 link _2rfL2rmI jsx-2439255140 link')

print(soup.title.text)
print(f'Count news {len(list(link_list))}')

list_news = []
i = 0
for link_item in link_list:
    dict_new = {}
    time.sleep(3)
    responce = requests.get(f'{domain}{link_item.get("href")}')
    # print(f'{domain}{link_item.get("href")}')
    # print(responce.status_code)
    soup = BeautifulSoup(responce.text, 'html.parser')
    link_text = soup.find('h1', class_ = 'jsx-2784051990 _1colu_j_').text
    link_date = soup.find('div', class_ = '_1Lg_CbTX _240YeLMx').text
    dict_new['news_text'] = link_text
    dict_new['news_date'] = link_date
    dict_new['news_link'] = f'{domain}{link_item.get("href")}'
    list_news.append(dict_new)

# print(list_news)
with open('news_file.txt', 'a', encoding='utf8') as f:
    f.write(str(list_news))
