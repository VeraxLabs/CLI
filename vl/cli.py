"""
CLI Driver
"""

import click
import logging
from logging.config import dictConfig
from config.logging import get_config


@click.command()
@click.option('--debug', is_flag=True)
def run(debug):
    """
    Main entry point into the application
    """
    dictConfig(get_config(debug))
    logger = logging.getLogger(__name__)
    logger.debug('Processing command line ...')
    click.echo('Welcome to VeraxLabs CLI')
