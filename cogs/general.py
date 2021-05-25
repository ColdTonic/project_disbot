import discord
from discord.ext import commands
import random
import pandas as pd
import source.hangman_questions as hm

#notes to develop - when important custom created files, note that the current directory is project_disbot's ROOT directory
#if your file is located in the same directory as here please use cogs.{my-file}

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
    
    @commands.command()
    async def han(self, ctx, *, difficulty="easy"):

        #init variable qna
        qna=""

        #set words based off difficulty
        if difficulty =="easy":
            qna = hm.easy()
        elif difficulty =="normal":
            qna = hm.normal()
        elif difficulty =="hard":
            qna = hm.hard()

        #generate hangman word
        key = random.choice(list(qna.values()))

        # #generate mystery letters
        temp = ""
        for i in range(0, len(key)):
             temp += "?"
        await ctx.send("Hangman Initiated. The word is: "+ temp)

        #guess recieved from user
        guess = await self.client.wait_for('message')

        #add guesses to a list
        user_guesses = list()

        for c in key.lower():
            if guess == c or c in user_guesses:
                temp += c
            else:
                temp += "?"
        user_guesses.append(guess.content.lower())

        #check if word has been answered, else show game progress
        if guess.content.lower() == key:
            await ctx.send("You guessed correctly, good job! The word was: " + key)
        else:
            await ctx.send("Progress: {0}".format(temp))
            guesses_str = ",".join(user_guesses)
            await ctx.send("Guess so far: {0}".format(guesses_str))
        
        if len(user_guesses) >= len(key):
            await ctx.send("Game over. The word was: {0}".format(key))
            return


def setup(client):
    client.add_cog(General(client))




