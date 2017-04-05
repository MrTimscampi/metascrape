"""Entry-point for metascrape."""
import click

from . import SCRAPER_MANAGER, SCRAPERS_DIRECTORY, VERSION, scrape


@click.group()
def main():
    """Provide an entry point to the various metascrape sub-commands."""
    click.echo(click.style("metascrape", fg="yellow") +
               " - version {0}".format(VERSION) + "\n")
    SCRAPER_MANAGER.setPluginInfoExtension("plugin")
    SCRAPER_MANAGER.setPluginPlaces([SCRAPERS_DIRECTORY])
    SCRAPER_MANAGER.collectPlugins()


@click.command(name="list-scrapers")
def list_scrapers():
    """Produce a list of available scrapers."""
    click.echo("Available scrapers:")
    if SCRAPER_MANAGER.getAllPlugins():
        for plugin in SCRAPER_MANAGER.getAllPlugins():
            click.echo("  {0} - {1}".format(plugin.name, plugin.description))
    else:
        click.secho("  No scrapers found.", fg="red")


main.add_command(list_scrapers)
main.add_command(scrape.scrape)
