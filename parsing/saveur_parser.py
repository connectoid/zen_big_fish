from pprint import pprint

import requests
from bs4 import BeautifulSoup

from gpt.deepseek import get_translation

base_url = 'https://www.saveur.com'


def get_all_recipes(url):
    urls_list = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        urls = soup.find_all('a', class_='post-card__featured-image')
        urls = [base_url + url['href'] for url in urls]
        for url in urls:
            print(url)
        return urls
    else:
        print(f'get_all_recipes error: {response.status_code}')
        return None


def get_recipe(url):
    recipe = {}
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        header_section = soup.find('header', {'data-og-area': 'article-header'})
        name = header_section.find('h1').text
        image = soup.find('source', {'media': '(max-width: 900px)'})['srcset'].split('?')[0]
        images = []
        images.append(image)
        ingredients_section = soup.find('ul', class_='ingredients')
        ingredients = ingredients_section.find_all('li')
        ingredients = [li.text for li in ingredients]
        article_div = soup.find('div', {'data-og-area': 'article-blocks'})
        description = article_div.find_all('p')[0].text
        recipe_div = article_div.find_all('span')
        instructions = [span.text for span in recipe_div]
        print(instructions)
        recipe['name'] = name
        recipe['image'] = image
        recipe['description'] = description
        recipe['ingredients'] = ingredients
        recipe['instructions'] = instructions
        return recipe, images

    else:
        print(f'get_recipe error: {response.status_code}')
        return None
