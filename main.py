#!/bin/python3.7

import os
import sys

import discord

from dotenv import load_dotenv

number_emotes = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
image_types = ["png", "jpeg", "gif", "jpg"]


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


def get_attributes(atr_string):
    return atr_string.split('"')[1::2]


def tag_user(author):
    return "<@" + str(author.id) + ">"


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if await MyClient.__show_graphic(message):
            return

        if await MyClient.__create_poll(message):
            return

        if await MyClient.__list_graphic(message):
            return

        if await MyClient.__print_help(message):
            return

        if await MyClient.__add_graphic(message):
            return

        if await MyClient.__sync_with_git(message):
            return

    @staticmethod
    async def __create_poll(message):
        if message.content.startswith('!poll '):
            attributes = get_attributes(message.content[6:])
            if len(attributes) < 3:
                await message.channel.send("Chtělo by to v anketě něco na výběr.")
                return True

            if len(attributes) > 10:
                await message.channel.send("Zas tolik možností nedávej.")
                return True

            msg_str = message.author.name + ": " + attributes[0] + "\n"
            for i in range(1, len(attributes)):
                msg_str += number_emotes[i]
                msg_str += " "
                msg_str += attributes[i]
                msg_str += "\n"

            msg = await message.channel.send( msg_str)
            await message.delete()

            for i in range(1, len(attributes)):
                await msg.add_reaction(number_emotes[i])

            return True
        else:
            return False

    @staticmethod
    async def __show_graphic(message):
        if not message.content.startswith('!'):
            return False
        str = message.content[1:]
        graphic = 'graphic'
        for f in os.listdir(graphic):
            if f.endswith('.gif') or f.endswith('.png') or f.endswith('.jpg'):
                if str == os.path.splitext(f)[0]:
                    await message.channel.send(message.author.name + ":", file=discord.File(os.path.join(graphic, f)))
                    await message.delete()
                    return True

        return False

    @staticmethod
    async def __list_graphic(message):
        if not message.content.startswith('!all_graphic'):
            return False
        ret = ''
        graphic = 'graphic'
        for f in os.listdir(graphic):
            ret += '!'
            ret += os.path.splitext(f)[0]
            ret += '\n'
        await message.channel.send(ret)
        await message.delete()
        return True

    @staticmethod
    async def __print_help(message):
        if not message.content.startswith('!help'):
            return False
        msg = tag_user(message.author) + "\n"
        msg += '!poll "popis" "první možnost" "druhá možnost" - Vytvoří anketu. Může obsahovat dvě až devět možností.\n'
        msg += '!all_graphic - zobrazí všechny příkay pro vložení všech obrázků nebo gifů.\n'
        msg += '!sync - synchroniuje data s projektem na githubu.\n'
        if message.author.guild_permissions.administrator:
            msg += '!add_graphic - přidá do možné grafiky nový obrázek.\n'
        await message.channel.send(msg)
        await message.delete()

    @staticmethod
    async def __add_graphic(message):
        if not message.content.startswith('!add_graphic'):
            return False
        if message.author.guild_permissions.administrator:
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(image) for image in image_types):
                    if os.path.isfile('graphic' + attachment.filename):
                        message.channel.send('Obrázek s tímto názvem již existuje.')
                    else:
                        await attachment.save(os.path.join('graphic', attachment.filename))
            return True
        return False

    @staticmethod
    async def __sync_with_git(message):
        if not message.content.startswith('!sync'):
            return False
        os.system('git pull')
        os.execv(sys.argv[0], sys.argv)
        return True


client = MyClient()
client.run(TOKEN)
