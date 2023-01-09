from bs4 import BeautifulSoup
import requests
import urllib.parse
from datetime import date
import pandas as pd
import sys


def search(product_name):
    products_list = []
    query_parameter = urllib.parse.quote(product_name)

    URL = f'https://www.backmarket.es/es-es/search?q={query_parameter}'
    html = requests.get(URL).text

    soup = BeautifulSoup(html, 'html.parser')

    products_grid = soup.find('div', {'class': 'grid'})

    try:
        for product in products_grid.findAll('a'):
            name = product.find('h2').text.strip().replace('\n', '').replace('\r', '')
            link = product['href'].strip()
            price = product.find('div', {'data-qa': 'prices'}).text.strip()

            dict_product = {
                'name': name,
                'link': 'https://www.backmarket.es' + link,
                'price': price
            }

            products_list.append(dict_product)

        return products_list

    except AttributeError:
        return products_list


if __name__ == '__main__':

    product_search = input('What\'s the product you want to search for in <backmarket.es>? <<"q" to exit>>')
    if product_search == 'q':
        sys.exit(0)

    list_products = search(product_search)

    while len(list_products) == 0:
        print(f'There were no products found matching "{product_search}", try again.')
        product_search = input('What''s the product you want to search for in <backmarket.es>? <<"q" to exit>>')
        list_products = search(product_search)

    while True:
        output_file_extension = input('Choose an output file extension (txt or csv). <<"q" to exit>>')
        if output_file_extension == 'q':
            sys.exit(0)
        if output_file_extension == 'txt' or output_file_extension == 'csv':
            break

    output_file = product_search.replace(' ', '_') + '_' + date.today().strftime("%d-%m-%Y") + f'.{output_file_extension}'

    if output_file_extension == 'txt':
        with open(output_file, 'w', encoding="utf-8") as file:
            for line in list_products:
                product = 'Name: {}\nLink: {}\nPrice: {}\n\n'
                product = product.format(line['name'], line['link'], line['price'])
                file.write(product)

    else:
        df = pd.DataFrame.from_dict(list_products)
        df.to_csv(output_file, encoding='utf-8-sig')

    print(f'The file {output_file} has been created')