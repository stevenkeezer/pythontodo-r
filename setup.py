import os
import sqlite3
from termcolor import colored
from tabulate import tabulate
from colored import fg, attr
from datetime import datetime

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

conn = sqlite3.connect(DEFAULT_PATH)
cur = conn.cursor()


def setup_todos():
    sql = """
        CREATE TABLE IF NOT EXISTS todos(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            due_date INTEGER,
            user_id INTEGER,
            project_id INTEGER,
            status TEXT
        )
    """

    cur.execute(sql)
    conn.commit()


def setup_users():
    sql = """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL
        )
    """

    cur.execute(sql)
    conn.commit()


def setup_projects():
    sql = """
        CREATE TABLE IF NOT EXISTS projects(
            id INTEGER PRIMARY KEY,
            project STRING
        )
    """

    cur.execute(sql)
    conn.commit()


def setup_user_projects():
    sql = """
        CREATE TABLE IF NOT EXISTS user_projects(
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            project_id INTEGER
        )
    """

    cur.execute(sql)
    conn.commit()


def setupInitialTodos():
    sql = """
        INSERT INTO todos (name, due_date, email, status)
    """


setup_todos()
setup_users()
setup_projects()
setup_user_projects()
