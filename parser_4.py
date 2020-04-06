import bs4
import logging
import random
import requests
import time
import json
# from openpyxl import Workbook


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('PARSING')


class Parser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
            'Content-type': 'application/json',
            'Host': 'technopoint.ru',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://technopoint.ru/catalog/recipe/e351231ca6161134/2020-goda/no-referrer',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRF-Token': 'C3MkljI_Nl-nawfbqyMScHvp9AO_p4pNgPbDGGv5h7xfChajBHxPBdZbNJqbTyMoL6PHWc328inut6BIPb_Yyw==',
            'content-type': 'application/x-www-form-urlencoded',
            'Origin': 'https://technopoint.ru',
            'Content-Length': '1980',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': 'PHPSESSID=5f16b0a2868a95ea6c6ab261bd3320d1; current_path=9f2babc7a1c41abf4433dbbdb5e5de2547976428f75f87008654920923a5765ba%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A64%3A%22%7B%22city%22%3A%22b464725e-819d-11de-b404-00151716f9f5%22%2C%22method%22%3A%22geoip%22%7D%22%3B%7D; cartUserCookieIdent_v3=590ec75ad9693e16f7a7668046606f2833e474ad4b5228f2e1d36f395344d89aa%3A2%3A%7Bi%3A0%3Bs%3A22%3A%22cartUserCookieIdent_v3%22%3Bi%3A1%3Bs%3A36%3A%22a1741e5d-921b-332f-b77d-4bfc3be9c6a7%22%3B%7D; orderCheckoutIdent=43c4e9ffad76a8b8e16ced45f3af4d12b4bbdd9090a32d00f8c41ef70e0facd2a%3A2%3A%7Bi%3A0%3Bs%3A18%3A%22orderCheckoutIdent%22%3Bi%3A1%3Bs%3A36%3A%22a1741e5d-921b-332f-b77d-4bfc3be9c6a7%22%3B%7D; ipp_uid2=6b1hPPkhTYY9CTk1/Gk9YT+kaMTRMqMp1wSv+0w==; ipp_uid1=1586151875402; ipp_uid=1586151875402/6b1hPPkhTYY9CTk1/Gk9YT+kaMTRMqMp1wSv+0w==; rerf=AAAAAF6KwcYKfRMBA3ixAg==; phonesIdent=3777e7ea502623520af22afb1715f8aa4787a6d0486be9f231b3e63d1107fbada%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22phonesIdent%22%3Bi%3A1%3Bs%3A36%3A%226ad4990a-005c-4cfd-bbe4-9d3c378d673f%22%3B%7D; wishlist-id=76defe02cbb038f8ee794b4b157c24302c3bfeabf5652fdc65d28a320fb9eb61a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22wishlist-id%22%3Bi%3A1%3Bs%3A36%3A%229041b3d0-6661-49c4-86c5-57a9c72a23d9%22%3B%7D; viewed_products=61bf5e3cf5d9579789ba69a0bddb80c9fc33f704a57a66d488074ed1cf81011ca%3A2%3A%7Bi%3A0%3Bs%3A15%3A%22viewed_products%22%3Bi%3A1%3Ba%3A2%3A%7Bi%3A0%3Bs%3A36%3A%22aca1c017-6cc3-11ea-a20f-00155d03332b%22%3Bi%3A1%3Bs%3A36%3A%221bb514cf-6cc4-11ea-a20f-00155d03332b%22%3B%7D%7D; city_path=chelyabinsk; _csrf=57cb5a8fff030289982a9cb529ee3c1e756e20781519d25d9ef260825ea01d41a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22Ty256CyZq03A0l1XTJ3ZrQxdnAcPVF_w%22%3B%7D'
        }
        self.data = {"type":"price","containers":[{"id":"ajs-ad71d39f-cfe3-4ac4-a7b6-0efc4e735176","data":{"product":"1bb514cf-6cc4-11ea-a20f-00155d03332b"}},{"id":"ajs-6d24ae43-96c7-41ae-aa04-90f942060bfa","data":{"product":"aca1c017-6cc3-11ea-a20f-00155d03332b"}},{"id":"ajs-38b64c93-5ff9-457b-a909-d01b7c294c10","data":{"product":"def4e505-6cc3-11ea-a20f-00155d03332b"}},{"id":"ajs-a6ac8442-da8c-4937-8362-462c6cb4f0b9","data":{"product":"779315b3-6a56-11ea-a20f-00155d03332b"}},{"id":"ajs-1ef81274-4983-4330-b1f5-182f89eb113d","data":{"product":"65bae14c-6a56-11ea-a20f-00155d03332b"}},{"id":"ajs-cd51793f-c4c7-4d25-98c1-a6680cd1a944","data":{"product":"9571736c-6a56-11ea-a20f-00155d03332b"}},{"id":"ajs-067c8018-316f-4964-bd03-c284d69502fb","data":{"product":"d1357546-6cc4-11ea-a20f-00155d03332b"}},{"id":"ajs-093e338b-46bc-4f2c-b6b5-2df7368a51e4","data":{"product":"a2071eb1-6cc4-11ea-a20f-00155d03332b"}},{"id":"ajs-b24e35ff-7cb6-4c7e-8400-61dec3ee038f","data":{"product":"b8dccbec-6cc4-11ea-a20f-00155d03332b"}},{"id":"ajs-44ec4a81-7abf-48a4-a18b-2253076b5886","data":{"product":"83b41a2e-6cc4-11ea-a20f-00155d03332b"}},{"id":"ajs-01c39120-9614-4af7-bf5c-93e6c93c3c6b","data":{"product":"53a625b4-6cc5-11ea-a20f-00155d03332b"}},{"id":"ajs-f978449b-1223-49e3-98dc-edea9257abc4","data":{"product":"39f97f62-6cc5-11ea-a20f-00155d03332b"}},{"id":"ajs-ea43b12d-77fb-432b-8eb6-82132fa5b11a","data":{"product":"11208c6a-35c3-11ea-a20d-00155d03332b"}},{"id":"ajs-1f0409c8-d97f-46b5-abe9-245f8b35ef52","data":{"product":"a185ca45-35c2-11ea-a20d-00155d03332b"}},{"id":"ajs-1ea573a7-466b-404d-b6be-9a8f647cf775","data":{"product":"6f312f05-6cc5-11ea-a20f-00155d03332b"}},{"id":"ajs-52f2472d-0234-4e24-a0fc-6aef32f42dcb","data":{"product":"0c0eac7d-40c6-11ea-a20f-00155d03332b"}},{"id":"ajs-16f79c45-d9be-4555-8558-629b2277411a","data":{"product":"de47f9f8-40c5-11ea-a20f-00155d03332b"}},{"id":"ajs-3e21d4b5-f3dc-40cc-8e2b-e49968ce07d0","data":{"product":"96e2c63b-5d00-11ea-a20f-00155d03332b"}}]}

        self.url = 'https://technopoint.ru/ajax-state/price/'
        self.data_for_record = []
        self.data_links = []
        self.fields = ['Наименование', 'Код товара', 'Цена', 'Ссылка на картинку']

    def loading(self, url):
        while True:
            try:
                result = self.session.post(url=url, data=self.data)
                break
            except Exception as exp:
                logger.exception(f'Ошибка {exp}')
                time.sleep(random.randint(2, 5))
        return result

    def parser(self, response):
        print(response)

    def run(self):
        response_json = self.loading(self.url, )

        self.parser(response=response_json)

    # def save_file_xlsx(self):
    #     wb = Workbook()
    #     ws = wb.active
    #     ws.append(self.fields)
    #     for data in self.data_for_record:
    #         ws.append(data)
    #     wb.save('parse.xlsx')


if __name__ == '__main__':
    parser = Parser()
    parser.run()
    # parser.save_file_xlsx()
