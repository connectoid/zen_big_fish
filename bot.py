import os
from time import sleep

from aiogram import Bot, Dispatcher, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, BaseFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (CallbackQuery, Message, User, BotCommand, KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)

from dotenv import load_dotenv

from parsing.recipesfish_parser import get_recipe
from tools.tools import clear_text
from gpt.deepseek import get_translation

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
chanel_id = '@big_fish_chan'

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

router = Router()

url = 'https://recipesfish.com/honey-garlic-salmon-bites/'
url = 'https://recipesfish.com/baked-salmon-with-lemon-butter-cream-sauce/'
url = 'https://recipesfish.com/baked-salmon-with-asparagus-lemon-garlic-sauce-recipe/'
url = 'https://recipesfish.com/cajun-salmon-recipe/'

outro_text = '\nПонравился рецепт? Поддержите канал лайком и подпиской! Не пропустите новые, интересные рецепты! '


async def set_commands_menu(bot: Bot):
    await bot.delete_my_commands()
    main_menu_commands = [BotCommand(
                            command='/start',
                            description='Запуск бота')
                        ]
    await bot.set_my_commands(main_menu_commands)
    return None


async def post_to_chanel(chat_id):
    recipe, images = get_recipe(url)
    image = images[0]
    translatated_recipe = get_translation(recipe)
    cleared_translatated_recipe = clear_text(translatated_recipe)
    cleared_translatated_recipe = cleared_translatated_recipe + '\n' + outro_text
    recipe_name = cleared_translatated_recipe.split('.')[0]
    print(f'Постим рецепт в канал')
    print(f'Image: {image}')
    print(f'Caption: {recipe_name}')

    try:
        await bot.send_photo(
            chat_id,
            photo=image,
            caption=recipe_name
        )
        await bot.send_message(
            chat_id,
            text=cleared_translatated_recipe,
            parse_mode='HTML'
        )
    except Exception as e:
        print(f'Исключение при отправке статьи в канал: {e}')


@dp.message(CommandStart())
async def command_start_process(message: Message):
    text = 'Bot started'
    request_button = KeyboardButton(text='Запостить')
    keyboard = ReplyKeyboardMarkup(keyboard=[[request_button]], resize_keyboard=True)
    chat_id = message.chat.id
    await post_to_chanel(chat_id)
    await message.answer(text, reply_markup=keyboard, parse_mode='Markdown')



def main():
    dp.startup.register(set_commands_menu)
    dp.include_router(router)
    dp.run_polling(bot)


if __name__ == '__main__':
    main()
