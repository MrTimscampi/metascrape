"""Scraper for U15DVDInfo. Part of metascrape."""
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup
from yapsy.IPlugin import IPlugin

from meta_scrape.utils import clean_title


class U15DVDInfo(IPlugin):
    """u15dvdinfo scraping plugin.

    This plugin scrapes information from u15dvdinfo.com.
    Returns a list of results.
    """

    U15_BASE_URL = 'http://u15dvdinfo.com'
    U15_SEARCH_URL = 'http://u15dvdinfo.com/?s_type=products&s='
    results = []

    def _search_u15dvdinfo_com(self, title):
        # TODO: Handle pagination
        soup = BeautifulSoup(urllib.request.urlopen(self.U15_SEARCH_URL +
                                                    urllib.parse.quote(title)),
                             "html.parser")
        result_list = soup.find_all("div", class_="entry")
        for result in result_list:
            result_title = result.find("h2") \
                .get_text().split('\n', 1)[0]
            link = result.find("a").get('href')
            self.results.append({"title": result_title, "link": link})

    def get_search_results(self, title):
        """Get search results for the title passed in parameter."""
        self._search_u15dvdinfo_com(title)
        return self.results

    @staticmethod
    def get_movie_information(link):
        """Scrape the movie page for information."""
        soup = BeautifulSoup(urllib.request.urlopen(link), "html.parser")

        title_pre_clean = clean_title(soup.find("h1").get_text()).split(' | ')
        title = title_pre_clean[0]
        movie_format = title_pre_clean[2]

        try:
            poster = soup.find(class_="p_image").find("img").get('src')
        except AttributeError:
            # No poster exists
            poster = None

        plot = soup.find("div", class_="description").get_text()
        # TODO: Refactor the synopsis cleaning
        if plot.startswith("\r\n"):
            plot = plot[2:]
        if plot.endswith("\r\n"):
            plot = plot[:-2]

        production_info_table = soup.find("table", class_="pro_info")\
            .find_all("tr")
        for row in production_info_table:
            header = row.find("th").get_text()
            # FIXME: Is there a better way to do this than with 5 conditions ?
            if header == "メーカー":
                maker = row.find("td").get_text().replace("\n", "")
                continue
            elif header == "発売日":
                release_date = row.find("td").get_text().replace("\n", "")
                continue

        production_info_table = soup.find("table", class_="idol_info") \
            .find_all("tr")
        actors = []
        for row in production_info_table[1:]:
            cell = row.find("td").get_text()
            actors.append(cell)
        return {
            "title": title or None,
            "poster": poster or None,
            "actors": actors or None,
            "format": movie_format or None,
            "release_date": release_date or None,
            "studio": maker or None,
            "set": None,
            "plot": plot or None
        }
