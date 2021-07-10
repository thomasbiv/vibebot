import random
import discord
from discord.ext.commands import bot
from discord.ext import commands

class usefulFunctions(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    @commands.command(name = "roll", help = " - Roll a die with the requested amount of sides.")
    @commands.has_role('Vibe Master')
    async def roll(ctx, number_of_sides:int):                                                                   #every command must include context (ctx) before signature / #type cast from string to int
        roll = str(random.randint(1, number_of_sides))                                                          #generate a random number in the specified range / #must type case back from int to string to display on discord
        await ctx.send("{} rolled a {}!".format(ctx.author, roll))                                              #await call and send message

    @commands.command(name = "ping", help = " - Display the latency of Vibe Bot.")
    @commands.has_role('Vibe Master')
    async def ping(ctx):
        await ctx.send(f'Pong! :ping_pong: - {round(bot.latency * 1000)}ms')

    @commands.command(name = '8ball', help = " - Ask a question to the Magic 8 Ball and recieve your fortune...")
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

    @commands.command(name = "devs", help = " - List the developers of Vibe Bot.")
    @commands.has_role('Vibe Master')
    async def devs(ctx):
        await ctx.send("DEVS: Thomas Bivins")

    @commands.command(name = "purge", help = " - Purges (clears) the last specified amount of messages.")
    @commands.has_role('Janitor')
    @commands.has_permissions(manage_messages = True)
    async def purge(ctx, amount = 5):
        await ctx.channel.purge(limit = amount)

def setup(bot):
    bot.add_cog(usefulFunctions(bot))  