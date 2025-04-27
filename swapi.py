import requests
from pathlib import Path


class APIRequester:

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):

        url = self.base_url + endpoint
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.RequestException:
            print("Возникла ошибка при выполнении запроса")


class SWRequester(APIRequester):

    def get_sw_categories(self):
        response = self.get("/")
        if response is not None:
            data = response.json()
            return data.keys()

    def get_sw_info(self, sw_type):
        response = self.get(f"/{sw_type}/")
        if response is not None:
            return response.text


def save_sw_data():
    requester = SWRequester("https://swapi.dev/api")
    path = Path("data")
    path.mkdir(exist_ok=True)

    categories = requester.get_sw_categories()

    for category in categories:
        info = requester.get_sw_info(category)
        file_path = f"data/{category}.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(info)
