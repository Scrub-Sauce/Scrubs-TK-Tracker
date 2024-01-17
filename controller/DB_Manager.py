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
    if conn:
        conn.close()
    if cursor:
        cursor.close()


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
        disconnect_from_db(cursor, conn)


def fetch_user_server(user_auto_id: int, server_auto_id: int):
    cursor, conn = connect_to_db()
    try:
        query = f"SELECT * FROM `users_servers` WHERE `user_id` = %s AND `server_id` = %s"
        cursor.execute(query, (user_auto_id, server_auto_id))
        result = cursor.fetchall()
        disconnect_from_db(cursor, conn)
        if result:
            return True, result[0]
        else:
            return False, None
    except mysql.connector.Error as err:
        print(f'Error encountered fetching User {user_auto_id} servers: {err}')
        disconnect_from_db(cursor, conn)

def fetch_top_15(server_id: int):
    cursor, conn = connect_to_db()
    try:
        query = ("SELECT `u`.`user_id`, `kill_count` "
                 "FROM `users` AS u "
                 "INNER JOIN `users_servers` AS us ON `u`.`auto_id` = `us`.`user_id` "
                 "INNER JOIN `servers` AS s ON `us`.`server_id` = `s`.`auto_id` "
                 "WHERE `us`.`server_id` = %s "
                 "ORDER BY `kill_count` DESC LIMIT 0, 15;"
                 )
        cursor.execute(query, (server_id,))
        result = cursor.fetchall()
        disconnect_from_db(cursor, conn)
        return True, result
    except mysql.connector.Error as err:
        print(f'Error encountered fetching the top 15 from {server_id}: {err}')
        return False, None


def fetch_history(killer_auto_id: int, server_auto_id:int):
    cursor, conn = connect_to_db()
    try:
        query = ("SELECT `tk`.`kill_id`, `u`.`user_id`, `tk`.`datetime` FROM `teamkills` AS tk "
                "INNER JOIN `users` AS u ON `u`.`auto_id` = `tk`.`victim` "
                "WHERE `tk`.`killer` = %s AND `tk`.`server_id` = %s "
                "ORDER BY `datetime` ASC;"
                 )
        cursor.execute(query, (killer_auto_id, server_auto_id))
        result = cursor.fetchall()
        disconnect_from_db(cursor, conn)
        return True, result
    except  mysql.connector.Error as err:
        print(f'Error encountered fetching kill history for killer {killer_auto_id} on server {server_auto_id}. {err}')
        return False, None


def insert_user(user: User):
    cursor, conn = connect_to_db()

    try:
        query = (
            "INSERT INTO `users` "
            "(user_id, username, user_displayname, user_globalname) "
            "VALUES (%s, %s, %s, %s)"
        )

        cursor.execute(
            query,
            (
                user.get_user_id(),
                user.get_username(),
                user.get_display_name(),
                user.get_global_name()
            ),
        )
        auto_id = cursor.lastrowid
        conn.commit()
        disconnect_from_db(cursor, conn)
        return True, auto_id

    except mysql.connector.Error as err:
        print(
            f'Error encountered inserting User: {user.get_username()} - {user.get_user_id()} into `users` table. {err}'
        )
        disconnect_from_db(cursor, conn)
        return False, None


def insert_server(server: Server):
    cursor, conn = connect_to_db()
    try:
        query = f"INSERT INTO `servers` (`server_name`, `server_id`, `owner_id`) VALUES (%s, %s, %s)"
        cursor.execute(query, (server.get_server_name(), server.get_server_id(), server.get_owner_id()))
        conn.commit()
        auto_id = cursor.lastrowid
        disconnect_from_db(cursor, conn)
        return True, auto_id

    except mysql.connector.Error as err:
        print(
            f'Error encountered inserting Server: {server.get_server_name()} - {server.get_server_id()} into `servers` table. {err}')
        return False, None


def insert_teamkill(tk: Teamkill):
    cursor, conn = connect_to_db()
    try:
        query = f"INSERT INTO `teamkills` (`killer`, `victim`, `server_id`, `datetime`) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (tk.get_killer_id(), tk.get_victim_id(), tk.get_server_id(), tk.get_datetime()))
        conn.commit()
        auto_id = cursor.lastrowid
        disconnect_from_db(cursor, conn)
        return True, auto_id
    except mysql.connector.Error as err:
        print(f"Error encountered inserting teamkill. {err}")
        disconnect_from_db(cursor, conn)
        return False, None


def insert_user_server(user_id: int, server_id: int, kill_count: int):
    cursor, conn = connect_to_db()
    try:
        query = f"INSERT INTO `users_servers` (`user_id`, `server_id`, `kill_count`) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, server_id, kill_count))
        conn.commit()
        auto_id = cursor.lastrowid
        disconnect_from_db(cursor, conn)
        return True, auto_id
    except mysql.connector.Error as err:
        print(f"Error Inserting User {user_id} - {server_id} into users_servers Table: {err}")
        disconnect_from_db(cursor, conn)
        return False, None


def update_user(user: User):
    cursor, conn = connect_to_db()
    try:
        query = (
            "UPDATE `users` "
            "SET `user_id` = %s, "
            "`username` = %s, "
            "`user_displayname` = %s, "
            "`user_globalname` = %s "
            "WHERE `auto_id` = %s"
        )
        cursor.execute(
            query,
            (
                user.get_user_id(),
                user.get_username(),
                user.get_display_name(),
                user.get_global_name(),
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
        cursor.execute(query,
                       (server.get_server_name(), server.get_server_id(), server.get_owner_id(), server.get_auto_id()))
        conn.commit()
        disconnect_from_db(cursor, conn)
        return True
    except mysql.connector.Error as err:
        print(
            f'Error encountered updating server: {server.get_server_name()} - {server.get_server_id()} in `servers` table. {err}')
        disconnect_from_db(cursor, conn)
        return False


def update_user_server(user_id: int, server_id: int, kill_count: int, auto_id: int):
    cursor, conn = connect_to_db()
    try:
        query = "UPDATE `users_servers` SET `user_id` = %s, `server_id` = %s, `kill_count` = %s WHERE `auto_id` = %s"
        cursor.execute(query, (user_id, server_id, kill_count, auto_id))
        conn.commit()
        disconnect_from_db(cursor, conn)
        return True
    except mysql.connector.Error as err:
        print(f'Error encountered updating user {user_id} server {server_id}: {err}')
        disconnect_from_db(cursor, conn)
        return False


def delete_tk(kill_id: int):
    cursor, conn = connect_to_db()
    try:
        query = "DELETE FROM `teamkills` WHERE `kill_id` = %s"
        cursor.execute(query, (kill_id,))
        conn.commit()
        disconnect_from_db(cursor, conn)
        return True
    except mysql.connector.Error as err:
        print(f'Error encountered deleting Kill ID: {kill_id}. {err}')
        return False

def delete_servers_tks(server_auto_id):
    cursor, conn = connect_to_db()
    try:
        print(f'{server_auto_id}')
        query = "DELETE FROM `teamkills` WHERE `server_id` = %s"
        cursor.execute(query, (server_auto_id,))
        conn.commit()
        disconnect_from_db(cursor, conn)
        return True
    except mysql.connector.Error as err:
        print(f'Error encountered wiping kills for server {server_auto_id}: {err}')
        return False
