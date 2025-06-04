from bs4 import BeautifulSoup
import requests
from random import choice
from time import sleep
from sys import argv, stdout

GAP_TIME = 0.03

def sprint(string: str, gap: float = GAP_TIME, new_line: bool = True) -> None:
    for ch in string:
        stdout.write(ch)
        stdout.flush()
        sleep(gap)
    if ch != '\n' and new_line:
        stdout.write('\n')
        stdout.flush()

def sinput(prompt: str) -> str:
    sprint(prompt, GAP_TIME, False)
    return input()

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml",
}

def main():
    username = sinput("Insert your Letterboxd username: ") if len(argv) < 2 else argv[1]
    url = "https://letterboxd.com"
    films = []
    watchlist_page = url + f"/{username}/watchlist/page/"

    sprint('Looking for your new favorite movie...')

    try:
        # 1 page --> 28 films
        for i in range(1, 7+1):  # the n. of pages now are 7 (168 < nFilms < 196)
            r = requests.get(watchlist_page + str(i), headers=headers)
            bs = BeautifulSoup(r.text, 'html.parser')

            ul = bs.find('ul', class_='poster-list')
            li_s = ul.find_all('li', class_='poster-container')
            for li in li_s:
                div = li.find('div')
                link = div.get('data-target-link')
                img = li.find('img')
                name = img.get('alt')
                films.append({'link': link, 'name': name})
    except AttributeError:
        sprint('No users found! (Maybe the user has a private account!)')
        return

    film = choice(films)
    sprint(f'''And the Oscar goes to... {film['name']}!\nLink: {url}{film['link']}''')


if __name__ == '__main__':
    main()