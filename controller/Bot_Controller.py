import discord
from model.User import User
from model.Server import Server
from model.Teamkill import Teamkill
from controller.DB_Manager import *
from datetime import datetime
import pytz


def add_teamkill(killer: discord.Member, victim: discord.Member, server: discord.Guild, note: str = None):
    killer_exists, killer_data = fetch_user(killer.id)
    victim_exists, victim_data = fetch_user(victim.id)
    server_exists, server_data = fetch_server(server.id)
    central_tz = pytz.timezone('America/Chicago')
    teamkill_dt = datetime.now(central_tz)

    tmp_server = Server(server.name, server.id, server.owner_id)
    if server_exists:
        tmp_server.set_auto_id(server_data[0])
        status_s = update_server(tmp_server)
    else:
        status_s, s_auto_id = insert_server(tmp_server)
        tmp_server.set_auto_id(s_auto_id)

    tmp_killer = User(killer.id, killer.name, killer.display_name, killer.global_name)

    if killer_exists:
        tmp_killer.set_auto_id(killer_data[0])
        status_k = update_user(tmp_killer)
    else:
        status_k, k_auto_id = insert_user(tmp_killer)
        tmp_killer.set_auto_id(k_auto_id)

    tmp_victim = User(victim.id, victim.name, victim.display_name, victim.global_name)

    if victim_exists:
        tmp_victim.set_auto_id(victim_data[0])
        status_v = update_user(tmp_victim)
    else:
        status_v, v_auto_id = insert_user(tmp_victim)
        tmp_victim.set_auto_id(v_auto_id)

    killer_on_server, killer_server_data = fetch_user_server(tmp_killer.get_auto_id(), tmp_server.get_auto_id())

    if killer_on_server:
        tmp_killer.set_kill_count(killer_server_data[3])
        tmp_killer.set_death_count(killer_server_data[4])
        k_us_auto_id = killer_server_data[0]
        k_status_us = update_user_server(tmp_killer.get_auto_id(), tmp_server.get_auto_id(),
                                         tmp_killer.get_kill_count(), tmp_killer.get_death_count(),
                                         k_us_auto_id)
    else:
        k_status_us, k_us_auto_id = insert_user_server(tmp_killer.get_auto_id(), tmp_server.get_auto_id(),
                                                       tmp_killer.get_kill_count(), tmp_killer.get_death_count())

    victim_on_server, victim_server_data = fetch_user_server(tmp_victim.get_auto_id(), tmp_server.get_auto_id())

    if victim_on_server:
        tmp_victim.set_kill_count(victim_server_data[3])
        tmp_victim.set_death_count(victim_server_data[4])
        v_us_auto_id = victim_server_data[0]
        v_status_us = update_user_server(tmp_victim.get_auto_id(), tmp_server.get_auto_id(),
                                         tmp_victim.get_kill_count(), tmp_victim.get_death_count(),
                                         v_us_auto_id)
    else:
        v_status_us, v_us_auto_id = insert_user_server(tmp_victim.get_auto_id(), tmp_server.get_auto_id(),
                                                       tmp_victim.get_kill_count(), tmp_victim.get_death_count())

    tmp_teamkill = Teamkill(tmp_killer.get_auto_id(), tmp_victim.get_auto_id(), tmp_server.get_auto_id(), teamkill_dt)

    if note is not None:
        tmp_teamkill.set_note(note)

    status_tk, tk_auto_id = insert_teamkill(tmp_teamkill)
    tmp_teamkill.set_auto_id(tk_auto_id)
    if status_s and status_k and status_v and k_status_us and v_status_us and status_tk:
        return True, tmp_teamkill,
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
