"""Scraper for EIC-Book. Part of metascrape."""
from yapsy.IPlugin import IPlugin
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import requests
from meta_scrape.utils import clean_title


class EIC(IPlugin):
    """EIC scraping plugin.

    This plugin scrapes information from EIC-Book and EIC-AV.
    Returns a list of results.
    """

    EIC_BOOK_BASE_URL = 'https://www.eic-book.com'
    EIC_AV_BASE_URL = 'https://www.eic-av.com'
    EIC_BOOK_SEARCH_URL = 'https://www.eic-book.com/search?q='
    EIC_AV_SEARCH_URL = 'https://www.eic-av.com/search?q='
    results = []

    @staticmethod
    def _has_multiple_formats(title):
        """Check if the title is part of the IMBD series."""
        # TODO: Make this universal.
        if "imbd" in title.lower():
            return True
        else:
            return False

    def _search_eic_book(self, title):
        soup = BeautifulSoup(requests.get(self.EIC_BOOK_SEARCH_URL +
                                                    urllib.parse.quote(title)),
                             "html.parser")
        result_list = soup.find_all("div", class_="list")
        if self._has_multiple_formats(title):
            for result in result_list:
                # TODO: Clean titles in a more generic fashion
                _title = clean_title(result.find("h2")
                                     .get_text()
                                     .split('\n', 1)[0])
                soup = BeautifulSoup(requests.get(
                    self.EIC_BOOK_SEARCH_URL +
                    urllib.parse.quote(_title)),
                    "html.parser")
                for _result in soup.find_all("div", class_="list"):
                    result_title = _result.find("h2") \
                        .get_text().split('\n', 1)[0]
                    link = self.EIC_BOOK_BASE_URL +\
                        _result.find("a").get('href')
                    self.results.append({"title": result_title, "link": link})
        else:
            for result in result_list:
                result_title = result.find("h2") \
                    .get_text().split('\n', 1)[0]
                link = self.EIC_BOOK_BASE_URL + result.find("a").get('href')
                self.results.append({"title": result_title, "link": link})

    def _search_eic_av(self, title):
        soup = BeautifulSoup(requests.get(self.EIC_AV_SEARCH_URL +
                                                    urllib.parse.quote(title)),
                             "html.parser")
        result_list = soup.find_all("div", class_="list")
        if self._has_multiple_formats(title):
            for result in result_list:
                # TODO: Clean titles in a more generic fashion
                _title = clean_title(result.find("h2")
                                     .get_text()
                                     .split('\n', 1)[0])
                soup = BeautifulSoup(requests.get(
                    self.EIC_AV_SEARCH_URL +
                    urllib.parse.quote(_title)),
                    "html.parser")
                for _result in soup.find_all("div", class_="list"):
                    result_title = _result.find("h2") \
                        .get_text().split('\n', 1)[0]
                    link = self.EIC_AV_BASE_URL + _result.find("a").get('href')
                    self.results.append({"title": result_title, "link": link})
        else:
            for result in result_list:
                result_title = result.find("h2") \
                    .get_text().split('\n', 1)[0]
                link = self.EIC_AV_BASE_URL + result.find("a").get('href')
                self.results.append({"title": result_title, "link": link})

    def get_search_results(self, title):
        """Get search results for the title passed in parameter."""
        self._search_eic_book(title)
        self._search_eic_av(title)
        return self.results

    @staticmethod
    def get_movie_information(link):
        """Scrape the movie page for information."""
        soup = BeautifulSoup(requests.get(link), "html.parser")
        try:
            title = clean_title(soup.find("div", {"id": "con20"}).find("h1").get_text())
        except AttributeError:
            title = clean_title(soup.find("h1").get_text())

        try:
            poster = soup.find(class_="dtMainPic").get('href')
        except AttributeError:
            # No poster exists
            poster = None

        info_table = soup.find("div", attrs={"id": "dtSpecR"}).find("table") \
            .find_all("tr")
        for row in info_table:
            header = row.find("th").get_text()
            # FIXME: Is there a better way to do this than with 5 conditions ?
            if header == "メディア":
                movie_format = row.find("td").get_text().replace("\n", "")
                continue
            elif header == "出演者":
                actors = []
                actors_soup = row.find("td").find_all("a")
                for actor in actors_soup:
                    actors.append((actor.get_text()))
                continue
            elif header == "発売日":
                release_date = row.find("td").get_text().replace("\n", "")
                continue
            elif header == "メーカー":
                maker = row.find("td").get_text().replace("\n", "")
                continue
            elif header == "シリーズ":
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
            "format": movie_format,
            "release_date": release_date,
            "studio": maker,
            "set": set,
            "plot": plot
        }
