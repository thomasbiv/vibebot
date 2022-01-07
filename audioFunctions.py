from asyncio.events import AbstractEventLoopPolicy
import discord
from discord import colour
from discord.ext.commands import bot
from discord.ext import commands
from discord import FFmpegPCMAudio
from asyncio import sleep
import urllib.parse
import urllib.request
import re
import youtube_dl
import random
import json
import os
import queue
import copy
import typing as t
import aiohttp
multiServerQueue = {}
SHUFFLE_COND = 0
REPEAT_NUM = 0

LYRICS_URL = "https://some-random-api.ml/lyrics?title="

class NoLyricsFound(commands.CommandError):
    pass

class audioFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot










    @commands.command(name="youtube", help=" - Search for a YouTube video!")
    @commands.has_role('Vibe Master')
    async def youtube(self, ctx, *, search):
        query_string = urllib.parse.urlencode({
            'search_query': search
        })
        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string
        )
        search_results = re.findall(
            r"watch\?v=(\S{11})", htm_content.read().decode())
        link = 'http://www.youtube.com/watch?v=' + search_results[0]
        await ctx.send(link)










    @commands.command(name="join", help=" - Have Vibe Bot join your voice channel.")
    @commands.has_role('Vibe Master')
    async def join(self, ctx):
        connected = ctx.author.voice
        if connected:
            try:
                await connected.channel.connect()
                await ctx.send("I have joined the voice channel.")
            except Exception as error:
                await ctx.send(error)
            if not (ctx.guild.voice_client.is_playing() or ctx.guild.voice_client.is_paused()):
                # Vibe Bot idles for 5 minutes when no music is played
                await sleep(300)
                # Vibe Bot performs a second audio and voice check, just in case $leave was used while in sleep mode
                if not (ctx.guild.voice_client.is_playing() or ctx.guild.voice_client.is_paused()):
                    if ctx.voice_client:
                        await ctx.send("I have left the voice channel due to voice inactivity.")
                        # After idling for 5 minutes, Vibe Bot will automatically leave the VC due to inactivity
                        await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")










    @commands.command(pass_context=True, name="leave", help=" - Have Vibe Bot leave your voice channel.")
    @commands.has_role('Vibe Master')
    async def leave(self, ctx):
        if (ctx.author.voice):
            if (ctx.voice_client):
                await ctx.guild.voice_client.disconnect()
                await ctx.send("I have left the voice channel.")
            else:
                await ctx.send("I am not in a voice channel.")
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")










    @commands.command(pass_context=True, name="pause", help=" - Pause the current selection being played in a voice channel.")
    @commands.has_role('Vibe Master')
    async def pause(self, ctx):
        if (ctx.author.voice):
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            if voice.is_playing():
                voice.pause()
                await ctx.send("***Selection paused.*** :pause_button:")
                await sleep(300)  # Vibe Bot idles for 5 minutes when paused
                # If bot is still connected and paused after sleep
                if ctx.voice_client and ctx.guild.voice_client.is_paused():
                    voice.resume()
                    await ctx.send("Automatically resumed.")
            else:
                await ctx.send("I am not playing any music to pause!")
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")










    @commands.command(pass_context=True, name="resume", help=" - Resume the current selection that is paused in the voice channel.")
    @commands.has_role('Vibe Master')
    async def resume(self, ctx):
        if (ctx.author.voice):
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            if voice.is_paused():
                voice.resume()
                await ctx.send("***Selection resumed.*** :play_pause:")
            else:
                await ctx.send("There is currently no selection that is paused.")
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")










    @commands.command(pass_context=True, name="skipq", help=" - Skip the specified amount of selections in the queue.")
    @commands.has_role('Vibe Master')
    async def skipq(self, ctx, amt=0):
        if (ctx.author.voice):
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            global REPEAT_NUM
            global SHUFFLE_COND
            SHUFFLE_COND = 0
            REPEAT_NUM = 0
            if (amt > 0):
                if (amt > len(multiServerQueue[ctx.guild.id])):
                    await ctx.send("Amount requested exceeds range of queue. Skipping current selection.")
                else:
                    for i in range(amt - 1):
                        del(multiServerQueue[ctx.guild.id][int(0)])

            voice.stop()
            await ctx.send("***Selection(s) skipped.*** :thumbsup:")
            if len(multiServerQueue[ctx.guild.id]) == 0:
                await ctx.guild.voice_client.disconnect()
                await ctx.send("I have left the voice channel.")
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")










    @commands.command(name="enq", help=" - Add audio from YouTube to the queue.")
    @commands.has_role('Vibe Master')
    async def enq(self, ctx, *, search):
        if (ctx.author.voice):
            if ctx.guild.id not in multiServerQueue:
                multiServerQueue[ctx.guild.id] = []
            query_string = urllib.parse.urlencode({
                'search_query': search
            })
            htm_content = urllib.request.urlopen(
                'http://www.youtube.com/results?' + query_string
            )
            search_results = re.findall(
                r"watch\?v=(\S{11})", htm_content.read().decode())
            link = 'http://www.youtube.com/watch?v=' + search_results[0]

            ydl_opts = {
                'quiet': True,
                'skip_download': True,
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link)

            multiServerQueue[ctx.guild.id].append(
                {'url': info['formats'][0]['url'], 'title': info['title'], 'from_playlist': False})
            await ctx.send("***Selection added to queue!*** :ok_hand:")
            await ctx.send('***The queue now contains ' + str(len(multiServerQueue[ctx.guild.id])) + ' selection(s)!***')
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")










    @commands.command(name="delq", help=" - Delete the specified selection in the queue.")
    @commands.has_role('Vibe Master')
    async def delq(self, ctx, number):
        if (ctx.author.voice):
            if ctx.guild.id not in multiServerQueue:
                return await ctx.send('No queue.')
            try:
                if (int(number) == 0):
                    temp = self.bot.get_command(name='skipq')
                    return await temp.callback(self, ctx, amt=0)
                del(multiServerQueue[ctx.guild.id][int(number)])
                await ctx.send("***Selection deleted from queue!*** :x:")
            except:
                await ctx.send("The specified selection is out of range.")
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")










    @commands.command(name="viewq", help=" - View the current selections in the queue.")
    @commands.has_role('Vibe Master')
    async def viewq(self, ctx, page_num=1):
        embed = discord.Embed(color=0xa09c9c)
        if ctx.guild.id not in multiServerQueue:
            embed.title = "***No queue.***"
            return await ctx.send(embed=embed)
        real_num = page_num - 1
        queue_pages = []
        page = []
        k = 1
        for i in range(len(multiServerQueue[ctx.guild.id])):
            page.append(multiServerQueue[ctx.guild.id][i])
            if k % 10 == 0:
                temp = page.copy()
                queue_pages.append(temp)
                page.clear()
            elif (k == len(multiServerQueue[ctx.guild.id])) and (k % 10 != 0):
                queue_pages.append(page)
            k = k + 1

        if (page_num > len(queue_pages)) or (page_num <= 0):
            return await ctx.send("Invalid page number. There are currently " + str(len(queue_pages)) + " page(s) in the queue.")

        embed.title = ":notes: ***Current queue:***"
        key = page_num - 1
        for j in range(len(queue_pages[real_num])):
            if page_num == 1:
                if j == 0:
                    embed.add_field(name="NP:", value=queue_pages[real_num][j].get('title', None), inline=False)
                else:
                    embed.add_field(name=str(j) + ". ", value=queue_pages[real_num][j].get('title', None), inline=False)
            else:
                embed.add_field(name=str(key) + str(j) + ". ", value=queue_pages[real_num][j].get('title', None), inline=False)

        embed.set_footer(text="Page " + str(page_num) +"/" + str(len(queue_pages)))
        await ctx.send(embed=embed)










    @commands.command(name="clear", help=" - Stop the current selection being played and clears the queue.")
    @commands.has_role('Vibe Master')
    async def clear(self, ctx):
        if (ctx.author.voice):
            if ctx.guild.id not in multiServerQueue:
                return await ctx.send('No queue.')
            global REPEAT_NUM
            global SHUFFLE_COND
            SHUFFLE_COND = 0
            REPEAT_NUM = 0
            multiServerQueue.pop(ctx.guild.id, None)
            await ctx.send("***Queue cleared.***")
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            voice.stop()
            await ctx.send("Selection stopped.")
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")










    @commands.command(name="play", help=" - Play audio off of YouTube using keywords or url. Also adds to queue.")
    @commands.has_role('Vibe Master')
    async def play(self, ctx, *, search):
        query_string = urllib.parse.urlencode({
            'search_query': search
        })
        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string
        )
        search_results = re.findall(
            r"watch\?v=(\S{11})", htm_content.read().decode())
        url = 'http://www.youtube.com/watch?v=' + search_results[0]
        if (ctx.author.voice):
            if ctx.guild.id not in multiServerQueue:
                multiServerQueue[ctx.guild.id] = []
            if not (ctx.voice_client):
                channel = ctx.message.author.voice.channel
                voice = await channel.connect()
            else:
                voice = ctx.guild.voice_client
            ydl_opts = {
                'quiet': True,
                'skip_download': True,
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url)

            multiServerQueue[ctx.guild.id].append(
                {'url': info['formats'][0]['url'], 'title': info['title'], 'from_playlist': False})
            await ctx.send('***Selection added to queue!*** :ok_hand:')
            await ctx.send('***The queue now contains ' + str(len(multiServerQueue[ctx.guild.id])) + ' selection(s)!***')
            if not (voice.is_playing() or voice.is_paused()):
                temp = self.bot.get_command(name='playq')
                await temp.callback(self, ctx)

        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")










    @commands.command(name="playlist", help=" - Play a playlist off of YouTube using a playlist url. Adds to queue.")
    @commands.has_role('Vibe Master')
    async def playlist(self, ctx, url: str):
        if (ctx.author.voice):
            if ctx.guild.id not in multiServerQueue:
                multiServerQueue[ctx.guild.id] = []

            ydl_opts = {
                'quiet': True,
                'skip_download': True,
                'dump_single_json': True,
                'extract_flat': True
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    await ctx.send('***Loading playlist...***')
                    for i in info['entries']:
                        try:
                            # newInfo = ydl.extract_info(i['url'], download=False) if playlist true do this in playq, else normal workflow
                            multiServerQueue[ctx.guild.id].append(
                                {   'url': i['url'],
                                    'title': i['title'],
                                    'from_playlist': True
                                })
                        except Exception as error:
                            print(error)

                    await ctx.send('***Playlist added to queue!*** :ok_hand:')
                    await ctx.send('***The queue now contains ' + str(len(multiServerQueue[ctx.guild.id])) + ' selection(s)!***')
                else:
                    if len(multiServerQueue[ctx.guild.id]) < 1:
                        temp = self.bot.get_command(name='clear')
                        await temp.callback(self, ctx)
                    return await ctx.send("Provided link is invalid.")

                if not (ctx.voice_client):
                    channel = ctx.message.author.voice.channel
                    voice = await channel.connect()
                else:
                    voice = ctx.guild.voice_client
                if not (voice.is_playing() or voice.is_paused()):
                    temp = self.bot.get_command(name='playq')
                    await temp.callback(self, ctx)

        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")
            










    @commands.command(name="playq", help=" - Play the current queue.")
    @commands.has_role('Vibe Master')
    async def playq(self, ctx):
        if (ctx.author.voice):
            if ctx.guild.id not in multiServerQueue:
                return await ctx.send("Nothing in the current queue.")
            if not (ctx.voice_client):
                channel = ctx.message.author.voice.channel
                voice = await channel.connect()
            else:
                voice = ctx.guild.voice_client

            FFMPEG_OPTIONS = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            YDL_OPTIONS = {'format': "bestaudio"}

            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                if multiServerQueue[ctx.guild.id][0]['from_playlist'] == True:
                    url2 = ydl.extract_info(multiServerQueue[ctx.guild.id][0]['url'], download=False)
                    url2 = url2['formats'][0]['url']
                else:
                    url2 = multiServerQueue[ctx.guild.id][0].get('url', None)
                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                voice.play(source)
            while voice.is_playing() or voice.is_paused():
                await sleep(1)
            global SHUFFLE_COND
            global REPEAT_NUM
            if REPEAT_NUM != 0:
                REPEAT_NUM = REPEAT_NUM - 1
            if SHUFFLE_COND == 1 and REPEAT_NUM == 0: #LAST SONG CASE / SHUFFLE CASE
                SHUFFLE_COND = 0
            elif SHUFFLE_COND == 1 and REPEAT_NUM != 0:
                SHUFFLE_COND = 1
            else:
                del(multiServerQueue[ctx.guild.id][int(0)])
            if len(multiServerQueue[ctx.guild.id]) != 0:
                temp = self.bot.get_command(name='playq')
                await temp.callback(self, ctx)
            else:
                multiServerQueue.pop(ctx.guild.id,None)
                await voice.disconnect()
                await ctx.send("I have left the voice channel.")
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")


            








    @commands.command(name="shuffleq", help=" - Shuffle the current queue.")
    @commands.has_role('Vibe Master')
    async def shuffleq(self, ctx):
        if (ctx.author.voice):
            if ctx.voice_client:
                if ctx.guild.id not in multiServerQueue:
                    return await ctx.send("Nothing in the current queue.")
                global SHUFFLE_COND
                global REPEAT_NUM
                SHUFFLE_COND = 1
                REPEAT_NUM = 0
                random.shuffle(multiServerQueue[ctx.guild.id])
                if not (ctx.voice_client):
                    channel = ctx.message.author.voice.channel
                    voice = await channel.connect()
                else:
                    voice = ctx.guild.voice_client
                if voice.is_playing() or voice.is_paused():
                    voice.stop()
                await ctx.send("***Queue shuffled.*** :twisted_rightwards_arrows:")
            else:
                await ctx.send("I am not connected to a voice channel.")
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")











    @commands.command(name="replay", help=" - Restart the current selection from the beginning.")
    @commands.has_role('Vibe Master')
    async def restart(self, ctx):
        if (ctx.author.voice):
            if ctx.voice_client:
                voice = ctx.guild.voice_client
                if voice.is_playing() or voice.is_paused():
                    global SHUFFLE_COND
                    SHUFFLE_COND = 1
                    voice.stop()
                    await ctx.send("***Selection restarted!*** :rewind:")
                else:
                    await ctx.send("I am not playing anything!")
            else:
                await ctx.send("I am not connected to a voice channel.")
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")

    
    
    






    @commands.command(name="currsong", help=" - View the name of the current selection.")
    @commands.has_role('Vibe Master')
    async def currsong(self, ctx):
        if (ctx.author.voice):
            if ctx.voice_client:
                voice = ctx.guild.voice_client
                if voice.is_playing() or voice.is_paused():
                    await ctx.send("***The current selection is '" + multiServerQueue[ctx.guild.id][0]['title'] + "'!***")
                else:
                    await ctx.send("I am not playing anything!")
            else:
                await ctx.send("I am not connected to a voice channel.")
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")

    









    @commands.command(name="moveto", help=" - Move a selection to a different spot in the queue.")
    @commands.has_role('Vibe Master')
    async def moveto(self, ctx, currSpot : int, toSpot : int):
        if (ctx.author.voice):
            if ctx.voice_client:
                voice = ctx.guild.voice_client
                if ctx.guild.id not in multiServerQueue:
                    await ctx.send("Nothing in the current queue.")
                else:
                    try:
                        if currSpot <= toSpot:
                            multiServerQueue[ctx.guild.id].insert(toSpot + 1, multiServerQueue[ctx.guild.id][currSpot])
                        else:
                            multiServerQueue[ctx.guild.id].insert(toSpot, multiServerQueue[ctx.guild.id][currSpot])

                        if currSpot > toSpot:
                            del(multiServerQueue[ctx.guild.id][currSpot + 1])
                        elif currSpot <= toSpot:
                            del(multiServerQueue[ctx.guild.id][currSpot])
                        
                        if currSpot == 0 or toSpot == 0:
                            global SHUFFLE_COND 
                            global REPEAT_NUM
                            SHUFFLE_COND = 1 
                            REPEAT_NUM = 0
                            voice.stop()
                        
                        await ctx.send("***Selection moved!*** :thumbsup:")
                    except:
                        await ctx.send("The specified indices are out of range.")
            else:
                await ctx.send("I am not connected to a voice channel.")
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")










    @commands.command(name="repeat", help=" - Repeat the current selection a given amount of times (DEFAULT/MAX = 20).")
    @commands.has_role('Vibe Master')
    async def repeat(self, ctx, num : int = 20):
        if (ctx.author.voice):
            if ctx.voice_client:
                voice = ctx.guild.voice_client
                if voice.is_playing() or voice.is_paused():
                    global REPEAT_NUM
                    global SHUFFLE_COND
                    if num > 20 or num < 1:
                        await ctx.send("Invalid repetition number. Number must be less than 20 and greater than 0.")
                    else:
                        REPEAT_NUM = num
                        SHUFFLE_COND = 1
                        await ctx.send("***The current selection will repeat '" + str(num) + "'  more time(s)!***")
                else:
                    await ctx.send("I am not playing anything!")
            else:
                await ctx.send("I am not connected to a voice channel.")
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")










    @commands.command(name="repeatnum", help=" - View the remaining repetitions left on a selection.")
    @commands.has_role('Vibe Master')
    async def repeatnum(self, ctx):
        if (ctx.author.voice):
            if ctx.voice_client:
                voice = ctx.guild.voice_client
                if voice.is_playing() or voice.is_paused():
                    if REPEAT_NUM != 0:
                        await ctx.send("***The current selection will repeat '" + str(REPEAT_NUM) + "' more time(s)!***")
                    else:
                        await ctx.send("This selection is not set to repeat.")
                else:
                    await ctx.send("I am not playing anything!")
            else:
                await ctx.send("I am not connected to a voice channel.")
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")

    












    @commands.command(name = "lyrics", help = " - Get the lyrics of a specified selection in the queue.")
    @commands.has_role('Vibe Master')
    async def lyrics(self, ctx, locale = 0):
        if (ctx.author.voice):
            if ctx.voice_client:
                voice = ctx.guild.voice_client
                if ctx.guild.id not in multiServerQueue:
                    return await ctx.send("No selections in queue.")
                else:
                    if locale > len(multiServerQueue[ctx.guild.id]) - 1 or locale < 0:
                        return await ctx.send("Specified index out of range.")
                    else:
                        name = multiServerQueue[ctx.guild.id][locale].get('title', None)
                        async with ctx.typing():
                            async with aiohttp.request("GET", LYRICS_URL + name, headers={}) as r:
                                if not 200 <= r.status <= 299:
                                    raise NoLyricsFound

                                data = await r.json()

                                #if len(data["lyrics"]) > 2000:
                                #    return await ctx.send(f"<{data['links']['genius']}>")

                                embed = discord.Embed(
                                    title = data["title"],
                                    description = data["lyrics"],
                                    colour=0xa09c9c,
                                )
                                
                                embed.set_thumbnail(url=data["thumbnail"]["genius"])
                                embed.set_author(name=data["author"])
                                embed.set_footer(text = "Vibe Bot")
                                await ctx.send(embed=embed)
            else:
                return await ctx.send("I am not connected to a voice channel.")
        else:
            return await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")

    


    @lyrics.error
    async def lyrics_error(self, ctx, exc):
        if isinstance(exc, NoLyricsFound):
            await ctx.send("No lyrics could be found.")









    
    @commands.command(name="swapq", help=" - Switch two selections in the queue.")
    @commands.has_role('Vibe Master')
    async def swapq(self, ctx, locOne : int, locTwo : int):
        if (ctx.author.voice):
            if ctx.voice_client:
                voice = ctx.guild.voice_client
                if ctx.guild.id not in multiServerQueue:
                    await ctx.send("Nothing in the current queue.")
                else:
                        if locOne > len(multiServerQueue[ctx.guild.id]) - 1 or locOne < 0 or locTwo > len(multiServerQueue[ctx.guild.id]) - 1 or locTwo < 0:
                            return await ctx.send("Specified indices out of range.")
                        else:
                            temp = multiServerQueue[ctx.guild.id][locOne]
                            multiServerQueue[ctx.guild.id][locOne] = multiServerQueue[ctx.guild.id][locTwo]
                            multiServerQueue[ctx.guild.id][locTwo] = temp
                            del(temp)

                            if locOne == 0 or locTwo == 0:
                                global SHUFFLE_COND 
                                global REPEAT_NUM
                                SHUFFLE_COND = 1 
                                REPEAT_NUM = 0
                                voice.stop()

                            await ctx.send("***Selections swapped!*** :thumbsup:")
            else:
                await ctx.send("I am not connected to a voice channel.")
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")

    

    

            


def setup(bot):
    bot.add_cog(audioFunctions(bot))
