import click
import logging
from services.notification_service import NotificationService
from data_extraction.data_extraction_provider import DataExtractionProvider
from pyfiglet import Figlet
from cli.click_progress_updater import ClickProgressUpdater

_QUIET = False


@click.group()
# @click.option('--dry-run', type=bool, help="Runs the command but only outputs what will happen. Useful for testing connections or side-effects.", default=False)
@click.option('--quiet', type=bool, help="Runs the command but silences logging output.", default=False)
def cli(quiet):
    _QUIET = quiet
    if (_QUIET):
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.INFO)
        f = Figlet(font='slant')
        click.secho(f.renderText('Airvantage'), fg='blue')
    pass


@cli.command()
@click.option("-p", "--input-json-path", type=str, required=True, help="The path to the json file for extract input. Contact airvantage@symbyte.tech for exact structure.")
@click.option("-cs", "--chunksize", type=int, default=10000, required=True, help="The pandas chunksize, i.e. how many rows should be in each fraction of the table.")
@click.option("--id", type=str, default='', required=False, help="Set your own extract ID if necessary.")
def extract(input_json_path, chunksize, id):
    dataExtractionService = DataExtractionProvider.provide()
    if (_QUIET == False):
        dataExtractionService.set_progress_updater(
            ClickProgressUpdater(None)
        )
    dataExtractionService.prepare_extract(
        input_json_path, chunksize, id or ''
    ).run_extract()


@cli.command()
@click.option("--channel", type=str, required=True, help="Can be one of `databricks`")
@click.option("--extract-guid", type=str, required=True, help="The unique extract guid`")
def notify():
    notificationService = NotificationService()
    notificationService.notify()


if __name__ == '__main__':
    try:
        cli()
    except Exception as err:
        logging.error(
            f"Error encountered. Check run file for details.")
        logging.error(err)
