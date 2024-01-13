import os
import mysql.connector
from dotenv import load_dotenv
from model.User import User
from model.Teamkill import Teamkill
from model.Server import Server

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        return cursor, conn
    except mysql.connector.Error as err:
        print(f'Error encountered while connecting to DB: {err}')
        exit(1)


def disconnect_from_db(cursor, conn):
    cursor.close()
    conn.close()


def fetch_user(user_id: int):
    cursor, conn = connect_to_db()
    try:
        query = f"SELECT * FROM `users` WHERE `user_id` = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        disconnect_from_db(cursor, conn)
        if result:
            return True, result[0]
        else:
            return False, None

    except mysql.connector.Error as err:
        print(f'Error encountered fetching User: {user_id} from DB: {err}')
        disconnect_from_db(cursor, conn)


def fetch_server(server_id: int):
    cursor, conn = connect_to_db()
    try:
        query = f"SELECT * FROM `servers` WHERE `server_id` = %s"
        cursor.execute(query, (server_id,))
        result = cursor.fetchall()
        disconnect_from_db(cursor, conn)
        if result:
            return True, result[0]
        else:
            return False, None

    except mysql.connector.Error as err:
        print(f'Error encountered fetching Server: {server_id} from DB: {err}')


def insert_user(user: User):
    cursor, conn = connect_to_db()

    try:
        query = (
            "INSERT INTO `users` "
            "(user_id, username, user_displayname, user_globalname, kill_count) "
            "VALUES (%s, %s, %s, %s, %s)"
        )

        cursor.execute(
            query,
            (
                user.get_user_id(),
                user.get_username(),
                user.get_display_name(),
                user.get_global_name(),
                user.get_kill_count(),
            ),
        )

        conn.commit()
        disconnect_from_db(cursor, conn)
        return True

    except mysql.connector.Error as err:
        print(
            f'Error encountered inserting User: {user.get_username()} - {user.get_user_id()} into `users` table. {err}'
        )
        disconnect_from_db(cursor, conn)
        return False


def insert_server(server: Server):
    cursor, conn = connect_to_db()
    try:
        query = f"INSERT INTO `servers` (`server_name`, `server_id`, `owner_id`) VALUES (%s, %s, %s)"
        cursor.execute(query, (server.get_server_name(), server.get_server_id(), server.get_owner_id()))
        conn.commit()
        disconnect_from_db(cursor, conn)
        return True

    except mysql.connector.Error as err:
        print(f'Error encountered inserting Server: {server.get_server_name()} - {server.get_server_id()} into `servers` table. {err}')


def insert_teamkill(tk: Teamkill):
    cursor, conn = connect_to_db()
    try:
        query = f"INSERT INTO `teamkills` (`killer`, `victim`, `server_id`, `datetime`) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (tk.get_killer_id(), tk.get_victim_id(), tk.get_server_id(), tk.get_datetime()))
        conn.commit()
        disconnect_from_db(cursor, conn)
        return True
    except mysql.connector.Error as err:
        print(f"Error encountered inserting teamkill. {err}")
        disconnect_from_db(cursor, conn)
        return False


def update_user(user: User):
    cursor, conn = connect_to_db()
    try:
        query = (
            "UPDATE `users` "
            "SET `user_id` = %s, "
            "`username` = %s, "
            "`user_displayname` = %s, "
            "`user_globalname` = %s, "
            "`kill_count` = %s "
            "WHERE `auto_id` = %s"
        )
        cursor.execute(
            query,
            (
                user.get_user_id(),
                user.get_username(),
                user.get_display_name(),
                user.get_global_name(),
                user.get_kill_count(),
                user.get_auto_id(),
            ),
        )
        conn.commit()
        disconnect_from_db(cursor, conn)
        return True
    except mysql.connector.Error as err:
        print(
            f'Error encountered updating User: {user.get_username()} - {user.get_user_id()} in `users` table. {err}'
        )
        disconnect_from_db(cursor, conn)
        return False


def update_server(server: Server):
    cursor, conn = connect_to_db()
    try:
        query = "UPDATE `servers` SET `server_name` = %s,`server_id` = %s, `owner_id` = %s WHERE `auto_id` = %s"
        cursor.execute(query, (server.get_server_name(), server.get_server_id(), server.get_owner_id(), server.get_auto_id()))
        conn.commit()
        disconnect_from_db(cursor, conn)
        return True
    except mysql.connector.Error as err:
        print(f'Error encountered updating server: {server.get_server_name()} - {server.get_server_id()} in `servers` table. {err}')
        disconnect_from_db(cursor, conn)
        return False
