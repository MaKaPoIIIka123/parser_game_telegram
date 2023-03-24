from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_button_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("Мой профиль", callback_data='мой профиль'),
     InlineKeyboardButton("Раздел игр 🎮", callback_data='раздел')]
])

main_button_game = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("Бесплатные игры🎮", callback_data='бесплатные игры'),
     InlineKeyboardButton('Популярные игры🎮', callback_data='популярные игры')]
])