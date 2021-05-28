import discord
from discord.ext import commands
import random

class General(commands.Cog):

    def __init__(self, client):
        self.client = client
    #Events
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
        )

    #Commands
    #Pings user and checks client latency to the server. Used for Bot-end testing.
    @commands.command(help = 'Check bot latency. Cmd: !ping')
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')
    
    #Display user profile using embeds - no additional user permissions required
    #other variations that this command can be called are user or avatar
    @commands.command(help = 'Display user profiles. Cmd: !userinfo <@Discord username>', aliases=['avatar', 'user'])
    async def userinfo(self, ctx, member: discord.Member = None):
        roles = [role for role in ctx.author.roles[1:]]
                
        member = ctx.author if member is None else member
        embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f"User Info: {member}")
        embed.add_field(name="Preferred name:", value=member.display_name)
        embed.add_field(name="Position:", value=member.top_role.mention)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Account information for: {member}", icon_url=member.avatar_url)
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Account created:", value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Join date:", value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))
        embed.add_field(name=f"Allocated roles: ({len(roles)})", value="".join([role.mention for role in roles]))
        await ctx.send(embed=embed)
    
    #Display server profile via embeds.
    #other variations that said command can be called is server_profile
    @commands.command(help = 'Display server profile. Cmd: !serverinfo ',aliases=['server_profile'])
    async def serverinfo(self, ctx):

        f = discord.File("src/server_profile.jpg", filename="server_profile.jpg")
        embed = discord.Embed(title="Instatute Server Statistics")
        embed.set_thumbnail(url="attachment://server_profile.jpg")
        embed.add_field(name="Region:", value=ctx.guild.region, inline=False)
        embed.add_field(name="Number of members:", value=ctx.guild.member_count, inline=False)
        embed.add_field(name="Server created:", value=ctx.guild.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"), inline=False)
        await ctx.send(embed=embed, file=f)

    #Command for pure entertainment purposes, flips a coin and guesses heads or tails
    @commands.command(help='Flip a coin and guess correctly. Cmd: !coinflip heads')
    async def coinflip(self, ctx, *, guess):
        result = random.choice(['heads', 'tails'])
        guess = guess.lower()
        if result == guess:
            await ctx.send("You guessed correctly! The answer was: " + result)
        elif result == None:
            await ctx.send("I didn't get a choice, please try again.")
        elif result != guess:
            await ctx.send("Incorrect. Try again next time. Result was: " + result)

    #generate inspirational quotes
    @commands.command(help='Display random inspirational quotes. Cmd: !quotes')
    async def quotes(self,ctx):
        images=[
            'https://smedia2.intoday.in/indiatoday/images/stories/2016May/albert-einstein_053016040636.jpg',
            'https://www.azquotes.com/picture-quotes/quote-the-aim-of-education-is-the-knowledge-not-of-facts-but-of-values-william-ralph-inge-4-23-76.jpg',
            'https://i.pinimg.com/originals/8d/65/8b/8d658b78916b12b60580e7b9d21757a0.jpg',
            'https://smallbiztrends.com/ezoimgfmt/media.smallbiztrends.com/2019/07/yoda-star-wars-hard-work-quote-850x446.png?ezimgfmt=ng%3Awebp%2Fngcb12%2Frs%3Adevice%2Frscb12-1',
            'https://www.positivityblog.com/wp-content/uploads/work_quotes_1.webp',
            'https://www.positivityblog.com/wp-content/uploads/work_quotes_b1.webp',
            'https://www.positivityblog.com/wp-content/uploads/work_quotes_4.webp',
            'https://1.bp.blogspot.com/-PSvklELGSfE/XrpEEXySAII/AAAAAAAAsPo/5NDVI2Zt7VAlOLUu_IVqu6RNP7VPQgMygCLcBGAsYHQ/s1600/Inspirational-education-quotes-that-will-motivate-you%2B%25281%2529-min.jpg'
    
        ]
        #display random image in an embed
        embed=discord.Embed(color=discord.Colour.red())
        random_link=random.choice(images)
        embed.set_image(url=random_link)
        await ctx.send(embed=embed)


#Add cog of generic functions
def setup(client):
    client.add_cog(General(client))




