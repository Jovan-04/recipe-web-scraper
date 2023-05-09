import requests
from bs4 import BeautifulSoup
import re

fromXtoML = {
    'teaspoon': 4.929,
    'tablespoon': 14.787,
    'cup': 240.0
}

def parse_volume(volume:str)->tuple[int,str]:
    quantities = re.findall(r'[\d|/]+', volume)
    length = len("".join(quantities))
    amount = sum(eval(s) for s in quantities)
    string = volume[length+len(quantities):]
    unit = string[:-1] if string.endswith('s') else string
    return tuple([amount, unit])

def convert_to_ml(volume:tuple[float,str]):
    return volume[0] * fromXtoML[volume[1].strip()]


def KAB_main():
    response = requests.get('https://www.kingarthurbaking.com/learn/ingredient-weight-chart')

    parsedHtml = BeautifulSoup(response.text, 'html.parser')

    body = parsedHtml.find('tbody')

    rows = body.find_all('tr')

    for row in rows:
        ingredient = re.sub(r'[^0-9|a-z|A-Z|\-|,| ]','',row.find('th').getText()).lower()
        # ingredient = row.find('th').getText().lower().replace("'", '').replace('"','-inch').replace(' ','')

        volume = row.find_all('td')[0].getText().replace('­','')
        try: 
            milliliters = convert_to_ml(parse_volume(volume))
        except:
            continue

        grams_text = row.find_all('td')[2].getText()

        try:
            grams = float(grams_text)
        except:
            interval = [int(i) for i in re.findall(r'\d+', grams_text)]
            grams = (interval[0] + interval[1]) / 2

        print(f'"{ingredient}": {round(grams / milliliters, 4)},')

if __name__ == '__main__':
    KAB_main()
