import asyncio
from aiogram import types
from config import dp
from scraper.news_scraper import NewsScraper


async def scrape_news(call: types.CallbackQuery):
    scraper = NewsScraper()
    # for i in range(1, 6):
    #     url = f"https://www.prnewswire.com/news-releases/news-releases-list/?page={i}&pagesize=25"
    #     html = await scraper.get_html(url)

    pages = []
    throttler = asyncio.Semaphore(5)
    for i in range(1, 25):
        url = f"https://www.prnewswire.com/news-releases/news-releases-list/?page={i}&pagesize=25"
        task = asyncio.create_task(scraper.get_html(url))
        pages.append(task)
    await asyncio.gather(*pages)

    data = scraper.links
    for url in data[:4]:
        await call.message.answer(
            f"{NewsScraper.BASE_URL}{url}",
        )


def register_news_handlers(dp):
    dp.register_callback_query_handler(scrape_news, lambda c: c.data == "news")