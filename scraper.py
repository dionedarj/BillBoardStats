from urllib.request import urlopen
from bs4 import BeautifulSoup
import discogs_client as dc
import re
import urllib.request
import json


def list_from_date(date):
    url = 'https://www.billboard.com/charts/hot-100/' + date
    request = urllib.request.Request(
        url,
        headers = {
            'User-Agent': 'BillBoardStats/0.1',
        }
    )
    html = urlopen(request).read()

    soup = BeautifulSoup(html, 'html.parser')

    # First Song/Artist - needed because Billboard puts their first song/artist in a div class
    # "chart-number-one__title"  and "chart-number-one__artist
    
    first_song = soup.find('div', {'class': 'chart-number-one__title'}).string.strip()
    first_artist = soup.find('div', {'class': 'chart-number-one__artist'}).find('a', text=True).string.strip()

    songs = soup.find_all('span', {'class': 'chart-list-item__title-text'})
    artists = soup.find_all(lambda tag: (tag.name == 'div' and tag.get('class') == ['chart-list-item__artist'] and len(list(tag.descendants)) == 1) 
                                    or (tag.name == 'a' and tag.parent.name == 'div' and tag.parent.get('class') == ['chart-list-item__artist']))

    songs = list(map(lambda x: x.contents[0].strip(), songs))
    artists = list(map(lambda x: x.contents[0].strip(), artists))

    songs = [first_song] + songs
    artists = [first_artist] + artists

    print('Number of songs on list: ' + str(len(songs)))
    print('Number of artists on list: ' + str(len(artists)))

    pairs = list(zip(artists,songs))
 
    print(pairs)
    return pairs


# Gets discogs token from file
def get_token():
    with open('token.json') as f:
        data = json.load(f)
        return data["token"]


if __name__ == '__main__':
    client = dc.Client('BillBoardStats/0.1', user_token=get_token())
    results = client.search('Psycho Post Malone', type='release')
    print(results[0].artists[0].name)
    list_from_date('')
