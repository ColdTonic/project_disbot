import discord
from discord.ext import commands
import random
import os
import re

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

def setup(client):
    client.add_cog(General(client))




