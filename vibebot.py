import discord
from discord.ext.commands import bot
from discord.ext import commands
from discord.ext.commands.help import HelpCommand
from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
bot = commands.Bot(command_prefix='$')
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("with Tommy's sanity"))
    print("We have logged in as {0.user}".format(bot))
    bot.load_extension('usefulFunctions')
    bot.load_extension('audioFunctions')

@bot.event
async def on_message(message):
    if message.author == client.user:
        return

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

@bot.group(invoke_without_command = True)
async def help(ctx):
    embed = discord.Embed(title = "***Help***", description = "For more information on a specific command, type $help <command>", color = 0xa09c9c)
    embed.add_field(name = "Useful Functions", value = "roll | ping | eightball | purge | poll", inline=False)
    embed.add_field(name = "Audio Functions", value = "youtube | join | leave | pause | resume | skipq | enq | delq | viewq | clear | play | playq | shuffleq | replay | playlist | currsong | moveto | repeat | repeatnum | lyrics | swapq", inline=False)
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def roll(ctx):
    embed = discord.Embed(title = "***roll***", description = "Roll a die with the requested amount of sides.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$roll <amount>")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def ping(ctx):
    embed = discord.Embed(title = "***ping***", description = "Display the latency of Vibe Bot.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$ping")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def eightball(ctx):
    embed = discord.Embed(title = "***eightball***", description = "Ask a question to the Magic 8 Ball and recieve your fortune...", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$eightball <question>")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def purge(ctx):
    embed = discord.Embed(title = "***purge***", description = "Purges (clears) the last specified amount of messages (Default = 5).", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$purge <amount>")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def poll(ctx):
    embed = discord.Embed(title = "***poll***", description = "Create a new poll.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$poll <topic>")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def youtube(ctx):
    embed = discord.Embed(title = "***youtube***", description = "Search for a YouTube video!", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$youtube <query>")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def join(ctx):
    embed = discord.Embed(title = "***join***", description = "Have Vibe Bot join your voice channel.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$join")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def leave(ctx):
    embed = discord.Embed(title = "***leave***", description = "Have Vibe Bot leave your voice channel.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$leave")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def pause(ctx):
    embed = discord.Embed(title = "***pause***", description = "Pause the current selection being played in a voice channel.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$pause")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def resume(ctx):
    embed = discord.Embed(title = "***resume***", description = "Resume the current selection that is paused in a voice channel.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$resume")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def skipq(ctx):
    embed = discord.Embed(title = "***skipq***", description = "Skip the specified amount of selections in the queue (Default = 1).", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$skipq <amount>")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def enq(ctx):
    embed = discord.Embed(title = "***enq***", description = "Add audio from YouTube to the queue.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$enq <query or link>")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def delq(ctx):
    embed = discord.Embed(title = "***delq***", description = "Delete the specified selection in the queue.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$delq <number>")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def viewq(ctx):
    embed = discord.Embed(title = "***viewq***", description = "View the current selections in the queue (Default page number = 1).", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$viewq <queue page number>")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def clear(ctx):
    embed = discord.Embed(title = "***clear***", description = "Stop the current selection being played and clears the queue.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$clear")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def play(ctx):
    embed = discord.Embed(title = "***play***", description = "Play audio off of YouTube using keywords or url. Also adds to queue.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$play <query or link>")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def playq(ctx):
    embed = discord.Embed(title = "***playq***", description = "Play the current queue.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$playq")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def shuffleq(ctx):
    embed = discord.Embed(title = "***shuffleq***", description = "Shuffle the current queue.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$shuffleq")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def replay(ctx):
    embed = discord.Embed(title = "***replay***", description = "Restart the current selection from the beginning.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$replay")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def playlist(ctx):
    embed = discord.Embed(title = "***playlist***", description = "Play a playlist off of YouTube using a playlist url. Adds to queue.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$playlist <youtube playlist link>")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def currsong(ctx):
    embed = discord.Embed(title = "***currsong***", description = "View the name of the current selection.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$currsong")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def moveto(ctx):
    embed = discord.Embed(title = "***moveto***", description = "Move a selection to a different spot in the queue.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$moveto <index of selection to move> <index to move selection to>")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def repeat(ctx):
    embed = discord.Embed(title = "***repeat***", description = "Repeat the current selection a given amount of times (DEFAULT/MAX = 20).", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$repeat <num of repeats>")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def repeatnum(ctx):
    embed = discord.Embed(title = "***repeatnum***", description = "View the remaining repetitions left on a selection.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$repeatnum")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def lyrics(ctx):
    embed = discord.Embed(title = "***lyrics***", description = "Get the lyrics of a specified selection in the queue (DEFAULT = 0).", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$lyrics <queue location>")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

@help.command()
async def swapq(ctx):
    embed = discord.Embed(title = "***swapq***", description = "Switch two selections in the queue.", color = 0xa09c9c)
    embed.add_field(name = "Syntax", value = "$swapq <index of first selection> <index of second selection>")
    embed.set_footer(text = "Vibe Bot")
    await ctx.send(embed = embed)

bot.run(TOKEN)
