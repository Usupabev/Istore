import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    headers = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    response = requests.get(url, headers=headers)
    return response.text

def write_to_csv(data):
    with open('istore.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter='/')
        writer.writerow((data['title'], data['price_full'], data['image_full'], data['info_full']))

def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    block = soup.find('div', class_='h-100 container d-flex flex-wrap products-content')
    for i in block:
        try:
            title = i.find('h5', class_='card-title mt-2 of-ellipsis').text

            price = i.find('p', class_='card-price-rub mb-1').text
            price_full = price.replace('от', '').replace('\n', '').replace('  ', '')

            image = i.find('img').get('src')
            image_full = 'https://istore.kg' + image

            info = i.find('ul', class_='as-macbundle-modelspecs')
            info_full = info.find('li').text

            data = {'title': title, 'price_full': price_full, 'image_full': image_full, 'info_full': info_full}
            write_to_csv(data)
        except:
            pass

def main():
    url = 'https://istore.kg/catalog/mac/mac-13-air'
    all_links = get_page_data(get_html(url))
    return all_links

main()
