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
    #Pings user and checks client latency to the server. Used for Bot-end testing.
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')
    
    #Display user profile using embeds - no additional user permissions required
    #other variations that this command can be called are user or avatar
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
    
    #Display server profile via embeds.
    #other variations that said command can be called is server_profile
    @commands.command(aliases=['server_profile'])
    async def serverinfo(self, ctx):

        f = discord.File("src/server_profile.jpg", filename="server_profile.jpg")
        embed = discord.Embed(title="Instatute Server Statistics")
        embed.set_thumbnail(url="attachment://server_profile.jpg")
        embed.add_field(name="Region:", value=ctx.guild.region, inline=False)
        embed.add_field(name="Number of members:", value=ctx.guild.member_count, inline=False)
        embed.add_field(name="Server created:", value=ctx.guild.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"), inline=False)
        await ctx.send(embed=embed, file=f)

#Add cog of generic functions
def setup(client):
    client.add_cog(General(client))




