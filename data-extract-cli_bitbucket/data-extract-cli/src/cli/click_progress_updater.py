from __future__ import annotations
from click._termui_impl import ProgressBar
from cli.progress_updater import ProgressUpdater
import click


class ClickProgressUpdater(ProgressUpdater):
    progress_bar: ProgressBar or None
    click_instance: click

    def __init__(self, progress_bar: ProgressBar = None):
        self.progress_bar = progress_bar
        self.loadingBar = ''

    def update(self, message: str = None, data: dict = None) -> ClickProgressUpdater:
        click.secho('▓', fg='blue', nl=False)
        if (message):
            click.secho(message, fg='blue')

        return self

    def success(self, message: str) -> ClickProgressUpdater:
        click.secho(message, fg='green')

        return self

    def error(self, error: str) -> ClickProgressUpdater:
        click.secho(f"ERROR: {error}", fg='red', error=True)

        return self

    def set_length(self, length: int) -> ClickProgressUpdater:
        return self
