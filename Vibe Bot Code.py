import discord
from discord.ext.commands import bot
from discord.ext import commands

client = discord.Client()
bot = commands.Bot(command_prefix ='$')

queue2 = []
SHUFFLE_COND = 0

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.online, activity = discord.Game("with Tommy's sanity"))
    print("We have logged in as {0.user}".format(bot))
    client.load_extension('usefulFunctions')
    client.load_extension('audioFunctions')

@bot.event
async def on_message(message):
    if message.author == client.user:
        return
    '''
    if message.content.startswith("ping"):
        await message.channel.send(f'Pong! - {round(bot.latency * 1000)}ms')                                                                 #await keyword makes sure all other actions are completed before taking this action
    '''
    #if message.author.id == 393845694349443073:
    if message.content.startswith("$"):
        await message.add_reaction("🤠")
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server!')

@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server. :(')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Error: Missing required arguments for this command.')
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Error: Unknown command. Maybe you fatfingered it.\nFor a list of commands, type '$help'.")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Error: You do not have permission to use this command.')
    if isinstance(error, commands.MissingRole):
        await ctx.send('Error: You do not have the required role to use this command.')
