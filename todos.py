import os
import sqlite3
from termcolor import colored
from tabulate import tabulate
from colored import fg, attr
from datetime import datetime

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

# POST http://localhost:5000/todos
conn = sqlite3.connect(DEFAULT_PATH)
cur = conn.cursor()


def add(user_id):
    print(colored("Enter message:", "red"))
    sql = """
        INSERT INTO todos(
            name,
            due_date,
            user_id,
            project_id,
            status
        ) VALUES (?, ?, ?, ?, ?)
    """
    name = input()

    cur.execute(sql, (name, datetime.now(), user_id, None, "incomplete"))
    conn.commit()

# DELETE http://localhost:5000/todos/1


def delete():
    sql = """ DELETE FROM todos WHERE id = ? """
    identity = input()

    cur.execute(sql, (identity,))
    conn.commit()

# PUT http://localhost:5000/todos/1


def complete():
    sql = """ UPDATE todos SET status = "complete" WHERE id = ? """
    identity = input()

    cur.execute(sql, (identity,))
    conn.commit()

# GET http://localhost:5000/todos


def incomplete():
    sql = """ UPDATE todos SET status = "incomplete" WHERE id = ? """
    identity = input()

    cur.execute(sql, (identity,))
    conn.commit()


def current_user(email):
    sql = """
        SELECT * FROM users WHERE (email) = (?)
    """
    cur.execute(sql, (email,))
    users = cur.fetchall()

    if len(users) == 1:
        return users[0]
    else:
        sql = """
            INSERT INTO users(
                email
            ) VALUES (?)
        """
        cur.execute(sql, (email, ))
        conn.commit()

        sql = """
          SELECT * FROM users WHERE (email) = (?)
        """
        cur.execute(sql, (email,))
        users = cur.fetchall()
        return users[0]


def new_project():
    print(colored("Enter project name:", "red"))
    sql = """
        INSERT INTO projects(
            project
        ) VALUES (?)
    """
    project = input()

    cur.execute(sql, (project, ))
    conn.commit()


def add_project(identity):
    print(colored("enter a user id:", "red"))
    user_id = input()
    print(colored("enter a project to work on:", "red"))
    project_id = input()

    sql = """
        UPDATE todos
        SET project_id = ?
        WHERE id = ?
    """

    cur.execute(sql, (project_id, user_id,))
    conn.commit()

    sql = """
        INSERT INTO user_projects(
            user_id,
            project_id
        ) VALUES (?,?)
    """

    cur.execute(sql, (identity, project_id,))
    conn.commit()


def list():
    print("   - all \n"
          "   - complete \n"
          "   - incomplete \n"
          "   - sort \n"
          "   - id \n"
          "   - users \n"
          "   - fire \n")
    command = input()
    if (command == '' or command == "all"):
        sql = """
            SELECT * FROM todos
        """

        cur.execute(sql)
        results = cur.fetchall()

        print(tabulate(results, headers=[
            colored("id", "green"), colored("name", "green"), colored("due date", "green"), colored("email", "green"), colored("project id", "green"), colored("status", "green")], tablefmt="orgtbl"))
        print("")

    elif (command == "complete" or command == "completed"):
        sql = """
            SELECT * FROM todos WHERE (status) IS "complete"
        """

        cur.execute(sql)
        results = cur.fetchall()

        print(tabulate(results, headers=[
            colored("id", "green"), colored("name", "green"), colored("due date", "green"), colored("email", "green"), colored("project id", "green"), colored("status", "green")], tablefmt="orgtbl"))
        print("")

    elif (command == "incomplete"):
        sql = """
            SELECT * FROM todos WHERE (status) IS "incomplete"
        """

        cur.execute(sql)
        results = cur.fetchall()

        print(tabulate(results, headers=[
            colored("id", "green"), colored("name", "green"), colored("due date", "green"), colored("email", "green"), colored("project id", "green"), colored("status", "green")], tablefmt="orgtbl"))
        print("")

    elif (command == "id"):
        print(colored("Which project are you looking for? Enter id.", "red"))
        identity = input()

        sql = """
            SELECT * FROM todos WHERE id = (?)
        """

        cur.execute(sql, (identity,))
        results = cur.fetchall()

        print(tabulate(results, headers=[
            colored("id", "green"), colored("name", "green"), colored("due date", "green"), colored("email", "green"), colored("project id", "green"), colored("status", "green")], tablefmt="orgtbl"))
        print("")

    elif (command == 'sort'):
        sql = """
            SELECT * FROM todos
            ORDER BY due_date DESC
        """

        cur.execute(sql)
        results = cur.fetchall()

        print(tabulate(results, headers=[
            colored("id", "green"), colored("name", "green"), colored("due date", "green"), colored("email", "green"), colored("project id", "green"),  colored("status", "green")], tablefmt="orgtbl"))
        print("")

    elif (command == 'users'):
        sql = """
            SELECT DISTINCT name FROM todos
        """

        cur.execute(sql)
        results = cur.fetchall()

        print(tabulate(results, headers=[
            colored("id", "green"), colored("name", "green"), colored("due date", "green"), colored("email", "green"), colored("project id", "green"), colored("status", "green")], tablefmt="orgtbl"))
        print("")

    elif (command == 'fire'):
        # if users id is not in todos id print names
        sql = """
            SELECT id, email FROM users WHERE id NOT IN(SELECT id FROM todos)
        """

        cur.execute(sql)
        results = cur.fetchall()

        print(tabulate(results, headers=[
            colored("id", "green"), colored("Lazy Asses", "green"), colored("due date", "green"), colored("email", "green"), colored("project id", "green"), colored("status", "green")], tablefmt="orgtbl"))
        print("")


if __name__ == '__main__':
    # try:
    print(colored('Whats your email?', "red"))
    email = input()
    user = current_user(email)
    print('')

    while True:
        print(colored("What do you want to do {}".format(
            user[1]) + "?", "red"))
        print(
            "-- add \n"
            "-- delete \n"
            "-- list \n"
            "   - all \n"
            "   - complete \n"
            "   - incomplete \n"
            "   - sort \n"
            "   - id \n"
            "   - users \n"
            "   - fire \n"
            "-- complete \n"
            "-- incomplete \n"
            "-- new project \n"
            "-- add project \n"
        )
        print(colored("Enter:", "red"))

        choice = input()

        if choice == "add":
            add(user[0])

        elif choice == "list":
            list()

        elif choice == "delete":
            delete()

        elif choice == "complete":
            complete()

        elif choice == "incomplete":
            incomplete()

        elif choice == "new project":
            new_project()

        elif choice == "add project":
            add_project(user[0])
    # except:
    #     print('error')
