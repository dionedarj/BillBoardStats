from urllib.request import urlopen
from bs4 import BeautifulSoup
import discogs_client as dc
import webbrowser
import requests
import json
import re
import time

WIKIPEDIA_API_URL = 'https://en.wikipedia.org/w/api.php'
BILLBOARD_URL = 'https://www.billboard.com/charts/hot-100/'
USER_AGENT = 'BillBoardStats/0.1'
SEARCH_PARAMS_TEMPLATE = {
    'action': 'query',
    'list': 'search',
    'srsearch': 'tosearch',
    'format': 'json'
}

def list_from_date(date=''):
    """
    Takes in a date from billboard top 100 and returns a list of tuples
    with various information about each song
    :param date: date to search for billboard top 100 week
    :return: tuple containing (artist, song, year, genre)
    """

    url = BILLBOARD_URL + date
    request = requests.get(url, headers={ 'User-Agent': USER_AGENT })
    html = request.text

    soup = BeautifulSoup(html, 'html.parser')

    # First Song/Artist - needed because Billboard puts their first song/artist in a div class
    # "chart-number-one__title"  and "chart-number-one__artist
    # Sometimes the artist is wrapped in an <a> tag and sometimes not. 
    # We check for this.
    
    first_song = soup.find('div', {'class': 'chart-number-one__title'}).string.strip()
    first_artist = soup.find('div', {'class': 'chart-number-one__artist'}).find('a', text=True)
    if first_artist is None:
        first_artist = soup.find('div', {'class': 'chart-number-one__artist'}).string.strip()
    else:
        first_artist = first_artist.string.strip()

        

    songs = soup.find_all('span', {'class': 'chart-list-item__title-text'})
    artists = soup.find_all(lambda tag: (tag.name == 'div' and tag.get('class') == ['chart-list-item__artist'] and len(list(tag.descendants)) == 1) 
                                    or (tag.name == 'a' and tag.parent.name == 'div' and tag.parent.get('class') == ['chart-list-item__artist']))

    songs = list(map(lambda x: x.contents[0].strip(), songs))
    artists = list(map(lambda x: x.contents[0].strip(), artists))

    songs = [first_song] + songs
    artists = [first_artist] + artists

    pairs = list(zip(artists, songs))

    years = []
    for i, pair in enumerate(pairs):
        artist = pair[0]
        song = pair[1]
        restriction_count = restriction_count + 1
        song_artist = song + ' ' + artist
        print(song_artist)

        found = False
        try:
            results = client.search(replace_feat(song_artist), type='release')
            for result in results:
                print(result)
                if artist in result.title:
                    years = years + [result.year]
                    found = True
                    break

            if not found:
                del pairs[i]
            found = False
        except IndexError:
            pass

        # results = client.search(replace_feat(song_artist), type='release')
        # if len(results) != 0:
        #     for result in results:
        #         if artist in result.title:
        #             years.append(result.year)
        #             break

        if restriction_count >= 60:
            print('waiting!')
            time.sleep(60)
            restriction_count = 0

    print(years)
    # results = [client.search(pair[0] + ' ' + pair[1], type='release') for pair in pairs]
    # years = [result[0].year for result in results]

    return pairs


def get_config():
    """
    Loads json from 'config.json'
    :return: token from json file
    """
    with open('config.json') as f:
        config = json.load(f)
        return config


def replace_feat(artist_song_string):
    """
    Remove instances of "feat, feat., ft., ft, featuring, &"
    Brute force right now but might fix
    :return: modified string without the aforementioned
    """
    result = re.sub(' .',          '',  artist_song_string, re.IGNORECASE)
    result = re.sub(' & ',         ' ', result, re.IGNORECASE)
    result = re.sub(' ft ',        ' ', result, flags=re.IGNORECASE)
    result = re.sub(' featuring ', ' ', result, flags=re.IGNORECASE)
    result = re.sub(' feat ',      ' ', result, flags=re.IGNORECASE)
    return result


if __name__ == '__main__':
    list_from_date()
