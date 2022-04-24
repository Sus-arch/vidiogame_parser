import requests
from bs4 import BeautifulSoup
import csv

CSV = 'games.csv'
HOST = 'https://zaka-zaka.com/'
URL = 'https://zaka-zaka.com/search/sort/sale.desc/offset/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    r.encoding = 'utf-8'
    new_url = r.url.replace('?', '')
    r = requests.get(new_url, headers=HEADERS, params=params)
    r.encoding = 'utf-8'
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='game-block')
    games = []
    for item in items:
        games.append(
            {
                'title': item.find('div', class_="game-block-name").get_text(),
                'price': item.find('div', class_='game-block-price').get_text().replace('c', 'рублей'),
                'discount': item.find('div', class_='game-block-discount').get_text(),
                'discount_sum': item.find('div', class_='game-block-discount-sum').get_text().replace('c', 'рублей'),
                'link': item.get('href')
            }
        )

    return games


def saver(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Name', 'Price', 'Discount', 'Discount amount', 'Link'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['discount'], item['discount_sum'], item['link']])


def parser():
    PAGENATION = int(input('Specify the number of pages to parse: ').strip())
    html = get_html(URL)
    n = 1
    if html.status_code == 200:
        games = []
        for page in range(0, PAGENATION * 10, 10):
            try:
                print(f'Parsing the page: {n}')
                html = get_html(URL, params=str(page))
                games.extend(get_content(html.text))
                saver(games, CSV)
            except UnicodeEncodeError:
                print('Encoding error')
                print(f'Data from page {n} not saved')
            n += 1
        print('Parsing completed')
    else:
        print('ERROR')


parser()

