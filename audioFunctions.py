import discord
from discord.ext.commands import bot
from discord.ext import commands
from discord import FFmpegPCMAudio
from asyncio import sleep
import urllib.parse, urllib.request, re
import youtube_dl
import random
import json
import os
import queue
import copy

class audioFunctions(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

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
    @bot.command(pass_context = True, name = "join", help = " - Have Vibe Bot join your voice channel (TESTING)." )
    @commands.is_owner()
    async def join(ctx):
        connected = ctx.author.voice
        if connected:
            channel = ctx.message.author.voice.channel
            await channel.connect()       
            await ctx.send("I have joined the voice channel.")
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")

    #@bot.command(name = "leave", help = " - Have Vibe Bot leave your voice channel")
    @bot.command(pass_context = True, name = "leave", help = " - Have Vibe Bot leave your voice channel (TESTING)." )
    @commands.is_owner()
    async def leave(ctx):
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.send("I have left the voice channel.")
        else:
            await ctx.send("I am not in a voice channel.")
            


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
        

    @bot.command(pass_context = True, name = "skipq", help = " - Stop the current song/video and play the next song in the queue. ")
    @commands.has_role('Vibe Master')
    async def skipq(ctx):
        voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
        voice.stop()
        await ctx.send("Song/video skipped.")
        if len(queue2) == 0:
            await ctx.guild.voice_client.disconnect()
            await ctx.send("I have left the voice channel.")



    @bot.command(name = "enq", help = " - Add audio from YouTube to the queue.")
    @commands.has_role('Vibe Master')
    async def enq(ctx, *, search):

        query_string = urllib.parse.urlencode({
            'search_query': search
        })
        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string
        )
        search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
        link = 'http://www.youtube.com/watch?v=' + search_results[0]

        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link)

        queue2.append(info['title'])
        await ctx.send("Selection added to queue!")

    @bot.command(name = "delq", help = " - Delete the specified selection in the queue.")
    @commands.has_role('Vibe Master')
    async def delq(ctx, number):

        try:
            del(queue2[int(number)])
            await ctx.send(f'Your queue is now `{queue2}!`')
        except:
            await ctx.send("The queue is either empty or the specified selection is out of range.")

        
    @bot.command(name = "viewq", help = " - View the current selections in the queue.")
    @commands.has_role('Vibe Master')
    async def viewq(ctx):
        try:
            await ctx.send(f'Your queue is now `{queue2}!`')
        except:
            await ctx.send("You have no queue initialized, so your queue is empty!")

    @bot.command(name = "clear", help = " - Stop the current song/video being played and clears the queue.")
    @commands.has_role('Vibe Master')
    async def clear(ctx):
        #queue.clear()
        queue2.clear()
        await ctx.send("Queue cleared.")
        
        voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
        voice.stop()
        await ctx.send("Song/video stopped.")
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I have left the voice channel.")

    @bot.command(name = "playlink", help = " - Play audio off of YouTube using a link. Also adds to queue.")
    @commands.has_role('Vibe Master')
    async def playlink(ctx, url:str):
        if (ctx.author.voice):
            if not (ctx.voice_client):
                channel = ctx.message.author.voice.channel
                voice = await channel.connect()
                ydl_opts = {
                    'quiet': True,
                    'skip_download': True,
                    }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url)

                queue2.append(info['title'])
                await ctx.send('Selection added to queue!')
                temp = bot.get_command(name = 'playq')
                await temp.callback(ctx)
                
            else:
                #ctx.voice_client.stop()
                voice = ctx.guild.voice_client
                if voice.is_playing() or voice.is_paused():
                    ydl_opts = {
                        'quiet': True,
                        'skip_download': True,
                        }
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url)

                    queue2.append(info['title'])
                    await ctx.send('Selection added to queue!')
                else:
                    ydl_opts = {
                        'quiet': True,
                        'skip_download': True,
                        }
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url)

                    queue2.append(info['title'])
                    await ctx.send('Selection added to queue!')
                    temp = bot.get_command(name = 'playq')
                    await temp.callback(ctx)
            
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")

    @bot.command(name = "play", help = " - Play audio off of YouTube using keywords. Also adds to queue.")
    @commands.has_role('Vibe Master')
    async def play(ctx, *, search):
        query_string = urllib.parse.urlencode({
            'search_query': search
        })
        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string
        )
        search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
        url = 'http://www.youtube.com/watch?v=' + search_results[0]
        if (ctx.author.voice):
            if not (ctx.voice_client):
                channel = ctx.message.author.voice.channel
                voice = await channel.connect()
                ydl_opts = {
                    'quiet': True,
                    'skip_download': True,
                    }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url)
                
                queue2.append(info['title'])
                await ctx.send('Selection added to queue!')
                temp = bot.get_command(name = 'playq')
                await temp.callback(ctx)
            else:
                #ctx.voice_client.stop()
                voice = ctx.guild.voice_client
                if voice.is_playing() or voice.is_paused():
                    ydl_opts = {
                        'quiet': True,
                        'skip_download': True,
                        }
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url)
                
                    queue2.append(info['title'])
                    await ctx.send('Selection added to queue!')
                else:
                    ydl_opts = {
                        'quiet': True,
                        'skip_download': True,
                        }
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url)
                
                    queue2.append(info['title'])
                    await ctx.send('Selection added to queue!')
                    temp = bot.get_command(name = 'playq')
                    await temp.callback(ctx)
            
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")
            

    @bot.command(name = "playq", help = " - Play the current queue.")
    @commands.has_role('Vibe Master')
    async def playq(ctx):
        if (ctx.author.voice):
            if not (ctx.voice_client):
                channel = ctx.message.author.voice.channel
                voice = await channel.connect()
            else:
                #ctx.voice_client.stop()
                voice = ctx.guild.voice_client

            query_string = urllib.parse.urlencode({
                'search_query': queue2[0]
            })
            htm_content = urllib.request.urlopen(
                'http://www.youtube.com/results?' + query_string
            )
            search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
            link = 'http://www.youtube.com/watch?v=' + search_results[0]


            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            YDL_OPTIONS = {'format': "bestaudio"}

            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(link, download=False)
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                voice.play(source)
            await ctx.send('Now Playing! :notes: ' + link)
            while voice.is_playing() or voice.is_paused():
                await sleep(1)
            global SHUFFLE_COND 
            if SHUFFLE_COND  == 1:
                SHUFFLE_COND = 0
            else:
                del(queue2[int(0)])
            if len(queue2) != 0:
                temp = bot.get_command(name = 'playq')
                await temp.callback(ctx)
            else:
                await voice.disconnect()
                await ctx.send("I have left the voice channel.")
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")


    @bot.command(name = "shuffleq", help = " - Shuffle the current queue.")
    @commands.has_role('Vibe Master')
    async def shuffleq(ctx):
        global SHUFFLE_COND
        SHUFFLE_COND  = 1
        tempq = []
        tempq.extend(queue2)
        random.shuffle(tempq)
        queue2.clear()
        queue2.extend(tempq)
        del tempq
        
        voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
        voice.stop()
        await ctx.send("Queue shuffled.")
        await ctx.send(f'Your queue is now `{queue2}!`')
        temp = bot.get_command(name = 'playq')
        await temp.callback(ctx)

def setup(bot):
    bot.add_cog(audioFunctions(bot))