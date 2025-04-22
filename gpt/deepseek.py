import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv('DEEP_SEEK_API_KEY')
BASE_DEEPSEEK_URL = 'https://api.deepseek.com'
DEEPSEEK_API_KEY = 'sk-7df9a4c320d849a7b25a1d40b69516fe'


translation_prompt_intro = """
        Переведи этот рецепт на русский язык при этом конвертируй количество 
        ингредиентов и единицы измерения в метрическую систему. Первым абзацем, 
        после названия блюда, вставь небольшую историю или полезную информацию 
        про это блюдо. Придай тексту живой характер, не пиши ничего от себя 
        (кроме первого абзаца), сразу название рецепта, историю и остальную информацию. 
        Не выделяй дефисами и цифрами списки в разделах Ингредиенты, Советы, Приготовление, 
        Пищевая ценность. Убери из раздела Пищевая ценность упоминание холестирина если оно есть. 
        Не пиши слово Рецепт вначале. Вот рецепт для перевода: 
    """


def get_translation(prompt):
    prompt = f'{translation_prompt_intro} {prompt}'
    print(f'Fetch data ...')
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=BASE_DEEPSEEK_URL)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )
    response_json = response.json()
    answer = response.choices[0].message.content
    return answer