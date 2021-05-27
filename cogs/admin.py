import discord
import pandas as pd
import asyncio
import re
import datetime
import random
from matplotlib import pyplot as plt
from discord.ext import tasks, commands

class admin(commands.Cog):
    def __init__(self, client):
        self.client = client

#To filter out the inappropriate words
    @commands.Cog.listener()
    async def on_message(self, message):

        content_list=[]
        new=[]
        f = open("src/BadWords.txt", "r")
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
                print("{0}'s message has been removed. Contents: {1}".format(message.author, message.content))

#To clear lines of text in channel
    @commands.command(help='[Tutor+ Role] Bans user. Cmd: !clear <num_messages>')
    @commands.has_any_role('Tutor', 'Admin')
    async def clear(self, ctx, amount=0):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'{amount} *lines of messages has been deleted.*')

#To kick a member
    @commands.command(help='[Tutor+ Role] Kicks user. Cmd: !kick <@User>')
    @commands.has_any_role('Tutor', 'Admin')
    async def kick(self, ctx, member : discord.Member):
        await member.kick()
        await ctx.send(f'{member.name} *has been kicked from the channel.*')

#To ban a member
    @commands.command(help='[Tutor+ Role] Bans user. Cmd: !ban <@User>')
    @commands.has_any_role('Tutor', 'Admin')
    async def ban(self, ctx, member : discord.Member):
        await member.ban()
        await ctx.send(f'{member.name} *has been banned from the channel.*')

#To unban a member
    @commands.command(help='[Tutor+ Role] Unbans user. Cmd: !unban <@User>')
    @commands.has_any_role('Tutor', 'Admin')
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_no = member.split('#')

        for id in banned_users:
            user = id.user
            if (user.name, user.discriminator) == (member_name, member_no):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.name} *has been unbanned from the channel.*') 

#To mute a member for certain time
    @commands.command(help= '[Tutor+ Role] Mutes user. Cmd: !mute <@User>')
    @commands.has_any_role('Tutor', 'Admin')
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
    @commands.command(help = '[Tutor+ Role] Assigns role. Cmd: !role <@User> Student')
    @commands.has_any_role('Tutor', 'Admin')
    async def role(self, ctx, member: discord.Member=None,*, role=""):
        guild = ctx.guild
        if role=="":
            await ctx.send(f'*Sorry! you have to mention a role name.*')
        else:
            assign_role = discord.utils.get(guild.roles, name = role)
            await member.add_roles(assign_role)
            await ctx.send(f'**{member.mention} has been assigned to {role} role.**')

#To remove a role from a member
    @commands.command(help = '[Tutor+ Role] Removes role. Cmd: !removeRole <@User>')
    @commands.has_any_role('Tutor', 'Admin')
    async def removeRole(self, ctx, member: discord.Member=None, role=""):
        guild = ctx.guild
        if role=="":
            await ctx.send(f'*Sorry! you have to mention a role name.*')
        else:
            assign_role = discord.utils.get(guild.roles, name = role)
            await member.remove_roles(assign_role)   
            await ctx.send(f'**{member.mention} has been removed from {role} role.**')

#To count most used word
    @commands.command(help = '[Tutor+ Role] Requires !get_history. Cmd: !countword')
    @commands.has_any_role('Tutor', 'Admin')
    async def countword(self,ctx):

        df = pd.read_csv("src/data.csv")
        df = df[df["author"] != 'Project Disbot']
        await ctx.channel.send(df['content'].str.split().explode().value_counts()[:10])

    #Create visualisation for word count
    @commands.command(help='[Tutor+ Role] Visualise feedback. Cmd: !plt_count', aliases=['viscount', 'plot_feedback', 'plt_count', 'visualise'])
    @commands.has_any_role('Tutor', 'Admin')
    async def visualisecount(self, ctx):

        #Read data file obtained from !get_history
        df = pd.read_csv('src/data.csv')
        
        #Use pd transformations to filter Disbot commands and plot value counts.
        df = df[df["author"] != 'Disbot']
        df['content'].str.split().explode().value_counts()[:10].plot(kind="bar",color="green", figsize=(10,8))
        plt.title("Word Frequencies")
        plt.ylabel('Frequency')
        plt.savefig("src/wordcounter.png")

        #Set discord file location from CDN
        f = discord.File("src/wordcounter.png", filename="wordcounter.png")

        #Create embed and push embed back to user to visualise results.
        plot = discord.Embed(title="Count feedback", description=f'Frequently used words.')
        plot.set_image(url='attachment://src/wordcounter.png')
        await ctx.send('Word count visualisation', file=f)

    #Grab server history where number of entries + ChannelID are configurable parameters
    #Takes feedback from only the feedback channel for the time being
    @commands.command(help = '[Tutor+ Role] Extracts feedback logs Cmd: !get_history')
    @commands.has_any_role('Tutor', 'Admin')
    async def get_history(self, message, *, lim=200):
        #empty dataframe
        data = pd.DataFrame(columns=['msg_id', 'content', 'time',
                                    'author', 'channel'])

        #grab list of channel history in #feedback
        messages = await self.client.get_channel(845906253326188574).history(limit=lim).flatten()

        #loop through each message and save to empty dataframe
        for msg in messages:
            data = data.append({'msg_id': msg.id,
                                    'content': msg.content,
									'time': msg.created_at,
									'author': msg.author.name,
                                    'channel': msg.channel
                                    }, ignore_index=True)
        
        #declare file location + save as csv for analytics
        file_location= "src/data.csv"
        data.to_csv(file_location)
        
        await message.channel.send("Data saved. Consult your administrator for data file.")

    #Change colour, alias added for localisation spelling
    #Checks permissions manage_roles = True
    @commands.command(help = '[Tutor+ Role] Gives random colour. Cmd: !changecolour <@Role>', aliases=['changecolour'])
    @commands.has_any_role('Tutor', 'Admin')
    async def changecolor(self, ctx, role: discord.Role):
        # Try change colour, notify user that colour has been changed.
        try:
            await role.edit(color=discord.Color(random.randint(0x000000, 0xFFFFFF)))
            await ctx.send("Colour has been changed. Check role to see new colour")
        except Exception as error:
            raise(error)

def setup(client):
    client.add_cog(admin(client))