import discord
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
multiServerQueue = {}
SHUFFLE_COND = 0

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
            except Exception as error:
                print(error)
            await ctx.send("I have joined the voice channel.")
            if not (ctx.guild.voice_client.is_playing() or ctx.guild.voice_client.is_paused()):
                await sleep(300) #Vibe Bot idles for 5 minutes when no music is played
                if not (ctx.guild.voice_client.is_playing() or ctx.guild.voice_client.is_paused()): #Vibe Bot performs a second audio and voice check, just in case $leave was used while in sleep mode
                    if ctx.voice_client:
                        await ctx.send("I have left the voice channel due to voice inactivity.")
                        await ctx.guild.voice_client.disconnect() #After idling for 5 minutes, Vibe Bot will automatically leave the VC due to inactivity
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
                await sleep(300) #Vibe Bot idles for 5 minutes when paused
                if ctx.voice_client and ctx.guild.voice_client.is_paused(): #If bot is still connected and paused after sleep
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
    async def skipq(self, ctx, amt = 0):
        if (ctx.author.voice):
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
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

            #multiServerQueue[ctx.guild.id].append(info)
            multiServerQueue[ctx.guild.id].append({'url':info['formats'][0]['url'],'title':info['title']})
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
    async def viewq(self,ctx, page_num = 1):
        embed = discord.Embed(color=0xa09c9c)
        if ctx.guild.id not in multiServerQueue:
            embed.title = "***No queue.***"
            return await ctx.send(embed = embed)
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
                    embed.add_field(name = "NP:" , value = queue_pages[real_num][j].get('title', None), inline = False)
                else:
                    embed.add_field(name = str(j) + ". ", value = queue_pages[real_num][j].get('title', None), inline = False)
            else:
                embed.add_field(name = str(key) + str(j) + ". ", value = queue_pages[real_num][j].get('title', None), inline = False)
            
        embed.set_footer(text = "Page " + str(page_num) + "/" + str(len(queue_pages)))
        await ctx.send(embed = embed)
        

                

    @commands.command(name="clear", help=" - Stop the current selection being played and clears the queue.")
    @commands.has_role('Vibe Master')
    async def clear(self, ctx):
        if (ctx.author.voice):
            if ctx.guild.id not in multiServerQueue:
                return await ctx.send('No queue.')
            multiServerQueue.pop(ctx.guild.id,None)
            await ctx.send("***Queue cleared.***")
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            voice.stop()
            await ctx.send("Selection stopped.")
            await ctx.guild.voice_client.disconnect()
            #await ctx.send("I have left the voice channel.")
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

            #multiServerQueue[ctx.guild.id].append(info)
            multiServerQueue[ctx.guild.id].append({'url':info['formats'][0]['url'],'title':info['title']})
            await ctx.send('***Selection added to queue!*** :ok_hand:')
            await ctx.send('***The queue now contains ' + str(len(multiServerQueue[ctx.guild.id])) + ' selection(s)!***')
            if not (voice.is_playing() or voice.is_paused()):
                temp = self.bot.get_command(name='playq')
                await temp.callback(self, ctx)
                
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command.")


    @commands.command(name="playlist", help=" - Play a playlist off of YouTube using a playlist url. Adds to queue.")
    @commands.has_role('Vibe Master')
    async def playlist(self, ctx, url:str):
        if (ctx.author.voice):
            if ctx.guild.id not in multiServerQueue:
                multiServerQueue[ctx.guild.id] = []
            
            ydl_opts = {
                'quiet': True,
                'skip_download': True,
            }
            await ctx.send('***Working on it, this might take a sec...***')
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url)
                if 'entries' in info:
                    await ctx.send('***Loading playlist...***')
                    for i in info['entries']:
                        newURL = i['formats'][0]['url']
                        newInfo = ydl.extract_info(newURL)
                        newInfo['title'] = i['title']
                        #multiServerQueue[ctx.guild.id].append(newInfo)
                        multiServerQueue[ctx.guild.id].append({'url':i['formats'][0]['url'],'title':i['title']})  #possible to cut down data 
                        
                    await ctx.send('***Playlist added to queue!*** :ok_hand:')
                else:
                    temp = self.bot.get_command(name='clear')
                    await temp.callback(self, ctx)
                    return await ctx.send("Provided link is invalid.")

            await ctx.send('***The queue now contains ' + str(len(multiServerQueue[ctx.guild.id])) + ' selection(s)!***')

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
                #url2 = multiServerQueue[ctx.guild.id][0]['formats'][0]['url']
                url2 = multiServerQueue[ctx.guild.id][0].get('url', None)
                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                voice.play(source)
            while voice.is_playing() or voice.is_paused():
                await sleep(1)
            global SHUFFLE_COND
            if SHUFFLE_COND == 1:
                SHUFFLE_COND = 0
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
                SHUFFLE_COND = 1
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

            


def setup(bot):
    bot.add_cog(audioFunctions(bot))
