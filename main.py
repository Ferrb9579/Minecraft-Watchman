import discord
from python_aternos import Client
import datetime
import os

client = discord.Client(intents=discord.Intents.all())
atclient = Client()
atclient.login('WINTERHOAX', 'Fanisus@09112005')
aternos = atclient.account


class SetupMessageButtons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Start", style=discord.ButtonStyle.green)
    async def green_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        servers = aternos.list_servers()
        myserver = servers[0]
        myserver.start()
        await interaction.response.send_message("Starting server", ephemeral=True)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def red_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        servers = aternos.list_servers()
        myserver = servers[0]
        myserver.stop()
        await interaction.response.send_message("Stopping server", ephemeral=True)


def getColor(status):
    if status == "online":
        return 0x1FD78D
    if status == "offline":
        return 0xF62451
    if status == "starting":
        return 0xE59831
    if status == "stopping":
        return 0xA4A4A4


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


def printAttributes(my_object):
    attributes = vars(my_object)
    for attribute, value in attributes.items():
        print(attribute, "=", value)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$start'):
        servers = aternos.list_servers()
        myserver = servers[0]
        myserver.start()
        await message.channel.send('Starting server')
    if message.content.startswith('$stop'):
        servers = aternos.list_servers()
        myserver = servers[0]
        myserver.stop()
        await message.channel.send('Stopping server')
    if message.content.startswith('$status'):
        servers = aternos.list_servers()
        myserver = servers[0]
        myserver.fetch()
        await message.channel.send(myserver.status)
    if message.content.startswith('$setup'):
        # if (message.author.id != 710847002342064188 and message.author.id != 789483148526092348):
        #     await message.channel.send("You are not allowed to do that")
        #     return
        for server in aternos.list_servers():
            server.fetch()
            serverEmbed = discord.Embed(color=getColor(server.status))
            serverEmbed.add_field(name="Server Name",
                                  value=server.domain.split(".")[0], inline=False)
            serverEmbed.add_field(
                name="Server IP", value=server.address, inline=False)
            serverEmbed.add_field(name="Server Port",
                                  value=server.port, inline=False)
            serverEmbed.add_field(name="Server Status",
                                  value=server.status, inline=False)
            serverEmbed.add_field(name="Online Players",
                                  value=str(server.players_count) + "/" + str(server.slots), inline=False)
            serverEmbed.add_field(name="Server Version",
                                  value=server.software + " " + server.version, inline=False)
            serverEmbed.add_field(
                name="Server Stop Countdown", value=str(datetime.timedelta(seconds=server.countdown + 1)), inline=False)
            embedMessage = await message.channel.send(embed=serverEmbed, view=SetupMessageButtons())

client.run(os.environ['TOKEN'])
