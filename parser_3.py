import bs4
import logging
import random
import requests
import time
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('PARSING')


class Parser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        }
        self.domain = 'https://technopoint.ru'
        self.data_for_record = []
        self.data_links = []
        self.fields = ['Наименование', 'Код товара', 'Цена', 'Ссылка на картинку']

    def loading(self, url):
        while True:
            try:
                result = self.session.get(url=url)
                break
            except Exception as exp:
                logger.exception(f'Ошибка в подключении {exp}')
                time.sleep(random.randint(2, 5))
        return result.text

    def parser_link(self, text):
        soup = bs4.BeautifulSoup(text, 'lxml')
        data = soup.select('div.n-catalog-product__main')
        for block in data[:10]:
            self._parse_block_link(block=block)

    def _parse_block_link(self, block):
        a_block = block.select_one('a.ui-link')
        a_link_block = a_block.get('href')

        link = self.domain + a_link_block

        code, img_href, price = self.parser_page(link)

        self.data_for_record.append(
            [
                a_block.text,
                code,
                price,
                img_href,
            ],
        )

    def parser_page(self, link):
        response = self.loading(link)
        return self._parser_product_code(response)

    def _parser_product_code(self, response):
        soup = bs4.BeautifulSoup(response, 'lxml')

        code = soup.select_one('div.price-item-code').select_one('span').text

        img = soup.select_one('a.lightbox-img')
        if img:
            img_href = img.get('href')
        else:
            img_href = 'None'

        price = soup.select_one('span.current-price-value').get('data-price-value')

        logger.info('Code - %s, href - %s, price - %s', code, img_href, price)

        return code, img_href, price

    def run(self):
        url = f'{self.domain}/catalog/recipe/e351231ca6161134/2020-goda/'
        text = self.loading(url)
        self.parser_link(text=text)

    def save_file_xlsx(self):
        ws.append(self.fields)
        for data in self.data_for_record:
            ws.append(data)
        wb.save('parse.xlsx')

# time run - 85-90 sec
if __name__ == '__main__':
    parser = Parser()
    parser.run()
    parser.save_file_xlsx()

