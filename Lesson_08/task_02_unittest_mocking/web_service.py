"""
Завдання 2. Мокування за допомогою unittest.mock

Напишіть програму для отримання даних з веб-сайту та протестуйте його за допомогою моків. Напишіть клас WebService, який має метод get_data(url: str) -> dict. Цей метод повинен використовувати бібліотеку requests, щоб робити GET-запит та повертати JSON-відповідь. Використовуйте unittest.mock для макування HTTP-запитів. Замокуйте метод requests.get таким чином, щоб він повертав фейкову відповідь (наприклад, {"data": "test"}), та протестуйте метод get_data.

Напишіть кілька тестів:

перевірка успішного запиту (200),
перевірка обробки помилки (404 чи інші коди).
"""

import requests

class WebService:
    """
    Клас для отримання даних з веб-сайту через HTTP-запит.
    """

    def get_data(self, url: str) -> dict:
        """
        Робить GET-запит до вказаного URL і повертає JSON-відповідь.

        Raises:
            requests.RequestException: якщо запит не вдався
        """
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
