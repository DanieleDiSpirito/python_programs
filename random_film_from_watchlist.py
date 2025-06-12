from bs4 import BeautifulSoup
import requests
from random import choice
from time import sleep
from sys import argv, stdout
from tqdm import tqdm

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

    curr_page = 1

    req_to_img = False
    if len(argv) > 2 and argv[2] == '--img':
        req_to_img = True
        sprint('Images will be requested.')
    
    try:
        r = requests.get(watchlist_page + str(curr_page), headers=headers)
        bs = BeautifulSoup(r.text, 'html.parser')
        count = bs.find('span', class_='js-watchlist-count')
        remain = int(count.text.split()[0])
        for curr_page in tqdm(range(1, (remain-1) // 28 + 2)): # 1 page == 28 films
            if curr_page != 1:
                r = requests.get(watchlist_page + str(curr_page), headers=headers)
                bs = BeautifulSoup(r.text, 'html.parser')
            ul = bs.find('ul', class_='poster-list')
            li_s = ul.find_all('li', class_='poster-container')
            for li in li_s:
                div = li.find('div')
                link = div.get('data-target-link')
                img_req = div.get('data-cache-busting-key')
                img_div = li.find('img')
                name = img_div.get('alt')
                if img_req and req_to_img:
                    r2 = requests.get(url + '/ajax/poster/' + link + '/std/125x187/?k=' + img_req, headers=headers)
                    bs2 = BeautifulSoup(r2.text, 'html.parser')
                    img = bs2.find('img').get('src')
                    films.append({'link': link, 'name': name, 'img': img})
                elif img_req is None and req_to_img:
                    films.append({'link': link, 'name': name, 'img': None})
                else: films.append({'link': link, 'name': name})
    except AttributeError as e:
        sprint('No users found! (Maybe the user has a private account!)\n' + str(e))
        return

    film = choice(films)
    if req_to_img:
        sprint(f'''And the Oscar goes to... {film['name']}!\nLink: {url}{film['link']}\nImage: {film['img']}''')
    else:
        sprint(f'''And the Oscar goes to... {film['name']}!\nLink: {url}{film['link']}''')
    sprint('Enjoy your movie!')


if __name__ == '__main__':
    main()