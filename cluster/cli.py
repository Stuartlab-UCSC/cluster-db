"""
cli exposed via flask *function-name

wrap create_app with the @command_line_interface decorator

`export FLASK_APP=cluster` is necessary.

`flask --help` to show available functions

to add another cli write a click.command() and add the function name into CLICK_COMMANDS (at bottom of file)
"""
import datetime
import os
import click
from decorator import decorator

from flask import current_app
from flask.cli import with_appcontext

from cluster.database import db
from cluster.database.add_entries import add_entries
from cluster.database.user_models import User


@click.command(help="Add a new user to the user database.")
@click.argument('email')
@click.argument('password')
@with_appcontext
def create_user(email, password):
    user_manager = current_app.user_manager
    user = {
        "email": email,
        "password": user_manager.hash_password(password),
        "email_confirmed_at": datetime.datetime.utcnow(),
    }

    entry = [(User, user)]
    add_entries(db.session, entry)

@click.command(help="Print all user emails.")
@with_appcontext
def all_users():
    print("\n".join([u.email for u in User.query.all()]))


@click.command(help="Remove cluster_user.db")
@with_appcontext
def clear_users():
    print("removing", current_app.config["USERDB"])
    os.remove(current_app.config["USERDB"])


@click.command(help="Add a new worksheet.")
@click.argument('email')
@click.argument('worksheet_name')
@click.argument('dataset_name')
@click.argument('cluster_name')
@with_appcontext
def create_worksheet(email, worksheet_name, dataset_name, cluster_name):
    from cluster.database.user_models import add_worksheet_entries
    add_worksheet_entries(
        db.session,
        email,
        worksheet_name,
        organ=None,
        species=None,
        dataset_name=dataset_name,
        cluster_name=cluster_name,
    )


CLICK_COMMANDS = [create_user, create_worksheet, all_users, clear_users]


@decorator
def command_line_interface(func, click_commands=CLICK_COMMANDS, *args, **kwargs):
    app = func(*args, **kwargs)
    for command in click_commands:
        app.cli.add_command(command)

    return app