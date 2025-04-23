from pprint import pprint

from gpt.deepseek import get_translation
from parsing.saveur_parser import get_all_recipes, get_recipe
from tools.tools import (download_images, remove_images, clear_text, save_text_to_file, 
                         save_list_to_file, get_new_url, create_recipe_folder)


all_recipes_url = 'https://www.saveur.com/recipes/fish-recipes/'
url = 'https://www.saveur.com/article/recipes/everything-potato-galette-with-lox-and-creme-fraiche/'

outro_text = 'Понравился рецепт? Поддержите канал лайком и подпиской! Не пропустите новые, интересные рецепты! '


def main():
    # urls_list = get_all_recipes(all_recipes_url)
    # if urls_list:
    #     save_list_to_file(urls_list, 'saveur_new_urls.txt')
    # else:
    #     print('Список адресов не получен')


    # url = get_new_url()
    # print(url)
    recipe_path = url.split('/')[5]
    target_path = f'/Users/alexanderbeley/Documents/Dzen/Recipes/Saveur/{recipe_path}/'
    create_recipe_folder(target_path)

    recipe, images = get_recipe(url)
    
    
    print(f'Найдено {len(images)} изображений')
    remove_images(target_path)
    download_images(images, target_path)
    translatated_article = get_translation(recipe)
    cleared_translatated_article = clear_text(translatated_article)
    cleared_translatated_article = cleared_translatated_article + '\n' + outro_text
    save_text_to_file(cleared_translatated_article, target_path)
    print(cleared_translatated_article)


if __name__ == '__main__':
    main()