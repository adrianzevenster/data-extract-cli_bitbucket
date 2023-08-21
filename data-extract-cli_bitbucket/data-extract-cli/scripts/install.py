import click
from pyfiglet import Figlet
import os
import subprocess

f = Figlet(font='slant')
click.secho(f.renderText('Airvantage'), fg='blue')
click.secho(
    'Running the Airvantage ETL CLI tool installation...', fg='yellow')

app_path = os.path.expanduser(os.path.join("~", '.airvantage-etl'))
click.secho(f"Copying assets to {app_path} ...", fg='green')
if os.path.exists('main'):
    p = subprocess.Popen(f"rsync -a main/* {app_path}/",
                         stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
    output, error = p.communicate()

env_path = os.path.expanduser(os.path.join(app_path, '.env'))
if os.path.exists('.env.example'):
    p = subprocess.Popen(f"cp .env.example {env_path}",
                         stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
    output, error = p.communicate()

if click.confirm('Do you want to enter the config?'):
    """
    Tenants config
    """
    config = {"APP_ENV": "production"}

    #    MTC
    config['MTC_HOST'] = click.prompt(
        'Database hostname or IP for MTC', type=str)
    config['MTC_USER'] = click.prompt('Database user for MTC', type=str)
    config['MTC_PW'] = click.prompt(
        f"Database password for MTC user '{config['MTC_USER']}'", type=str)
    config['MTC_STORAGE_BUCKET'] = click.prompt(
        "Storage bucket key for MTC", type=str, default='mtc-av')
    click.secho('------------------------', fg='green')

    #   TMCEL
    config['TMCEL_HOST'] = click.prompt(
        'Database hostname or IP for TMCEL', type=str)
    config['TMCEL_USER'] = click.prompt('Database user for TMCEL', type=str)
    config['TMCEL_PW'] = click.prompt(
        f"Database password for TMCEL user '{config['TMCEL_USER']}'", type=str)
    config['TMCEL_STORAGE_BUCKET'] = click.prompt(
        "Storage bucket key for TMCEL", type=str, default='tmcel-av')
    click.secho('------------------------', fg='green')

    #   DIGICELL
    config['DIGICELL_HOST'] = click.prompt(
        'Database hostname or IP for DIGICELL', type=str)
    config['DIGICELL_USER'] = click.prompt(
        'Database user for DIGICELL', type=str)
    config['DIGICELL_PW'] = click.prompt(
        f"Database password for DIGICELL user '{config['DIGICELL_USER']}'", type=str)
    config['DIGICELL_STORAGE_BUCKET'] = click.prompt(
        "Storage bucket key for DIGICELL", type=str, default='digicel-jamaica-av')
    click.secho('------------------------', fg='green')

    #   DIGIBELIZE
    config['DIGIBELIZE_HOST'] = click.prompt(
        'Database hostname or IP for DIGIBELIZE', type=str)
    config['DIGIBELIZE_USER'] = click.prompt(
        'Database user for DIGIBELIZE', type=str)
    config['DIGIBELIZE_PW'] = click.prompt(
        f"Database password for DIGIBELIZE user '{config['DIGIBELIZE_USER']}'", type=str)
    config['DIGIBELIZE_STORAGE_BUCKET'] = click.prompt(
        "Storage bucket key for DIGIBELIZE", type=str, default='digibelize-av')
    click.secho('------------------------', fg='green')

    config['AWS_PROFILE'] = click.prompt(
        'AWS profile to use in `~/.aws/credentials`', type=str, default='airvantage')

    click.secho('Configuring installation...', fg='green')

    # Export the environment variables to a bash-compliant file
    # that will pick them up when starting a bash session
    with open(env_path, "a+") as outfile:
        with click.progressbar(config) as bar:
            for key in bar:
                outfile.write(f"{key}=\"{config[key]}\"\n")
        outfile.close()

# create a bin symlink so that we can call the tool as a global command
# using `airvantage-etl`
global_cmd_path = os.path.expanduser('~/.local/bin/airvantage-etl')

if os.path.exists(os.path.expanduser('~/.local/bin')) == False:
    os.makedirs(os.path.expanduser('~/.local/bin'))
    bashrc_uri = os.path.expanduser('~/.bashrc')

    with open(bashrc_uri, "a+") as outfile:
        outfile.write('PATH="$HOME/.local/bin/:$PATH"\n')
        outfile.close()

    p = subprocess.Popen(f"source {bashrc_uri}",
                         stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
    output, error = p.communicate()

if os.path.exists(global_cmd_path) == False:
    script_uri = os.path.abspath(os.path.join(f"{app_path}", "main"))
    p = subprocess.Popen(f"ln -s {script_uri} {global_cmd_path}",
                         stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
    output, error = p.communicate()

click.secho('Installation finished.', fg='green')
click.secho(
    'You can now use `airvantage-etl` in the terminal', fg='blue')
