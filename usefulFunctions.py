import random
import discord
from discord.ext.commands import bot
from discord.ext import commands


class usefulFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll", help=" - Roll a die with the requested amount of sides.")
    @commands.has_role('Vibe Master')
    # every command must include context (ctx) before signature / #type cast from string to int
    async def roll(self, ctx, number_of_sides: int):
        # generate a random number in the specified range / #must type case back from int to string to display on discord
        roll = str(random.randint(1, number_of_sides))
        # await call and send message
        await ctx.send("{} rolled a {}!".format(ctx.author, roll))

    @commands.command(name="ping", help=" - Display the latency of Vibe Bot.")
    @commands.has_role('Vibe Master')
    async def ping(self, ctx):
        await ctx.send(f'Pong! :ping_pong: - {round(self.bot.latency * 1000)}ms')

    @commands.command(name='eightball', help=" - Ask a question to the Magic 8 Ball and recieve your fortune...")
    @commands.has_role('Vibe Master')
    async def _8ball(self, ctx, *, question):
        embed = discord.Embed(title = ":8ball: ***The magic 8 ball says...***", color = 0xa09c9c)
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
        embed.add_field(name = "Question: ", value = question, inline=True)
        embed.add_field(name = "Answer: ", value = random.choice(responses), inline=True)
        embed.set_footer(text = "Vibe Bot")
        await ctx.send(embed=embed)

    @commands.command(name="purge", help=" - Purges (clears) the last specified amount of messages.")
    @commands.has_role('Janitor')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    
    @commands.command(name='poll', help=" - Create a new poll")
    @commands.has_role('Vibe Master')
    async def poll(self, ctx, *, message):
        await ctx.channel.purge(limit=1)
        embed=discord.Embed(title = "***Poll***", description = f"{message}")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')



def setup(bot):
    bot.add_cog(usefulFunctions(bot))
