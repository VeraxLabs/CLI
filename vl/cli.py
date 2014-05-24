"""
CLI Driver
"""

import click


@click.command()
def run():
    """
    Main entry point into the application
    """
    click.echo('Welcome to VeraxLabs CLI')
