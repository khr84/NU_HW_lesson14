import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup

class AUTO_NEWS:

    def __init__(self):
        self.domain = 'https://motor.ru'
        self.cnt = 0
        self.news = []
        self.dir = os.path.join(os.getcwd(), "news_data")
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

    def get_news(self, dt):
        url = f'{self.domain}/pulse/{dt}'
        response = requests.get(url)

        # print(url)
        # print(response.status_code)

        soup = BeautifulSoup(response.text, 'html.parser')
        link_list = soup.findAll('a', class_ = 'jsx-353754120 link QUieMngm jsx-1839251063 link')
        self.cnt = len(list(link_list))
        # print(f'Count news {len(list(link_list))}')

        for link_item in link_list:
            dict_new = {}
            link_text = link_item.find('div', class_ = 'jsx-1959323720 Uc8vv_RT jsx-1839251063 headline').text
            link_date = link_item.find('div', class_ ='jsx-1959323720 _I0wYzqX').text
            dict_new['news_text'] = link_text
            dict_new['news_date'] = link_date
            dict_new['news_link'] = f'{self.domain}{link_item.get("href")}'
            url = f'{self.domain}{link_item.get("href")}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            link_img = soup.find('img', class_ = 'sX8xPdQU')
            print(link_img)
            self.news.append(dict_new)
        with open(os.path.join(self.dir,'news_file.txt'), 'w', encoding='utf8') as f:
            f.write(str(self.news))
        return self.news


if __name__ == '__main__':
    date_in = ''
    end_loop = False
    news_class = AUTO_NEWS()
    while not end_loop:
        try:
            datetime.strptime(date_in, '%Y/%m/%d')
            end_loop = True
        except:
            date_in = input('Введите дату за которую необходимы новости в формате YYYY/MM/DD: ')
    news = news_class.get_news(date_in)