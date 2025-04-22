from pprint import pprint

import requests
from bs4 import BeautifulSoup

from gpt.deepseek import get_translation


def create_recipe_text(recipe):
    name = recipe['name']
    description = recipe['description']
    ingredients = '\n'.join(recipe['ingredients'])
    instructions = '\n'.join(recipe['instructions'])
    notes = '\n'.join(recipe['notes'])
    nutritions = '\n'.join(recipe['nutritions'])
    text = f'{name}\n{description}\n{ingredients}\n{instructions}\n{notes}\n{nutritions}'
    return text


def get_all_recipes(main_url):
    urls_list = []
    response = requests.get(main_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        nav_links = soup.find('div', class_='nav-links').find_all('a', class_='page-numbers')
        try:
            page_number = int(nav_links[-2].text.split('Page')[-1])
        except Exception as e:
            print(f'Ошибка получения числа страниц: {e}')
            page_number = 0

        for page in range(1, page_number + 1):
            page_url = f'{main_url}page/{page}/'
            response = requests.get(page_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                recipes = soup.find_all('h2', class_='entry-title')
                for recipe in recipes:
                    urls_list.append(recipe.find('a')['href'])

        for url in urls_list:
            print(url)
    else:
        print(f'Requests error in get_all_recipes: {response.status_code}')
        return None

def get_recipe(url):
    response = requests.get(url)
    if response.status_code == 200:
        recipe = {}
        soup = BeautifulSoup(response.text, 'lxml')
        name = soup.find('h1', class_='entry-title').text
        image = soup.find('span', class_='ns-pinterest-image').find('img')['data-src']
        images = []
        images.append(image)
        description = soup.find('div', class_='tasty-recipes-description').text
        ingredients = soup.find('div', class_='tasty-recipes-ingredients-body').find_all('li')
        ingredients = [ingredient.text for ingredient in ingredients]
        instructions = soup.find('div', class_='tasty-recipes-instructions-body').find_all('li')
        instructions = [instruction.text for instruction in instructions]
        notes = soup.find('div', class_='tasty-recipes-notes').find_all('li')
        notes = [note.text for note in notes]
        nutritions = soup.find('div', class_='tasty-recipes-nutrition').find_all('li')
        nutritions = [nutrition.text for nutrition in nutritions]
        recipe['name'] = name
        recipe['image'] = image
        recipe['description'] = description
        recipe['ingredients'] = ingredients
        recipe['instructions'] = instructions
        recipe['notes'] = notes
        recipe['nutritions'] = nutritions
        return recipe, images
    else:
        print(f'Requests error in get_recipe: {response.status_code}')
        return None
