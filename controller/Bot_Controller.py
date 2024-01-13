import discord
from model.User import User
from model.Server import Server
from model.Teamkill import Teamkill
from controller.DB_Manager import *
from datetime import datetime


def add_teamkill(killer: discord.Member, victim: discord.Member, server: discord.Guild):
    existing_killer, killer_data = fetch_user(killer.id)
    existing_victim, victim_data = fetch_user(victim.id)
    teamkill_dt = datetime.now()

    if existing_killer:
        tmp_killer = User(killer.id, killer.name, killer.display_name, killer.global_name, killer_data[5])
        tmp_killer.add_kill()
        tmp_killer.set_auto_id(killer_data[0])
        status_k = update_user(tmp_killer)
    else:
        tmp_killer = User(killer.id, killer.name, killer.display_name, killer.global_name, 1)
        insert_user(tmp_killer)
        status_k, killer_data = fetch_user(tmp_killer.get_user_id())
        tmp_killer.set_auto_id(killer_data[0])

    if existing_victim:
        tmp_victim = User(victim.id, victim.name, victim.display_name, victim.global_name, victim_data[5])
        tmp_victim.set_auto_id(victim_data[0])
        status_v = update_user(tmp_victim)
    else:
        tmp_victim = User(victim.id, victim.name, victim.display_name, victim.global_name, 0)
        insert_user(tmp_victim)
        status_v, victim_data = fetch_user(tmp_victim.get_user_id())
        tmp_victim.set_auto_id(victim_data[0])

    status_s, server_data = fetch_server(server.id)
    tmp_server = Server(server.name, server.id, server.owner_id)

    if status_s:
        tmp_server.set_auto_id(server_data[0])
        update_server(tmp_server)
    else:
        insert_server(tmp_server)
        status_s, server_data = fetch_server(server.id)
        tmp_server.set_auto_id(server_data[0])

    tmp_teamkill = Teamkill(tmp_killer.get_auto_id(), tmp_victim.get_auto_id(), tmp_server.get_auto_id(), teamkill_dt)
    status_tk = insert_teamkill(tmp_teamkill)

    if status_k and status_v and status_s and status_tk:
        return True
    else:
        return False
