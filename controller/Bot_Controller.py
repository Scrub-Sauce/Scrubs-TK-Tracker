import discord
from model.User import User
from model.Server import Server
from model.Teamkill import Teamkill
from controller.DB_Manager import *
from datetime import datetime


def add_teamkill(killer: discord.Member, victim: discord.Member, server: discord.Guild):
    killer_exists, killer_data = fetch_user(killer.id)
    victim_exists, victim_data = fetch_user(victim.id)
    server_exists, server_data = fetch_server(server.id)
    teamkill_dt = datetime.now()

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
        tmp_killer.add_kill()
        status_us = update_user_server(tmp_killer.get_auto_id(), tmp_server.get_auto_id(), tmp_killer.get_kill_count(), killer_server_data[0])
    else:
        tmp_killer.add_kill()
        status_us, us_auto_id = insert_user_server(tmp_killer.get_auto_id(), tmp_server.get_auto_id(), tmp_killer.get_kill_count())

    tmp_teamkill = Teamkill(tmp_killer.get_auto_id(), tmp_victim.get_auto_id(), tmp_server.get_auto_id(), teamkill_dt)

    status_tk, tk_auto_id = insert_teamkill(tmp_teamkill)
    tmp_teamkill.set_auto_id(tk_auto_id)
    if status_s and status_k and status_v and status_us and status_tk:
        return True, tmp_teamkill,
    else:
        return False, None
