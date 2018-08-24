import re


def replace_feat(artist_song_string):
    """
    Remove instances of "feat, feat., ft., ft, featuring, &"
    Brute force right now but might fix
    :return: modified string without the aforementioned
    """
    result = re.sub('\.',        '', artist_song_string, re.IGNORECASE)
    result = re.sub('& ',         '', result, re.IGNORECASE)
    result = re.sub('ft ',        '', result, flags=re.IGNORECASE)
    result = re.sub('featuring ', '', result, flags=re.IGNORECASE)
    result = re.sub('feat ',      '', result, flags=re.IGNORECASE)
    return result


if __name__ == "__main__":
    test = 3
    if True:
        test = 4
