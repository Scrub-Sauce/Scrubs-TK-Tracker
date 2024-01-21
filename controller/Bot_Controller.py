import discord
from model.User import User
from model.Server import Server
from model.Teamkill import Teamkill
from controller.DB_Manager import *
from datetime import datetime
import pytz


def add_teamkill(killer: discord.Member, victim: discord.Member, server: discord.Guild, note: str = None):
    central_tz = pytz.timezone('America/Chicago')
    teamkill_dt = datetime.now(central_tz)

    status_s, tmp_server = create_server(server)

    status_k, tmp_killer = create_user(killer)
    status_v, tmp_victim = create_user(victim)

    k_status_us, k_us_auto_id = create_user_server(tmp_killer, tmp_server)
    v_status_us, v_us_auto_id = create_user_server(tmp_victim, tmp_server)

    tmp_teamkill = Teamkill(tmp_killer.get_auto_id(), tmp_victim.get_auto_id(), tmp_server.get_auto_id(), teamkill_dt)

    if note is not None:
        tmp_teamkill.set_note(note)

    status_tk, tk_auto_id = insert_teamkill(tmp_teamkill)
    tmp_teamkill.set_auto_id(tk_auto_id)
    if status_s and status_k and status_v and k_status_us and v_status_us and status_tk:
        return True, tmp_teamkill
    else:
        return False, None


def remove_tk(kill_id: int):
    delete_tk_status = delete_tk(kill_id)
    return delete_tk_status


def get_leaderboard_data(server: discord.Guild):
    s_status, server_data = fetch_server(server.id)
    server_auto_id = server_data[0]
    lb_status, leaderboard_data = fetch_top_15(server_auto_id)
    return lb_status, leaderboard_data


def wipe_server_tks(server: discord.Guild):
    s_status, server_data = fetch_server(server.id)
    server_auto_id = server_data[0]
    wipe_status = delete_servers_tks(server_auto_id)
    return wipe_status


def get_kill_history(killer: discord.Member):
    u_status, u_data = fetch_user(killer.id)
    s_status, s_data = fetch_server(killer.guild.id)
    user_auto_id = u_data[0]
    server_auto_id = s_data[0]
    us_status, us_data = fetch_user_server(user_auto_id, server_auto_id)
    ret_data = [us_data[3]]
    if u_status and s_status and us_status:
        h_status, h_data = fetch_kill_history(user_auto_id, server_auto_id)
        ret_data.append(h_data)
        if h_status:
            return True, ret_data
        else:
            return False, None
    else:
        return False, None


def get_death_history(victim: discord.Member):
    u_status, u_data = fetch_user(victim.id)
    s_status, s_data = fetch_server(victim.guild.id)
    user_auto_id = u_data[0]
    server_auto_id = s_data[0]
    us_status, us_data = fetch_user_server(user_auto_id, server_auto_id)
    ret_data = [us_data[4]]
    if u_status and s_status and us_status:
        h_status, h_data = fetch_death_history(user_auto_id, server_auto_id)
        ret_data.append(h_data)
        if h_status:
            return True, ret_data
        else:
            return False, None
    else:
        return False, None


def create_server(server: discord.Guild):
    server_exists, server_data = fetch_server(server.id)
    tmp_server = Server(server.name, server.id, server.owner_id)
    if server_exists:
        tmp_server.set_auto_id(server_data[0])
        status_s = update_server(tmp_server)
    else:
        status_s, s_auto_id = insert_server(tmp_server)
        tmp_server.set_auto_id(s_auto_id)

    return status_s, tmp_server


def create_user(user: discord.Member):
    user_exists, user_data = fetch_user(user.id)
    tmp_user = User(user.id, user.name, user.display_name, user.global_name)
    if user_exists:
        tmp_user.set_auto_id(user_data[0])
        status_u = update_user(tmp_user)
    else:
        status_u, u_auto_id = insert_user(tmp_user)
        tmp_user.set_auto_id(u_auto_id)

    return status_u, tmp_user


def create_user_server(user: User, server: Server):
    u_server_status, u_data = fetch_user_server(user.get_auto_id(), server.get_auto_id())
    if u_server_status:
        user.set_kill_count(u_data[3])
        user.set_death_count(u_data[4])
        u_us_auto_id = u_data[0]
        u_status_us = update_user_server(user.get_auto_id(), server.get_auto_id(),
                                         user.get_kill_count(), user.get_death_count(),
                                         u_us_auto_id)
    else:
        u_status_us, u_us_auto_id = insert_user_server(user.get_auto_id(), server.get_auto_id(),
                                                       user.get_kill_count(), user.get_death_count())

    return u_status_us, u_us_auto_id
