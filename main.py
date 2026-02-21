import sys
import os
import asyncio

from colorama import Fore, Style, init
import discord
from discord.ext import commands
import sqlite3

F = Fore
R = Style.RESET_ALL

init(autoreset=True)

token_file = "bot_token.txt"
if not os.path.exists(token_file):
    bot_token = input("Enter the bot token: ")
    with open(token_file, "w") as f:
        f.write(bot_token)
else:
    with open(token_file, "r") as f:
        bot_token = f.read().strip()

if not os.path.exists("db"):
    os.makedirs("db")
    print(F.GREEN + "db folder created" + R)

databases = {
    "conn_alliance": "db/alliance.sqlite",
    "conn_giftcode": "db/giftcode.sqlite",
    "conn_changes": "db/changes.sqlite",
    "conn_users": "db/users.sqlite",
    "conn_settings": "db/settings.sqlite",
}

connections = {name: sqlite3.connect(path) for name, path in databases.items()}

print(F.GREEN + "Database connections have been successfully established." + R)

def create_tables():
    with connections["conn_changes"] as conn_changes:
        conn_changes.execute("""CREATE TABLE IF NOT EXISTS nickname_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fid INTEGER,
            old_nickname TEXT,
            new_nickname TEXT,
            change_date TEXT
        )""")
        conn_changes.execute("""CREATE TABLE IF NOT EXISTS furnace_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fid INTEGER,
            old_furnace_lv INTEGER,
            new_furnace_lv INTEGER,
            change_date TEXT
        )""")

    with connections["conn_settings"] as conn_settings:
        conn_settings.execute("""CREATE TABLE IF NOT EXISTS botsettings (
            id INTEGER PRIMARY KEY,
            channelid INTEGER,
            giftcodestatus TEXT
        )""")
        conn_settings.execute("""CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY,
            is_initial INTEGER
        )""")

    with connections["conn_users"] as conn_users:
        conn_users.execute("""CREATE TABLE IF NOT EXISTS users (
            fid INTEGER PRIMARY KEY,
            nickname TEXT,
            furnace_lv INTEGER DEFAULT 0,
            kid INTEGER,
            stove_lv_content TEXT,
            alliance TEXT
        )""")

    with connections["conn_giftcode"] as conn_giftcode:
        conn_giftcode.execute("""CREATE TABLE IF NOT EXISTS gift_codes (
            giftcode TEXT PRIMARY KEY,
            date TEXT
        )""")
        conn_giftcode.execute("""CREATE TABLE IF NOT EXISTS user_giftcodes (
            fid INTEGER,
            giftcode TEXT,
            status TEXT,
            PRIMARY KEY (fid, giftcode),
            FOREIGN KEY (giftcode) REFERENCES gift_codes (giftcode)
        )""")

    with connections["conn_alliance"] as conn_alliance:
        conn_alliance.execute("""CREATE TABLE IF NOT EXISTS alliancesettings (
            alliance_id INTEGER PRIMARY KEY,
            channel_id INTEGER,
            interval INTEGER
        )""")
        conn_alliance.execute("""CREATE TABLE IF NOT EXISTS alliance_list (
            alliance_id INTEGER PRIMARY KEY,
            name TEXT
        )""")

    print(F.GREEN + "All tables checked." + R)

create_tables()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

async def load_cogs():
    import os
    skip = {"bear_event_types", "gift_captchasolver", "gift_operationsapi", "login_handler"}
    cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")
    cogs = [
        f[:-3] for f in os.listdir(cogs_dir)
        if f.endswith(".py") and not f.startswith("_") and f[:-3] not in skip
    ]
    cogs.sort()

    for cog in cogs:
        try:
            await bot.load_extension(f"cogs.{cog}")
            print(f"✓ Loaded cog: {cog}")
        except Exception as e:
            print(f"✗ Failed to load cog {cog}: {e}")

@bot.event
async def on_ready():
    try:
        print(f"{F.GREEN}Logged in as {F.CYAN}{bot.user}{R}")
        await bot.tree.sync()
    except Exception as e:
        print(f"Error syncing commands: {e}")

async def main():
    await load_cogs()
    await bot.start(bot_token)

if __name__ == "__main__":
    asyncio.run(main())
