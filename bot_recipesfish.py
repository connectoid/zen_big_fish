import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from parsing.recipesfish_parser import get_recipe
from tools.tools import clear_text, get_new_url
from gpt.deepseek import get_translation

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
chanel_id = '@breakingames'

chat_id = os.getenv('ADMIN_CHAT_ID')
outro_text = '\nПонравился рецепт? Поддержите канал лайком и подпиской! Не пропустите новые, интересные рецепты! '


async def post_to_chanel(bot, chat_id):
    url = get_new_url()
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


# async def main():
#     await post_to_chanel(chat_id)

async def main():
    async with Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) as bot:
        await post_to_chanel(bot, chat_id)



if __name__ == '__main__':
    asyncio.run(main())
