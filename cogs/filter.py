import discord
import re
from discord.ext import commands

#announcement reactions mapping
ann_react_map = {
    "🐺": 841157129082634260, #VIC
    "🦉": 841157218325626900, #NSW
    "🦋": 841157239762714645, #QLD
    "🦁": 841157258673913906, #WA
    "🐬": 841157357777059850 #SA
}
class filter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        #discord -> "copy_id" message
        self.reaction_message = await self.client.get_channel(822706554393853963).fetch_message(841148340124385280)
        print(self.reaction_message.content)

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
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == self.reaction_message.id:
            role = self.client.get_guild(820532335802843136).get_role(ann_react_map[payload.emoji.name])
            await payload.member.add_roles(role, reason="location role assignment")

    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        member = self.client.get_guild(820532335802843136).get_member(payload.user_id)
        role = self.client.get_guild(820532335802843136).get_role(ann_react_map[payload.emoji.name])
        print(payload)

        #await payload.member.remove_roles(role, reason="remove reacted role")

def setup(client):
    client.add_cog(filter(client))