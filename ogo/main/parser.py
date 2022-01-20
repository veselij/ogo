import subprocess
import json
import glob
import requests
import time
from collections import namedtuple


command = """
curl 'https://www.onlinetours.ru/api/v1/searches/{city}/results?sort=cheap&page=1&per_page=14' \
  -H 'authority: www.onlinetours.ru' \
  -H 'pragma: no-cache' \
  -H 'cache-control: no-cache' \
  -H 'sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'x-csrf-token: KhKUxGZigNTSbdl6X8FH7wfDhHBwsQGUXDL0Y8knc6UgqK0CMpqOk3yBYM1pBZwf06E54e67THUGs5Qg0y4-VQ' \
  -H 'x-requested-with: XMLHttpRequest' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://www.onlinetours.ru/tours/144b16405106117a07b1bb7e1d35b8d8?sort=cheap' \
  -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8' \
  -H 'cookie: _onlinetours_session_v3=f0acde28a46b348eede60e86df5e3279; __gads=ID=8d31dff941ab7bac-22bbbabf22cd0064:T=1642609972:RT=1642609972:S=ALNI_ManTKcBTQdqJoIXONIe76jlQfMUKw; _ga=GA1.2.1310875452.1642609973; _gid=GA1.2.234589705.1642609973; _ym_uid=1642609973171438945; _ym_d=1642609973; _ym_visorc=w; _ym_isad=2; 33688536846_k50cookie=; _fbp=fb.1.1642609973264.992805037; popup_session_at=1674146020; _gcl_au=1.1.1221614651.1642610051; referer_md5=dd115e2147b62da9d8a57161b33a7125; mindboxDeviceUUID=192671e4-f15d-4d37-a7ce-721332074fe6; directCrm-session=%7B%22deviceGuid%22%3A%22192671e4-f15d-4d37-a7ce-721332074fe6%22%7D; k50lastvisit=2be88ca4242c76e8253ac62474851065032d6833.da39a3ee5e6b4b0d3255bfef95601890afd80709.0a8a8950ab75ec798180fa45ffd30f515e0237f3.da39a3ee5e6b4b0d3255bfef95601890afd80709.1642610455430; k50uuid=bbe514a0-7b09-49cc-8f2c-4a3c375d0e47; k50sid=d3555948-1a92-468b-8ee6-de84f1ebd86e; _dc_gtm_UA-21526464-1=1' \
  --compressed > tmp/tours.json
"""


def collect_tours(city_id):
    result = subprocess.run(command.format(city=city_id), shell=True, capture_output=True)
    if result.returncode != 0:
        print(city_id, result)
        exit('чо то пошло не так')

def process_tours():
    Hotel = namedtuple('Hotel', ['hotel_name', 'short_location', 'beach', 'images', 'description', 'start_date',
            'duration', 'meal_type', 'price', 'room_type', 'stars', 'lat', 'long'])
    hotels = []
    files = glob.glob("tmp/*.json")
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            tours = data['results']
            for tour in tours:
                hotel = Hotel(tour['hotel']['name'].strip(), tour['shortLocationCardInfo'].strip(), tour['beachCardInfo'].strip(), tour['images'], tour['hotel']['description'].strip(), tour['cheapestOffer']['startDate'], tour['cheapestOffer']['duration'], tour['cheapestOffer']['mealTypeName'].strip(), tour['cheapestOffer']['price'], tour['cheapestOffer']['roomTypeName'].strip(), tour['hotel']['stars'], tour['hotel']['coords']['lat'], tour['hotel']['coords']['lon'])
                hotels.append(hotel)
    return hotels

def download_image(url, name):
    response = requests.get(url)
    with open(name, 'wb') as f:
        f.write(response.content)

def collect_data(resort):
    hotels = []
    collect_tours(city_id=resort)
    hotels += process_tours()
    return hotels
