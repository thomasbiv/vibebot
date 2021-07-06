import discord
from discord.ext.commands import bot
from discord.ext import commands
from discord import FFmpegPCMAudio
from asyncio import sleep
import urllib.parse, urllib.request, re
import random
import youtube_dl
import json
import os
import queue

client = discord.Client()
bot = commands.Bot(command_prefix ='$')

queue = []
queue2 = []

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.online, activity = discord.Game("with Tommy's sanity"))
    print("We have logged in as {0.user}".format(bot))

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





def check_if_me(ctx):
    return ctx.message.author.id == 393845694349443073

@bot.command(name = "roll", help = " - Roll a die with the requested amount of sides.")
@commands.has_role('Vibe Master')
async def roll(ctx, number_of_sides:int):                                                                   #every command must include context (ctx) before signature / #type cast from string to int
    roll = str(random.randint(1, number_of_sides))                                                          #generate a random number in the specified range / #must type case back from int to string to display on discord
    await ctx.send("{} rolled a {}!".format(ctx.author, roll))                                              #await call and send message

@bot.command(name = "ping", help = " - Display the latency of Vibe Bot.")
@commands.has_role('Vibe Master')
async def ping(ctx):
    await ctx.send(f'Pong! :ping_pong: - {round(bot.latency * 1000)}ms')

@bot.command(name = '8ball', help = " - Ask a question to the Magic 8 Ball and recieve your fortune...")
@commands.has_role('Vibe Master')
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidedly so.', 
                 'Without a doubt.', 
                 'Yes, definitely.', 
                 'You may rely on it.', 
                 'As I see it, yes.', 
                 'Most likely.', 
                 'Outlook good.', 
                 'Yes.', 
                 'Signs point to yes.', 
                 'Reply hazy try again.', 
                 'Ask again later.', 
                 'Better not tell you now.', 
                 'Cannot predict now.', 
                 'Concentrate and ask again.', 
                 "Don't count on it.", 
                 'My reply is no.',
                 'My sources say no.', 
                 'Outlook not so good.', 
                 'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@bot.command(name = "devs", help = " - List the developers of Vibe Bot.")
@commands.has_role('Vibe Master')
async def devs(ctx):
    await ctx.send("DEVS: Thomas Bivins")

@bot.command(name = "purge", help = " - Purges (clears) the last specified amount of messages.")
@commands.has_role('Vibe Master')
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount = 5):
    await ctx.channel.purge(limit = amount)

@bot.command(name = "youtube", help = " - Search for a YouTube video!")
@commands.has_role('Vibe Master')
async def youtube(ctx, *, search):
    query_string = urllib.parse.urlencode({
        'search_query': search
    })
    htm_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string
    )
    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
    await ctx.send('http://www.youtube.com/watch?v=' + search_results[0]) #Return first search result


#@bot.command(name = "join", help = " - Have Vibe Bot join your voice channel")
@bot.command(pass_context = True, name = "join", help = " - Have Vibe Bot join your voice channel (RESTRICTED)." )
@commands.check(check_if_me)
async def join(ctx):
    connected = ctx.author.voice
    if connected:
        channel = ctx.message.author.voice.channel
        await channel.connect()       
        await ctx.send("I have joined the voice channel.")
    else:
        await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")

#@bot.command(name = "leave", help = " - Have Vibe Bot leave your voice channel")
@bot.command(pass_context = True, name = "leave", help = " - Have Vibe Bot leave your voice channel (RESTRICTED)." )
@commands.check(check_if_me)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I have left the voice channel.")
    else:
        await ctx.send("I am not in a voice channel.")
        

@bot.command(name = "playlink", help = " - Play audio off of YouTube using a link.")
@commands.has_role('Vibe Master')
async def playlink(ctx, url:str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Please wait for the current song/video to end or use the '$stop' command before playing a new selection.")

    if (ctx.author.voice):
        #connect to voice channel
        if not (ctx.voice_client):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
        else:
            voice = ctx.guild.voice_client
     
        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        }

        #download youtube video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")

        #play youtube video
        source = FFmpegPCMAudio('song.mp3')
        player = voice.play(source)
        await ctx.send('Now Playing! :notes: ' + url) #Return first search result 
        while voice.is_playing() or voice.is_paused():
            await sleep(1)
        await voice.disconnect()

    else:
        await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")


@bot.command(pass_context = True, name = "pause", help = " - Pause the current song/video being played in a voice channel.")
@commands.has_role('Vibe Master')
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("Song/video paused.")
    else:
        await ctx.send("I am not playing any music to pause!")

@bot.command(pass_context = True, name = "resume", help = " - Resume the current song/video that is paused in the voice channel.")
@commands.has_role('Vibe Master')
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("Song/video resumed.")
    else:
        await ctx.send("There is currently no song/video that is paused.")



@bot.command(pass_context = True, name = "skipq", help = " - Stop the current song/video and play the next song in the queue (RESTRICTED).")
@commands.check(check_if_me)
async def skipq(ctx):
    voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
    voice.stop()
    await ctx.send("Song/video skipped.")
    #await ctx.guild.voice_client.disconnect()
    #await ctx.send("I have left the voice channel.")
    

@bot.command(pass_context = True, name = "stop", help = " - Stop the current song/video.")
@commands.has_role('Vibe Master')
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
    voice.stop()
    await ctx.send("Song/video stopped.")
    await ctx.guild.voice_client.disconnect()
    await ctx.send("I have left the voice channel.")


@bot.command(name = "play", help = " - Play audio off of YouTube using keywords.")
@commands.has_role('Vibe Master')
async def play(ctx, *, search):
    query_string = urllib.parse.urlencode({
        'search_query': search
    })
    htm_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string
    )
    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
    #await ctx.send('Now Playing! :notes: http://www.youtube.com/watch?v=' + search_results[0]) #Return first search result
    link = 'http://www.youtube.com/watch?v=' + search_results[0]
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Please wait for the current song to end or use the '$stop' command before playing a new song.")

    if (ctx.author.voice):
        #connect to voice channel
        if not (ctx.voice_client):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
        else:
            voice = ctx.guild.voice_client
     
        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        }

        #download youtube video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")

        #play youtube video
        source = FFmpegPCMAudio('song.mp3')
        player = voice.play(source)
        await ctx.send('Now Playing! :notes: http://www.youtube.com/watch?v=' + search_results[0]) #Return first search result 

        while voice.is_playing() or voice.is_paused():
            await sleep(1)
        await voice.disconnect()

    else:
        await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")

@bot.command(name = "enq", help = " - Add audio from YouTube to the queue (RESTRICTED).")
@commands.check(check_if_me)
async def enq(ctx, *, search):

    query_string = urllib.parse.urlencode({
        'search_query': search
    })
    htm_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string
    )
    #await ctx.send("Test")
    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
    link = 'http://www.youtube.com/watch?v=' + search_results[0]
    #await ctx.send("Test")
    queue.append(link)
    queue2.append(search)
    await ctx.send("Selection added to queue!")

@bot.command(name = "delq", help = " - Delete the specified selection in the queue (RESTRICTED).")
@commands.check(check_if_me)
async def delq(ctx, number):

    try:
        del(queue[int(number)])
        del(queue2[int(number)])
        await ctx.send(f'Your queue is now `{queue2}!`')
    except:
        await ctx.send("The queue is either empty or the specified selection is out of range.")
        await ctx.send("Current queue size: " + queue.qsize())

@bot.command(name = "playq", help = " - Play audio from the queue (RESTRICTED).")
@commands.check(check_if_me)
async def playq(ctx):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Please wait for the current song/video to end or use the '$stop' command before playing a new selection.")

    if (ctx.author.voice):
        #connect to voice channel
        if not (ctx.voice_client):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
        else:
            voice = ctx.guild.voice_client
     
        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        }

        #download youtube video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([queue[0]])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")

        #play youtube video
        source = FFmpegPCMAudio('song.mp3')
        player = voice.play(source)
        await ctx.send('Now Playing! :notes: ' + queue[0]) #Return first search result 
        while voice.is_playing() or voice.is_paused():
            await sleep(1)
        del(queue[int(0)])
        del(queue2[int(0)])
        #await voice.disconnect()
        if len(queue) < 1:
            await voice.disconnect()
        else:
            #await ctx.invoke(self.bot.get_command('playq'), query = ctx)
            temp = bot.get_command(name = 'playq')
            await temp.callback(ctx)
    else:
        await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")
    
@bot.command(name = "viewq", help = " - View the current selections in the queue (RESTRICTED).")
@commands.check(check_if_me)
async def viewq(ctx):
    try:
        await ctx.send(f'Your queue is now `{queue2}!`')
    except:
        await ctx.send("You have no queue initialized, so your queue is empty!")

@bot.command(name = "clearq", help = " - Stop the current song/video being played and clears the queue (RESTRICTED).")
@commands.check(check_if_me)
async def clearq(ctx):
    queue.clear()
    queue2.clear()
    await ctx.send("Queue cleared.")
    
    voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
    voice.stop()
    await ctx.send("Song/video stopped.")
    await ctx.guild.voice_client.disconnect()
    await ctx.send("I have left the voice channel.")
