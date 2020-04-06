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

    def loading(self):
        url = f'{self.domain}/catalog/recipe/e351231ca6161134/2020-goda/'
        while True:
            try:
                result = self.session.get(url=url)
                print(result.raise_for_status())
                break
            except Exception as exp:
                logger.exception(f'Ошибка в подключении {exp}')
                time.sleep(random.randint(2, 5))
                result = self.session.get(url=url, timeout=(25, 10))
                print(result.raise_for_status())
        return result.text

    def parser_page(self, text):
        soup = bs4.BeautifulSoup(text, 'lxml')
        data = soup.select('div.n-catalog-product__main')
        logger.info(f'Длинна списка - {len(data)}')
        for block in data:
            self.parse_block(block=block)

    def parse_block(self, block):
        a_text_block = block.select_one('a.ui-link')

        logger.info('%s', a_text_block.text)

        self.data_for_record.append(a_text_block.text,)

    def run(self):
        text = self.loading()
        self.parser_page(text=text)


    def save_file_xlsx(self):
        for data in self.data_for_record[:10]:
            ws.append((data,))
            logger.info('Записал - %s', data)
        wb.save('parse.xlsx')


if __name__ == '__main__':
    parser = Parser()
    parser.run()
    parser.save_file_xlsx()
