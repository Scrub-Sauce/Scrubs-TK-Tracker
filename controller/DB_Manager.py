import os
from datetime import datetime

import mysql.connector
import discord
from dotenv import load_dotenv
from model.User import User
from datetime import datetime

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


def add_teamkill(killer: discord.Member, victim: discord.Member, server: discord.Guild):
    existing_killer, killer_data = fetch_user(killer.id)
    existing_victim, victim_data = fetch_user(victim.id)
    teamkill_dt = datetime.now()

    if existing_killer:
        tmp_killer = User(killer.id, killer.name, killer.display_name, killer.global_name, killer_data[5] + 1)
        status_k = update_user(tmp_killer, killer_data[0])
        k_auto_id = killer_data[0]
    else:
        tmp_killer = User(killer.id, killer.name, killer.display_name, killer.global_name, 1)
        insert_user(tmp_killer)
        status_k, killer_data = fetch_user(tmp_killer.get_user_id())
        k_auto_id = killer_data[0]

    if existing_victim:
        tmp_victim = User(victim.id, victim.name, victim.display_name, victim.global_name, victim_data[5])
        status_v = update_user(tmp_victim, victim_data[0])
        v_auto_id = victim_data[0]
    else:
        tmp_victim = User(victim.id, victim.name, victim.display_name, victim.global_name, 0)
        insert_user(tmp_victim)
        status_v, victim_data = fetch_user(tmp_victim.get_user_id())
        v_auto_id = victim_data[0]

    insert_server(server)
    status_s, server_info = fetch_server(server.id)
    s_auto_id = server_info[0]
    status_tk = insert_teamkill(k_auto_id, v_auto_id, s_auto_id, teamkill_dt)

    if status_k and status_v and status_s and status_tk:
        return True
    else:
        return False


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
            f'Error encountered inserting User: {user.get_user_id()} into `users` table. {err}'
        )
        disconnect_from_db(cursor, conn)
        return False


def update_user(user: User, auto_id: int):
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
                auto_id,
            ),
        )
        conn.commit()
        disconnect_from_db(cursor, conn)
        return True
    except mysql.connector.Error as err:
        print(
            f'Error encountered updating User: {user.get_user_id()} in `users` table. {err}'
        )
        disconnect_from_db(cursor, conn)
        return False


def insert_server(server: discord.Guild):
    cursor, conn = connect_to_db()
    try:
        query = f"INSERT IGNORE INTO `servers` (`server_name`, `server_id`, `owner_id`) VALUES (%s, %s, %s)"
        cursor.execute(query, (server.name, server.id, server.owner_id))
        conn.commit()
        disconnect_from_db(cursor, conn)
        return True

    except mysql.connector.Error as err:
        print(f'Error encountered inserting Server: {server.name} into `servers` table. {err}')


def insert_teamkill(killer: int, victim: int, server: int, date: datetime):
    cursor, conn = connect_to_db()
    try:
        query = f"INSERT INTO `teamkills` (`killer`, `victim`, `server_id`, `datetime`) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (killer, victim, server, date))
        conn.commit()
        disconnect_from_db(cursor, conn)
        return True
    except mysql.connector.Error as err:
        print(f"Error encountered inserting teamkill. {err}")
        disconnect_from_db(cursor, conn)
        return False


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
