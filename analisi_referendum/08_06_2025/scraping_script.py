from playwright.sync_api import sync_playwright
import csv

url = 'https://elezioni.interno.gov.it/risultati/20250608/referendum/votanti/italia/'

cod = [
    [2, 7, 96, 27, 52, 81, 102, 88],
    [4],
    [12, 15, 24, 26, 98, 99, 45, 49, 104, 57, 77, 86],
    [14, 83],
    [10, 54, 71, 84, 87, 89, 90],
    [35, 93, 92, 85],
    [34, 37, 39, 74],
    [13, 29, 32, 50, 56, 61, 66, 68, 101],
    [5, 30, 36, 42, 43, 46, 62, 63, 100, 75],
    [58, 80],
    [3, 6, 105, 44, 59],
    [33, 40, 69, 70, 91],
    [23, 38, 60, 79],
    [19, 94],
    [8, 11, 20, 51, 72],
    [9, 106, 16, 31, 41, 78],
    [47, 64],
    [22, 25, 97, 67, 103],
    [1, 18, 21, 28, 48, 55, 65, 76, 82],
    [17, 53, 95, 73]
]

QUERY_NAME = '.riga_noclick > td:nth-child(1) > p, .riga > td:nth-child(1) > p'
QUERY_VALUE = '.riga_noclick > td:nth-child(7) > p, .riga > td:nth-child(7) > p'

for V in range(1, 6):
    perc = {}
    for idx, x in enumerate(cod):
        for y in x:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url + str(V).zfill(2) + str(idx+1).zfill(2) + str(y).zfill(3), wait_until="networkidle")
                print(  \
                    provincia := page.locator('#tabella > div.q-table__container.q-table--horizontal-separator.column.no-wrap.q-table__card.q-table--no-wrap.tabella.tabella_votanti > div.q-table__top.relative-position.row.items-center > div:nth-child(1) > p').text_content(), \
                    ': ', page.locator(QUERY_NAME).count(), sep='' \
                )
                for i in range(0, page.locator(QUERY_NAME).count()):
                    name = page.locator(QUERY_NAME).nth(i).text_content() + ' (' + provincia.split(' ')[-1] + ')'
                    value = page.locator(QUERY_VALUE).nth(i).text_content()
                    try:
                        perc[name] = float(value.replace(',', '.'))
                    except:
                        perc[name] = None

    with open(f"percentuale{str(V).zfill(2)}.csv", "w", newline="") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Comune", "Percentuale"])  # header row
        for comune, percentuale in perc.items():
            writer.writerow([comune, percentuale])