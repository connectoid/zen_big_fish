from gpt.deepseek import get_translation
from parsing.recipesfish_parser import get_recipe, get_all_recipes
from tools.tools import download_images, remove_images, clear_text, save_text_to_file, create_recipe_folder

url = 'https://recipesfish.com/honey-garlic-salmon-bites/'
url = 'https://recipesfish.com/baked-salmon-with-lemon-butter-cream-sauce/'
url = 'https://recipesfish.com/baked-salmon-with-asparagus-lemon-garlic-sauce-recipe/'

all_recipes_url = 'https://recipesfish.com/category/recipes/seafood/'

outro_text = 'Понравился рецепт? Поддержите канал лайком и подпиской! Не пропустите новые, интересные рецепты! '


def main():
    get_all_recipes(all_recipes_url)
    return

    recipe_path = url.split('/')[3]
    target_path = f'/Users/alexanderbeley/Documents/Dzen/Recipes/Recipesfish/{recipe_path}/'
    create_recipe_folder(target_path)
    recipe, images = get_recipe(url)
    print(f'Найдено {len(images)} изображений')
    download_images(images, target_path)
    translatated_article = get_translation(recipe)
    cleared_translatated_article = clear_text(translatated_article)
    cleared_translatated_article = cleared_translatated_article + '\n' + outro_text
    save_text_to_file(cleared_translatated_article, target_path)
    print(cleared_translatated_article)


if __name__ == '__main__':
    main()