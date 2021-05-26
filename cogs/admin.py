import discord
import pandas as pd
import asyncio
import re
import datetime
from discord.ext import tasks, commands


class admin(commands.Cog):
    def __init__(self, client):
        self.client = client

#To filter out the inappropriate words
    @commands.Cog.listener()
    async def on_message(self, message):

        content_list=[]
        new=[]
        f = open("cogs/BadWords.txt", "r")
        for line in f:
            content_list = line.split(",")

        val = message.content.lower()

        data1 = []
        data = val.split(" ")
        for i in data:
            i = re.sub(r"[^a-zA-Z0-9]+",'',i)
            data1.append(i)

        for a in content_list:
            for b in data1:
                if a==b:
                    new.append("censored line")
            
        for a in new:
            if a=="censored line":
                await message.delete()
                await message.channel.send (" *Inappropriate words or phrase are not allowed.* ")

#To clear lines of text in channel
    @commands.command()
    async def clear(self, ctx, amount=0):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'{amount} *lines of messages has been deleted.*')

#To kick a member
    @commands.command()
    async def kick(self, ctx, member : discord.Member):
        await member.kick()
        await ctx.send(f'{member.name} *has been kicked from the channel.*')

#To ban a member
    @commands.command()
    async def ban(self, ctx, member : discord.Member):
        await member.ban()
        await ctx.send(f'{member.name} *has been banned from the channel.*')

#To unban a member
    @commands.command()
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_no = member.split('#')

        for id in banned_users:
            user = id.user
            if (user.name, user.discriminator) == (member_name, member_no):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.name} *has been unbanned from the channel.*') 

#To mute a member for certain time
    @commands.command()
    async def mute(self, ctx, member: discord.Member=None, time=0.5):

        guild = ctx.guild
        Muted = discord.utils.get(guild.roles, name="Muted")
        
        await member.add_roles(Muted)
        muted_embed = discord.Embed(title="Member is muted!", description=f'{member.mention} is muted by Admin for {time} min.')
        await ctx.send(embed=muted_embed)
        await asyncio.sleep(int(time*60))
        await member.remove_roles(Muted)
        unmute_embed = discord.Embed(title="Mute over!", description=f'Mute time over for {member.mention}.')
        await ctx.send(embed=unmute_embed)

#To assign a role to member
    @commands.command()
    async def role(self, ctx, member: discord.Member=None,*, role=""):
        guild = ctx.guild
        if role=="":
            await ctx.send(f'*Sorry! you have to mention a role name.*')
        else:
            assign_role = discord.utils.get(guild.roles, name = role)
            await member.add_roles(assign_role)
            await ctx.send(f'**{member.mention} has been assigned to {role} role.**')

#To remove a role from a member
    @commands.command()
    async def removeRole(self, ctx, member: discord.Member=None, role=""):
        guild = ctx.guild
        if role=="":
            await ctx.send(f'*Sorry! you have to mention a role name.*')
        else:
            assign_role = discord.utils.get(guild.roles, name = role)
            await member.remove_roles(assign_role)   
            await ctx.send(f'**{member.mention} has been removed from {role} role.**')

#To count most used word
    @commands.command()
    async def countword(self,ctx):

        df = pd.read_csv("cogs/data.csv")
        df = df[df["author"] != 'Project Disbot']
        await ctx.channel.send(df['content'].str.split().explode().value_counts()[:10])
    

def setup(client):
    client.add_cog(admin(client))