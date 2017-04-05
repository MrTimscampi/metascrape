import json
import os

from yapsy.IPlugin import IPlugin
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse


class EICBOOK(IPlugin):

    BASE_URL = 'https://www.eic-book.com'
    SEARCH_URL = 'https://www.eic-book.com/search?q='

    @staticmethod
    def _is_imbd(title):
        if "imbd" in title.lower():
            return True
        else:
            return False

    def get_search_results(self, title):
        results = []
        soup = BeautifulSoup(urllib.request.urlopen(self.SEARCH_URL +
                                                    urllib.parse.quote(title)),
                             "html.parser")
        result_list = soup.find_all("div", class_="list")
        if self._is_imbd(title):
            for result in result_list:
                _title = result.find("h2").get_text().split('\n', 1)[0]\
                    .replace(" [Blu-ray]", "")
                soup = BeautifulSoup(urllib.request.urlopen(self.SEARCH_URL +
                                                            urllib.parse
                                                            .quote(_title)),
                                     "html.parser")
                _result_list = soup.find_all("div", class_="list")
                for _result in _result_list:
                    link = self.BASE_URL + _result.find("a").get('href')
                    results.append(link)
        else:
            for result in result_list:
                link = self.BASE_URL + result.find("a").get('href')
                results.append(link)
        return results

    @staticmethod
    def get_movie_information(link):
        soup = BeautifulSoup(urllib.request.urlopen(link), "html.parser")
        title = soup.find("h1").get_text().replace(" [DVD]", "")\
            .replace(" [Blu-ray]", "").replace("　", " ")
        poster = soup.find(class_="dtMainPic").get('href')
        info_table = soup.find("div", attrs={"id": "dtSpecR"}).find("table")\
            .find_all("tr")
        for row in info_table:
            header = row.find("th").get_text()
            # FIXME: Is there a better way to do this than with 5 conditions ?
            if header == "メディア":
                format = row.find("td").get_text().replace("\n", "")
                continue
            if header == "出演者":
                actors = []
                actors_soup = row.find("td").find_all("a")
                for actor in actors_soup:
                    actors.append((actor.get_text()))
                continue
            if header == "発売日":
                release_date = row.find("td").get_text().replace("\n", "")
                continue
            if header == "メーカー":
                maker = row.find("td").get_text().replace("\n", "")
                continue
            if header == "シリーズ":
                set = row.find("td").get_text().replace("\n", "")
                continue
        plot = soup.find("div", attrs={"id": "dtSpec"}).find("p").get_text()
        # TODO: Refactor the synopsis cleaning
        if plot.startswith("\r\n"):
            plot = plot[2:]
        if plot.endswith("\r\n"):
            plot = plot[:-2]
        return {
            "title": title,
            "poster": poster,
            "actors": actors,
            "format": format,
            "release_date": release_date,
            "studio": maker,
            "set": set,
            "plot": plot
        }
