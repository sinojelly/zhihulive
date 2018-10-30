import asyncio
import click
from aiohttp import web

from network.crawl import Crawler
from network.transform import Transformer
from models import create_table, drop_table
from web.main import app


@click.group()
def cli():
    pass


@click.command()
def initdb():
    click.echo('Initialized the database and create table')
    create_table()


@click.command()
def dropdb():
    click.echo('Dropped the database')
    drop_table()


@click.command()
def crawl():
    click.echo('Start crawl')
    loop = asyncio.get_event_loop()
    crawler = Crawler(loop=loop)
    loop.run_until_complete(crawler.crawl())
    click.echo('Finished in {:.3f} seconds'.format(crawler.t1 - crawler.t0))


@click.command()
def crawlvip():
    click.echo('Start crawl_list')
    loop = asyncio.get_event_loop()
    crawler = Crawler(loop=loop)
    loop.run_until_complete(crawler.crawl_vip())
    click.echo('Finished in {:.3f} seconds'.format(crawler.t1 - crawler.t0))


@click.command()
def transform():
    click.echo('Start transform')
    loop = asyncio.get_event_loop()
    transformer = Transformer(loop=loop)
    loop.run_until_complete(transformer.transform())
    click.echo('Finished in {:.3f} seconds'.format(transformer.t1 - transformer.t0))


@click.command()
def webserver():
    click.echo('Start webserver')
    app.router.add_static('/static', 'web/static')
    web.run_app(app)


cli.add_command(initdb)
cli.add_command(dropdb)
cli.add_command(crawl)
cli.add_command(crawlvip)
cli.add_command(transform)
cli.add_command(webserver)

if __name__ == '__main__':
    from config import *
    cli()
