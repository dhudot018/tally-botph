import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '/', intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready.")


#global variables
tally = {}
answers = 0
message_id = None
ongoing = False

#when a user reacted to a message
@bot.event
async def on_reaction_add(reaction, user):
    global tally 
    if reaction.message.content.startswith('POLL:') and reaction.message.id == message_id:
        if str(reaction.emoji) in tally:
            if user.name not in tally[str(reaction.emoji)] and user.name != "Tally Bot":
                tally[str(reaction.emoji)].append(user.name)
        elif str(reaction.emoji) not in tally and user.name != "Tally Bot":
            tally[str(reaction.emoji)] = [user.name]

#when a user remove a reaction from a message
@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == message_id:
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, bot.guilds)
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        if member is not None:
            tally[str(payload.emoji.name)].remove(member.name)


@bot.command(aliases = ["tally"])
async def tally_(ctx, *, feature):
    members = []
    repeater = []

    feature = feature.split(" ")

    if feature[0] == "text_channel":
        text_channel = ctx.guild.get_channel(ctx.channel.id)
        for member in text_channel.members:
            flag = True
            for role in member.roles:
                if role.name == "BOT":
                    flag = False
                    break
            if flag:
                members.append(member.name)
        
    elif feature[0] == "voice_channel":
        try:
            voice_channel = ctx.author.voice.channel
            for member in voice_channel.members:
                members.append(member.name)
        except:
            await ctx.send("You are not in a Voice channel.")

    global tally
    members.sort()
    
    await ctx.message.delete()
    
    if message_id != None and len(members) != 0:
        string = "Tallying Latest Poll:\n"
        for emoji in tally:
            if len(tally[emoji]) != 0:
                string += "# of users who voted in " + emoji + " is " + str(len(tally[emoji])) + ":\n"
                tally[emoji].sort() 
                for user in tally[emoji]:
                    string += user + "\n"
                    if user in members:
                        members.remove(user)
                    else:
                        if user not in repeater:
                            repeater.append(user)    
        string += "================================================\n"
        if len(members) != 0:
            string += "Users who did not vote.\n"
            for user in members:
                string += str(user) + "\n"
        else:
            string += "Everyone voted.\n"
        if len(repeater) != 0:
            string += "================================================\n"
            string += "Users who voted more than once.\n"
            for user in repeater:
                string += str(user) + "\n"

        await ctx.send(string)
        global ongoing
        ongoing = False
    elif message_id == None and len(members) != 0:
        string = "No Available Poll yet!"
    
    

emoji = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯"]
@bot.command(aliases=["vote"])
async def vote_(ctx, *, args):
    global answers, ongoing, tally
    await ctx.message.delete()
    if not ongoing:

        ongoing = True
        args = args.split(", ")
        answers = len(args) - 1


        string = "POLL:\n\n" + args.pop(0) + "\n\n"
        for i in range(answers):
            string += str(emoji[i]) + "    " + args[i] + "\n"
        
        await ctx.send(string)

        
        tally = {}
    else:
        await ctx.send("There's an onging poll! Tally it first.")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author == bot.user and message.content.startswith("POLL:"):
        global message_id
        message_id = message.id
        for i in range(answers):
            await message.add_reaction(str(emoji[i]))

bot.run('Nzk1Mzc4NTE4Mzc1NzkyNjcx.X_If-A.wolkqInTjeAKS8SZDzZ6fNPdHI8')