from parsel import Selector
import requests


class NewsScraper:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    MAIN_URL = 'https://www.prnewswire.com/news-releases/news-releases-list/'
    PLUS_URL = 'https://www.prnewswire.com'

    def parse_data(self):
        response = requests.get(self.MAIN_URL, headers=self.headers)
        if response.status_code > 400:
            return []
        # print(response.status_code)
        selector = Selector(text=response.text)
        title = selector.xpath('//title/text()').get()
        news_info = []
        all_news = selector.xpath('//div[@class="card col-view"]//a//h3/text()').getall()
        all_links = selector.xpath('//div[@class="card col-view"]/a/@href').getall()
        
        return all_links


if __name__ == '__main__':
    scraper = NewsScraper()
    print(scraper.parse_data())