import abc
import discord
from datetime import datetime
from discord.ext import commands
from discord import activity
from discord.ext.commands.core import has_permissions
from dataIO import fileIO

# check for settings file, create if missing
def check_settings():
    if not fileIO("settings.json", "check"):
        content = {
            "TOKEN" : None}
        print("settings.json missing, creating...")
        fileIO("settings.json", "save", content)

# load settings file
check_settings()
settings = fileIO("settings.json" , "load")
token = settings["TOKEN"]

# hardcoded values (needed mainly for cogs)
presence = "v1.0 | @ me"

# check for missing variables
if token == None:
    token = str(input("Please paste in your bot's token and hit enter. \n"))
    settings["TOKEN"] = token
    fileIO("settings.json" , "save", settings)

# finishing touches
bot = commands.Bot(command_prefix=commands.when_mentioned_or("em!"), help_command=None)

def timestamp():
    dt = datetime.now()
    ts = dt.strftime("%H:%M:%S")
    return ts

# startup
@bot.event
async def on_ready():
    user = str(bot.user)
    guilds = len(bot.guilds)
    print(" ")
    print("{}    ###    Bot online!".format(timestamp()))
    print("{}    ###    Bot username: {}".format(timestamp(), user))
    print("{}    ###    Default prefix: {}".format(timestamp(), "em!"))
    print("{}    ###    Currently in {} guilds".format(timestamp(), guilds))
    print(" ")
    # streaming status requires a twitch URL so we're redirecting the "Watch Stream" button to twitch's directory page
    await bot.change_presence(status=discord.Status.online, activity=discord.Streaming(name=presence, url="https://www.twitch.tv/directory", twitch_name="directory"))

# commands
@bot.command(aliases = ['run'])
@commands.has_permissions(manage_messages=True)
@commands.guild_only()
async def genmessage(ctx):
    """Generates the emote list message and sends it in the current channel"""
    emotes = []
    counter = 0
    # search all emojis in the guild and append to emotes list
    for x in ctx.guild.emojis:
        # formatting as follows: emote `:emote name: \n`
        data = "{} `{}`".format(str(x), x.name)
        emotes.append(data)
        counter += 1
    # put all emotes into string format and 
    msg = "\n".join(emotes)
    left = ctx.guild.emoji_limit - counter
    await ctx.message.delete()
    # check for previous messages and delete previously generated lists
    async for message in ctx.channel.history(limit=500): # limiting to 500 for better performance
        if message.author.id == bot.user.id: # checking IDs should be faster
            await message.delete()
    await ctx.send("{}\n\n{}/{} emotes used ({} left)".format(msg, counter, ctx.guild.emoji_limit, left))

bot.run(token)