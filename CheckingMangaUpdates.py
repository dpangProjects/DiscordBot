from manganelo import SearchManga
from manganelo import MangaInfo

class manga_updates:

    def __init__(self):
        return

    def getupdate(manganame):
        search = SearchManga(manganame, threaded=True)

        results = search.results

        best_result = results[0]

        manga_info = MangaInfo(best_result.url, threaded=True)

        manga_page = manga_info.results

        latest = manga_page.chapters[-1]

        chapter = ''
        name = str(latest)
        for i in name:
            if i.isdigit():
                chapter += i
            if i == ',':
                chapter = ''

        url = ''
        endset = False
        for idx, i in enumerate(name[40:]):
            if i == "'" and not endset:
                end = idx + 40
                endset = True

        url = name[40:end]
        return chapter, url
