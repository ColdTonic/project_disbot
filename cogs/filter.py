import discord
import re
from discord.ext import commands

class filter(commands.Cog):
    def __init__(self, client):
        self.client = client

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
        

def setup(client):
    client.add_cog(filter(client))