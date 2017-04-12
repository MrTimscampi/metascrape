"""Metascrape subcommand for scraping files and folders."""
import os
import xml.etree.cElementTree as ET

import click

from meta_scrape import SCRAPER_MANAGER


@click.command()
@click.option('-t', '--title',
              help='Title to use as search string.',
              metavar='TITLE')
@click.argument('path', type=click.Path(exists=True,
                                        file_okay=True,
                                        dir_okay=True,
                                        writable=True,
                                        readable=True))
def scrape(title, path):
    """Scrape the metadata for the directory."""
    information = None

    if SCRAPER_MANAGER.getAllPlugins():
        # If the title option wasn't provided, get it from the path
        if not title:
            title = os.path.basename(os.path.normpath(path))

        click.echo("Scraping for title: {0}".format(title))
        for plugin in SCRAPER_MANAGER.getAllPlugins():
            click.echo("Searching for movie using the {0} scraper"
                       .format(plugin.name))
            search_results = plugin.plugin_object.get_search_results(title)
            if not search_results:
                click.echo("No results found using scraper {0}."
                           .format(plugin.name))
                continue
            elif len(search_results) == 1:
                link = search_results[0]
                click.echo("Found a match at: {0}".format(link))
            else:
                click.echo("Multiple matches have been found by the {0} "
                           "scraper:".format(plugin.name))
                for index, link in enumerate(search_results):
                    click.echo("  {0} - {1}\n      URL: {2}"
                               .format(index, link['title'], link['link']))
                value = click.prompt('Please enter the number '
                                     'of the link to use',
                                     default=0)
                link = search_results[value]['link']
            information = plugin.plugin_object.get_movie_information(link)
        if information:
            write_kodi_nfo(information, path)
            click.echo("Scraped {0} as {1}.".format(title, information.get("title")))
        else:
            click.echo("No match found.")
    else:
        click.secho("  No scrapers found.", fg="red")


def write_kodi_nfo(information, path):
    """Write the provided information to movie.nfo."""
    click.echo("Writing movie.nfo...")
    root = ET.Element("movie")
    ET.SubElement(root, "title").text = information.get("title")
    ET.SubElement(root, "originaltitle").text = information.get("title")
    ET.SubElement(root, "sorttitle").text = information.get("title")
    ET.SubElement(root, "set").text = information.get("set")
    ET.SubElement(root, "year").text = information.get("release_date")[:4]
    ET.SubElement(root, "plot").text = information.get("plot")
    ET.SubElement(root, "studio").text = information.get("studio")
    tree = ET.ElementTree(root)
    tree.write(os.path.join(path, "movie.nfo"), encoding="UTF-8")
