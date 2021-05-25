import discord
from discord.ext import commands
import random
import os
import re
import pandas as pd

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
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')
    
    @commands.command(aliases=['avatar', 'user'])
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
    
    @commands.command(aliases=['server_profile'])
    async def serverinfo(self, ctx):

        embed = discord.Embed(title="Instatute Server Statistics")
        embed.add_field(name="Region:", value=ctx.guild.region, inline=False)
        embed.add_field(name="Number of members:", value=ctx.guild.member_count, inline=False)
        embed.add_field(name="Server created:", value=ctx.guild.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"), inline=False)
        await ctx.send(embed=embed)
		
    @commands.command()
    async def get_history(self, message):
        #empty dataframe
        data = pd.DataFrame(columns=['msg_id', 'content', 'time',
                                    'author', 'channel'])

        #grab list of channel history in #feedback
        messages = await self.client.get_channel(845906253326188574).history(limit=200).flatten()

        #loop through each message and save to empty dataframe
        for msg in messages:
            data = data.append({'msg_id': msg.id,
                                    'content': msg.content,
									'time': msg.created_at,
									'author': msg.author.name,
                                    'channel': msg.channel
                                    }, ignore_index=True)
        
        #declare file location + save as csv for analytics
        file_location= "data.csv"
        data.to_csv(file_location)
        
        await message.channel.send("Data saved. Consult your administrator for data file.")

    @commands.command(aliases=['changecolour'])
    @commands.has_permissions(manage_roles=True)
    async def changecolor(self, ctx, role: discord.Role):
        try:
            await role.edit(color=discord.Color(random.randint(0x000000, 0xFFFFFF)))
            await ctx.send("Colour has been changed. Check role to see new colour")
        except Exception as error:
            raise(error)

def setup(client):
    client.add_cog(General(client))




