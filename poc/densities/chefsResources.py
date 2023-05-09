import requests
from bs4 import BeautifulSoup
import re

def CR_main():
    response = requests.get('https://www.chefs-resources.com/culinary-conversions-calculators-and-capacities/dry-spice-yields/')

    parsedHtml = BeautifulSoup(response.text, 'html.parser')

    body = parsedHtml.find('tbody')

    rows = body.find_all('tr')

    # failed_densities = []

    for row in rows:
        ingredient = re.sub(r'[^0-9|a-z|A-Z|\-|,| ]','',row.find_all('td')[0].getText()).lower()
        oz_per_cup = row.find_all('td')[1].getText()
        try:
            grams_per_ml = float(oz_per_cup) / 8.345
        except:
            try:
                tbl_per_oz = row.find_all('td')[2].getText()
                grams_per_ml = (1 / float(tbl_per_oz)) * 1.917
            except:
                # failed_densities.append(ingredient)
                continue

        print(f'"{ingredient}": {round(grams_per_ml, 4)},')

    # print(failed_densities)

if __name__ == '__main__':
    CR_main()
