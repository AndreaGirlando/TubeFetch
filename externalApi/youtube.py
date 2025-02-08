
from youtube_search import YoutubeSearch


def fromYoutubeSearchGetLink(search:str):
    return YoutubeSearch(search, max_results=1).to_dict()[0]["url_suffix"]
