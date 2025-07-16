#!/usr/bin/env python3

import Ice
import sys

# -------------------- Configuration --------------------#

iceslice = "/usr/share/slice/MumbleServer.ice"
iceincludepath = "/usr/share/ice/slice"
serverport = 64738
icehost = "127.0.0.1"
iceport = 6502
icesecret = "YOUR_ICE_SECRET"
messagesizemax = "65535"

# -------------------- Mumble-Server Data --------------------#

show_users_all = True
show_users_muted = True
show_users_unregistered = True
show_users_registered = True
show_ban_count = True
show_channel_count = True
show_uptime = True

# -------------------- ICE Initialization --------------------#

Ice.loadSlice(f"--all -I{iceincludepath} {iceslice}")
import MumbleServer

props = Ice.createProperties([])
props.setProperty("Ice.MessageSizeMax", str(messagesizemax))
props.setProperty("Ice.ImplicitContext", "Shared")
props.setProperty("Ice.Default.EncodingVersion", "1.0")

id = Ice.InitializationData()
id.properties = props

ice = None
server = None

try:
    with Ice.initialize(sys.argv, id) as communicator:
        context = {"secret": icesecret}

        base = communicator.stringToProxy(f"Meta:tcp -h {icehost} -p {iceport} -t 60000")
        meta = MumbleServer.MetaPrx.checkedCast(base)

        if not meta:
            print("❌ Could not cast proxy to MetaPrx.")
            sys.exit(1)

        server = meta.getServer(1, context)
        if not server:
            print("❌ Could not get server instance.")
            sys.exit(1)


        users_all = 0
        users_muted = 0
        users_unregistered = 0
        users_registered = 0

        onlineusers = server.getUsers()
        channels = server.getChannels()

        for user in onlineusers.values():
            if show_users_all:
                users_all += 1
            if show_users_muted and (user.mute or user.selfMute or user.suppress):
                users_muted += 1
            if show_users_unregistered and user.userid == -1:
                users_unregistered += 1
            if show_users_registered and user.userid > 0:
                users_registered += 1

        if len(sys.argv) > 1:
            arg = sys.argv[1].lower()
            if arg == "users":
                print(users_all)
            elif arg == "muted":
                print(users_muted)
            elif arg == "registered":
                print(users_registered)
            elif arg == "unregistered":
                print(users_unregistered)
            elif arg == "bans":
                print(len(server.getBans()))
            elif arg == "channels":
                print(len(channels))
            elif arg == "uptime":
                print(f"{server.getUptime() // 60}")
            else:
                print("Unknown argument:", arg)
                sys.exit(5)
        else:
            print('Help for Zabbix Mumble Script\n')
            print('Usage: ./zabbix-mumble.py <command>\n')
            print('Available commands:')
            print('  users         - Number of users online')
            print('  muted         - Number of users muted')
            print('  registered    - Number of registered users')
            print('  unregistered  - Number of unregistered users')
            print('  bans          - Count of bans on server')
            print('  channels      - Channel count')
            print('  uptime        - Server uptime in minutes')

except Ice.Exception as e:
    print("❌ ICE Exception:", e)
    sys.exit(1)

