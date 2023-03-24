import requests
from bs4 import BeautifulSoup
from aiogram import types, executor, Bot, Dispatcher
from dotenv import dotenv_values
import logging
import asyncio
from markup import main_button_inline, main_button_game

logging.basicConfig(level=logging.INFO)

confing = dotenv_values('.env')
bot = Bot(confing['token'])
dp = Dispatcher(bot)

time_sleep = 2


@dp.message_handler(commands='start')
async def hi(message: types.Message):
    await message.answer("HI" + "  " + message.from_user.first_name)
    await asyncio.sleep(time_sleep)
    await message.answer("Я бот для поиска игр 😎: ")
    await asyncio.sleep(time_sleep)
    await message.answer("Самое главное меню", reply_markup=main_button_inline)


@dp.callback_query_handler(lambda x: x.data == 'раздел')
async def razdel(callback: types.CallbackQuery):
    await callback.message.answer('начинаю парсинг бесплатных игр🎮')

    changing_msg = await callback.message.answer("""⏳ Авторизация... 0%
    🟩⬜⬜⬜⬜⬜⬜⬜⬜⬜""")
    await asyncio.sleep(1)
    await changing_msg.edit_text(text="""⏳ Поиск данных... 36%
    🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜""")
    await asyncio.sleep(1)
    await changing_msg.edit_text(text="""⏳ Проверка материала... 64%
    🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜""")
    await asyncio.sleep(1)
    await changing_msg.edit_text(text="""⏳ Отправка материала... 92%
    🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜""")
    await asyncio.sleep(1)
    await changing_msg.edit_text(text="""⏳ Получен материал... 100%⏳
    🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩""")

    #бесплатные игры
    url = "https://iwant.games/bestgames-pc/"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    page_count = int(soup.find_all("a", {"class": "page-numbers"})[-2].text)

    for i in range(1, page_count + 1):
        logging.info(f'Обработка {i} страницы')
        url = f"https://iwant.games/besplatnye-igry/page/{i}/"
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        # game = soup.select(".game")
        game_free = soup.find_all('article', class_='game free')
        for i in game_free:
            nic = i.select("h2 > a")[0].text
            number_data = i.select(".date")[0].text
            photo = i.find("a", class_="game__img").find("img").get("src")
            silka = i.find("a", class_="game__img").get("href")

            await asyncio.sleep(2)

            #бесплатные игры
            await bot.send_photo(callback.message.chat.id, photo,
                caption="<b>" + "Название игры:" + "  " + nic + "</b>\n<i>" + "Год выхода игры:" + "  " +
                number_data + "\n" + "Сылка на сайт:" + "  " + f"</i><a href='{silka}'>Ссылка на сайт</a>",
                parse_mode='html')


@dp.callback_query_handler(lambda x: x.data == 'популярные игры')
async def search_games(callback: types.CallbackQuery):
    await callback.message.answer("начинаю парсинг популярные игр🎮")
    changing_msg = await callback.message.answer("""⏳ Авторизация... 0%
    🟩⬜⬜⬜⬜⬜⬜⬜⬜⬜""")
    await asyncio.sleep(1)
    await changing_msg.edit_text(text="""⏳ Поиск данных... 36%
    🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜""")
    await asyncio.sleep(1)
    await changing_msg.edit_text(text="""⏳ Проверка материала... 64%
    🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜""")
    await asyncio.sleep(1)
    await changing_msg.edit_text(text="""⏳ Отправка материала... 92%
    🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜""")
    await asyncio.sleep(1)
    await changing_msg.edit_text(text="""⏳ Получен материал... 100%⏳
    🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩""")

    url = "https://iwant.games/bestgames-pc/"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    page_count = int(soup.find_all("a", {"class": "page-numbers"})[-2].text)

    for i in range(1, page_count + 1):
        url = f"https://iwant.games/bestgames-pc/page/{i}/"
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        game = soup.select(".game")
        for i in game:
            name = i.select("h2 > a")[-1]
            name = list(name)[0]
            foto = i.find("a", class_="game__img").find("img").get("src")
            data = i.select(".date")[0].text.strip()
            link = i.find("a", class_="game__img").get("href")

            await asyncio.sleep(2)

            # популярные игры
            await bot.send_photo(callback.message.chat.id, foto,
                caption="<b>" + "Название игры:" + "  " + name + "</b>\n<i>" + "Год выхода игры:" + "  " +
                data + "\n" + "Сылка на сайт:" + "  " + f"</i><a href='{link}'>Ссылка на сайт</a>",
                parse_mode='html')

if __name__ == '__main__':
    executor.start_polling(dp)