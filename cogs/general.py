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
		
    @commands.command()
    async def get_history(self, ctx):
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


def setup(client):
    client.add_cog(General(client))




