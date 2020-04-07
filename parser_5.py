import bs4
import logging
import random
# import requests
import time
import threading
from openpyxl import Workbook
from requests_html import HTMLSession


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('PARSING')


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        ended_at = time.time()
        elapsed = round(ended_at - started_at)
        print('')
        print(f'Time run func {elapsed} sec.')
        return result
    return surrogate


class ParserPageOne(threading.Thread):

    def __init__(self, url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = HTMLSession()
        # self.session.headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        #     'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # }
        self.url = url
        self.data_for_record = []

    def loading(self, url):
        while True:
            try:
                result = self.session.get(url=url)
                break
            except Exception as exp:
                logger.exception(f'Ошибка в подключении {exp}')
                time.sleep(random.randint(2, 3))
        return result.text

    def parser_page(self, link):
        response = self.loading(link)
        self.parser_one_page(response)

    def parser_one_page(self, response):
        soup = bs4.BeautifulSoup(response, 'lxml')
        a_title = soup.select_one('h1.page-title.price-item-title').text
        code = soup.select_one('div.price-item-code').select_one('span').text
        img = soup.select_one('a.lightbox-img')
        if img:
            img_href = img.get('href')
        else:
            img_href = 'None'
        price = soup.select_one('span.current-price-value').get('data-price-value')

        logger.info('title - %s, code - %s, href - %s, price - %s', a_title, code, price, img_href)

        self.data_for_record = [a_title, code, price, img_href]

    def run(self):
        self.parser_page(self.url)


class ParserIndex:
    def __init__(self):
        self.session = HTMLSession()
        # self.session.headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        #     'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # }
        self.domain = 'https://technopoint.ru'
        self.data_links = []

    def loading(self, url):
        while True:
            try:
                result = self.session.get(url=url)
                break
            except Exception as exp:
                logger.exception(f'Ошибка в подключении {exp}')
                time.sleep(random.randint(2, 3))
        return result.text

    def parser_link(self, response):
        soup = bs4.BeautifulSoup(response, 'lxml')
        data = soup.select('div.n-catalog-product__main')
        for block in data[:10]:
            self._parse_block_link(block=block)
        return self.data_links

    def _parse_block_link(self, block):
        a_block = block.select_one('a.ui-link')
        a_link_block = a_block.get('href')
        link = self.domain + a_link_block

        logger.info('href - %s', link)

        self.data_links.append(link,)

    def run(self):
        url = f'{self.domain}/catalog/recipe/e351231ca6161134/2020-goda/'

        response = self.loading(url)
        links = self.parser_link(response=response)

        return links


@time_track
def main():
    wb = Workbook()
    ws = wb.active

    fields = ['Наименование', 'Код товара', 'Цена', 'Ссылка на картинку']

    parser_index = ParserIndex()
    data_links = parser_index.run()

    parser_page = [ParserPageOne(url) for url in data_links]

    for page in parser_page:
        page.start()

    for page in parser_page:
        page.join()

    ws.append(fields)
    for page in parser_page:
        ws.append(page.data_for_record)
    wb.save('parse.xlsx')

# Time run func 11 sec.
if __name__ == '__main__':
    main()
