#!/usr/bin/env python
import click
import requests
import arrow
import jinja2
import settings
import time
import sys
import os
import os.path
from os import path
from yaspin import yaspin
from yaspin.spinners import Spinners

@click.group()
def cli():
    pass


def get_cookie_dict():
    expires = arrow.utcnow().format('ddd, DD MMM YYYY HH:mm:ss') + ' GMT'
    return dict(session="{session_key}; Path=/; Domain={aoc_domain}; Expires={expires};".format(
        session_key=settings.SESSION_KEY,
        aoc_domain=settings.AOC_DOMAIN,
        expires=expires
    ))


def get_path_to_data(year, day):
    return settings.DATA_PATH.format(year=year) + '/' + settings.DAY_FILE_FORMAT.format(day=day.zfill(2))


def setup_code_file(year, day, overwrite_existing=False):
    code_filename_path = settings.CODE_FILENAME_FORMAT.format(day=day.zfill(2))
    if path.exists(code_filename_path) and not overwrite_existing:
        print("Code file at {code_filename_path} exists, exiting".format(code_filename_path=code_filename_path))
        sys.exit(1)

    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="./"))
    template = template_env.get_template(settings.CODE_TEMPLATE_FILE)
    outputText = template.render(code_path=get_path_to_data(year, day))

    with open(code_filename_path, 'w') as code_file:
        code_file.write(outputText)


def download_data(year, day, overwrite_existing=False):
    try:
        os.makedirs(settings.DATA_PATH.format(year=year))
    except FileExistsError:
        pass
    cookies = get_cookie_dict()
    r = requests.get('{url}/{year}/day/{day}/input'.format(url=settings.AOC_URL, year=year, day=day,), cookies=cookies)

    with open(get_path_to_data(year=year, day=day), 'w') as download_file:
        download_file.write(r.text)

    setup_code_file(year=year, day=day, overwrite_existing=overwrite_existing)


@click.command()
@click.argument("day")
@click.option('--year', default=arrow.utcnow().year, help='Year to pull from')
@click.option('--overwrite_existing', default=False, type=bool, help='Should we overwrite an existing code file')
def download(year, day, overwrite_existing):
    print("Downloading input for day %s" % day)

    download_data(year, day, overwrite_existing)


@click.command()
def wait():
    release = arrow.utcnow().to(settings.AOC_TIMEZONE).replace(
        hour=settings.AOC_RELEASE_HOUR,
        minute=settings.AOC_RELEASE_MINUTE,
        second=0,
        microsecond=0
    )

    if release.timestamp < arrow.utcnow().to(settings.AOC_TIMEZONE).timestamp:
        release = release.replace(day=release.day + 1)

    local = arrow.utcnow().to(settings.TIMEZONE)

    with yaspin() as spin:
        spin.spinner = Spinners.christmas
        spin.text = "Waiting for today's contest %s" % release.humanize()
        while release.timestamp - local.timestamp > 0:
            time.sleep(1)
            local = arrow.utcnow().to(settings.TIMEZONE)

            spin.text = "Waiting for today's contest %s" % release.humanize()

    download_data(release.year, str(release.day))
    print("Everything is ready, let's go!")


@click.command()
@click.argument("day")
@click.option('--year', default=arrow.utcnow().year, help='Year to pull from')
def view(year, day):
    print("Viewing day %s" % day)
    cookies = get_cookie_dict()
    r = requests.get('{url}/{year}/day/{day}'.format(url=settings.AOC_URL, year=year, day=day,), cookies=cookies)

    print(r.text)


cli.add_command(view)
cli.add_command(download)
cli.add_command(wait)


if __name__ == '__main__':
    cli()
