import requests
import re
from bs4 import BeautifulSoup
import csv
import tqdm

BASE_URL = "https://ru.wikipedia.org"
BASE_WIKI_CATEGORY_URL = f"{BASE_URL}/wiki/Категория:Животные_по_алфавиту"


def extract_page_count(data) -> int | None:
    """Извлечение количества страниц из текстового фрагмента на странице"""
    match = re.search(r'из\s([\d\s\u00a0]+)', data)

    if match:
        number_str = match.group(1).replace('\xa0', '').replace(' ', '')
        number = int(number_str)
        return number


def compute_pages_for_parsing(exact_page_count) -> int:
    # Вычисление количества страниц с запасом
    return exact_page_count // 200


def update_beasts_quantity(new_data: dict, beasts_vault: dict) -> None:
    for key, value in new_data.items():
        if key in beasts_vault:
            beasts_vault[key] = beasts_vault[key] + value
        else:
            beasts_vault[key] = value


def write_to_csv(beasts_vault: dict) -> None:
    with open("beasts_sample.csv", "w", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(beasts_vault.items())


def find_next_page_url(data: BeautifulSoup) -> str | None:
    return data.find("a", string="Следующая страница")["href"]


def find_beasts_quantity(data: BeautifulSoup) -> dict:
    temp_beasts = dict()
    all_letters_boxes = data.find_all("div", class_="mw-category-group")[2:]

    for box in all_letters_boxes:
        temp_beasts.update(
            {box.find("h3").get_text(): len(box.find_all("li"))}
        )

    return temp_beasts


def fetch_page_data(request_url: str) -> BeautifulSoup:
    """"""
    resp = requests.get(request_url)
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup


def fetch_page_count(request_url: str = BASE_WIKI_CATEGORY_URL) -> str:
    resp = requests.get(request_url)
    soup = BeautifulSoup(resp.text, "html.parser")
    page_info_box = soup.find("div", id="mw-pages")
    raw_page_count = page_info_box.find("p").get_text()
    return raw_page_count


def write_final_data(data: dict) -> None:
    pass


def main():
    beasts_quantity = dict()
    raw_page_count = fetch_page_count()
    exact_page_count = extract_page_count(raw_page_count)
    page_count = compute_pages_for_parsing(exact_page_count)

    request_url = BASE_WIKI_CATEGORY_URL
    for _ in tqdm.tqdm(range(page_count), desc="Прогресс загрузки"):
        page_data = fetch_page_data(request_url)
        temp_beasts = find_beasts_quantity(page_data)
        request_url = BASE_URL + find_next_page_url(page_data)

        update_beasts_quantity(temp_beasts, beasts_quantity)

    write_to_csv(beasts_quantity)


main()
