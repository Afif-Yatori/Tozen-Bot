import discord
from discord.ext import commands
import Game

client = commands.Bot(command_prefix= "^")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("use ^start to call me for the first time"))
    print("deployed")

@client.command()
async def servers(ctx):
    await ctx.send("I'm in " + str(len(client.guilds)) + " servers")

#@client.command()
#async def test(ctx):
 #   ID = ctx.author.id
  #  await ctx.send(test(ID))

@client.command()
async def start(ctx):
    author = ctx.author
    ID = ctx.author.id
    channelid = ctx.channel.id
    if Game.existing_char(ID) == None:
        await ctx.send(Game.start(ID))
        def check(m):
            return m.author == author and m.channel.id == channelid
        msg = await client.wait_for('message', check=check)
        await ctx.send(Game.welcome(msg.content))
        msg2 = await client.wait_for('message', check=check)
        await ctx.send(Game.createchar(msg.content, msg2.content, ID))
    else:
        await ctx.send("You already have a character")


@client.command()
async def learnskill(ctx):
    ID = ctx.author.id
    author = ctx.author
    channelid = ctx.channel.id
    if Game.checkskill(ID)!= None:
        await ctx.send("There are 2 types of skills: active and passive , which are furthermore separated into 5 different tiers : Common, Rare , Epic , Legendary and Mythic. A passive skill does not require mana but is only used after a condition has been fulfilled while active skills require mana to be used. Which type of skill would you like?(Only choose for active for now since passive will make it bug)")
        def check(m):
            return m.author == author and m.channel.id == channelid
        msg = await client.wait_for('message', check=check)
        if ID == 257115950623490049:
            await ctx.send(Game.skillafif(ID, msg.content))
        else:
            await ctx.send(Game.randomskill(ID, msg.content))
    else:
        await ctx.send(f"<@{ID}>,you either don't have a character or you already have at least a skill")

@client.command()
async def statpoints(ctx):
    ID = ctx.author.id
    author = ctx.author
    channelid = ctx.channel.id
    def check(m):
        return m.author == author and m.channel.id == channelid
    if Game.statpoints(ID) == None:
        await ctx.send("You don't have a character yet")
    elif Game.statpoints(ID) < 5:
        await ctx.send(f"You currently have {Game.statpoints(ID)} available statpoints. It is below 5 so you cannot increase a stat.")
    elif Game.statpoints(ID) >= 5:
        await ctx.send(f"You currently have {Game.statpoints(ID)} available statpoints. It's above or equal to 5 which means you can improve a stat of your choice. Would you like to? Please answer with yes or no.")
        msg = await client.wait_for('message', check=check)
        if Game.use_statpoints(ID, msg.content) != None:
            await ctx.send(Game.use_statpoints(ID, msg.content))
            msg2 = await client.wait_for('message', check=check)
            await ctx.send(Game.chosen_statpoint(ID, msg2.content))
    else:
        await ctx.send("???")

@client.command()
async def mana(ctx):
    ID = ctx.author.id
    await ctx.send(Game.add_mana(ID))

@client.command()
async def hp(ctx):
    ID = ctx.author.id
    await ctx.send(Game.add_hp(ID))

@client.command()
async def stats(ctx):
    ID = ctx.author.id
    await ctx.send(Game.stats(ID))

@client.command()
async def floor(ctx):
    ID = ctx.author.id
    await ctx.send(Game.floor(ID))

@client.command()
async def status(ctx):
    ID = ctx.author.id
    await ctx.send(Game.currentinfo(ID))

@client.command()
async def monsterinformation(ctx):
    ID = ctx.author.id
    author = ctx.author
    channelid = ctx.channel.id
    await ctx.send("Which floor's monsters would you like to see?")
    def check(m):
        return m.author == author and m.channel.id == channelid

    msg = await client.wait_for('message', check=check)

    if Game.valuecheck(msg.content) != None:
        await ctx.send(Game.floormonsters(ID, Game.valuecheck(msg.content)))
    else:
        await ctx.send("This is not a number.")

@client.command()
async def titleon(ctx):
    ID = ctx.author.id
    await ctx.send(Game.titleon((ID)))

@client.command()
async def afif(ctx):
    ID = ctx.author.id
    await ctx.send(Game.Yatori(ID))

@client.command()
async def titles(ctx):
    ID = ctx.author.id
    author = ctx.author
    channelid = ctx.channel.id
    current_titles = Game.current_titles_available(ID)
    if current_titles != "You don't have a title except the one which is equipped" and current_titles != "You don't have a character yet":
        await ctx.send(current_titles)
        await ctx.send("Would you like to change the current equipped title? Please answer with yes or no")
        def check(m):
            return m.author == author and m.channel.id == channelid

        msg = await client.wait_for('message', check=check)
        if msg.content == "yes":
            await ctx.send("Which title would you like to equip")
            msg2 = await client.wait_for('message', check=check)
            await ctx.send(Game.weartitle(ID, msg2.content))
    else:
        await ctx.send(current_titles)

@client.command()
async def skills(ctx):
    ID = ctx.author.id
    await ctx.send(Game.skills(ID))

@client.command()
async def bal(ctx):
    ID = ctx.author.id
    await ctx.send(Game.getbal(ID))

@client.command()
async def shop(ctx):
    ID = ctx.author.id
    author = ctx.author
    channelid = ctx.channel.id
    await ctx.send("Current purchasable items : Life Potion(refills your hp by 50) for 600 Gold and Stamina Potion(refills your stamina by 50) for 600 Gold. Would you like to purchase an item? Please answer with yes or no")
    def check(m):
        return m.author == author and m.channel.id == channelid
    msg = await client.wait_for('message', check=check)
    if msg.content == "yes":
        await ctx.send("Which item would you like to buy?")
        msg2 = await client.wait_for('message', check=check)
        if msg2.content.lower() == "life potion" or msg2.content.lower() == "stamina potion":
            await ctx.send(Game.shop(ID, msg2.content))
        else:
            await ctx.send("I do not understand your request , please come by soon again.")
    elif msg.content == "no":
        await ctx.send("Please come by another time then :/")
    else:
        await ctx.send("I do not understand your request , please come by soon again.")

@client.command()
async def use(ctx, *, arg):
   ID = ctx.author.id
   if arg == "Life Potion" or "Stamina Potion":
       await ctx.send(Game.use(ID, arg))
   else:
       await ctx.send("Item has not been found")


@client.command()
async def monster(ctx):
    ID = ctx.author.id
    author = ctx.author
    channelid = ctx.channel.id
    if Game.checkskill(ID) == None:
        await ctx.send(Game.monsterrecog(ID))
        if Game.enoughmana(ID)== None:
            await ctx.send("You do not have enough mana to use a skill. Would you like to attack with your sword or quit? Please answer with either Sword or Quit. Answering something else will be considered quitting!")
            def check(m):
                return m.author == author and m.channel.id == channelid
            msg = await client.wait_for('message', check=check)
            await ctx.send(Game.automode2(ID, msg.content))
            while Game.hp(ID) == None:
                if Game.enoughmana(ID) != None:
                    await ctx.send(Game.monsteratt(ID))
                    await ctx.send("Would you like to attack with your sword, use a skill or quit?Quitting means losing all your hp. Please answer with either Sword,Skill or Quit. Answering something else will be considered quitting!")
                    msg = await client.wait_for('message', check=check)
                    await ctx.send(Game.automode2(ID, msg.content))
                else:
                    await ctx.send(Game.monsteratt(ID))
                    await ctx.send("You do not have enough mana to use a skill. Would you like to attack with your sword or quit? Please answer with either Sword or Quit. Answering something else will be considered quitting!")
                    msg = await client.wait_for('message', check=check)
                    await ctx.send(Game.automode2(ID, msg.content))
        else:
            await ctx.send("Would you like to attack with your sword, use a skill or quit?Quitting means losing all your hp. Please answer with either Sword,Skill or Quit. Answering something else will be considered quitting!")
            def check(m):
                return m.author == author

        msg = await client.wait_for('message', check=check)
        await ctx.send(Game.automode2(ID, msg.content))
        while Game.hp(ID) == None:
            if Game.enoughmana(ID) != None:
                await ctx.send(Game.monsteratt(ID))
                await ctx.send("Would you like to attack with your sword, use a skill or quit?Quitting means losing all your hp. Please answer with either Sword,Skill or Quit. Answering something else will be considered quitting!")
                msg = await client.wait_for('message', check=check)
                await ctx.send(Game.automode2(ID, msg.content))
            else:
                await ctx.send(Game.monsteratt(ID))
                await ctx.send("You do not have enough mana to use a skill. Would you like to attack with your sword or quit? Please answer with either Sword or Quit. Answering something else will be considered quitting!")
                msg = await client.wait_for('message', check=check)
                await ctx.send(Game.automode2(ID, msg.content))
    elif Game.checkskill(ID) == "exists but no skill":
        await ctx.send("Please finish the second part of the divine ceremony by using ^learnskill before trying to fight monsters!")
    else:
        await ctx.send("You did not create a character yet. Please create one using ^start.")






@client.command()
async def floorboss(ctx):
    ID = ctx.author.id
    author = ctx.author
    channelid = ctx.channel.id
    if Game.checkskill(ID) == None:
        Game.floorboss(ID)
        await ctx.send(Game.welcomemessage(ID))
        def check(m):
            return m.author == author and m.channel.id == channelid
        message = await client.wait_for('message', check=check)
        if (message.content).lower() == "yes":
            if Game.enoughmana(ID) == None:
                await ctx.send("You do not have enough mana to use a skill. Would you like to attack with your sword or quit? Please answer with either Sword or Quit. Answering something else will be considered quitting!")
                msg = await client.wait_for('message', check=check)
                await ctx.send(Game.automode3(ID, msg.content))
                while Game.hp2(ID) == None:
                    if Game.enoughmana(ID) != None:
                        await ctx.send(Game.bossatt(ID))
                        await ctx.send("Would you like to attack with your sword, use a skill or quit?Quitting means losing all your hp. Please answer with either Sword,Skill or Quit. Answering something else will be considered quitting!")
                        msg = await client.wait_for('message', check=check)
                        await ctx.send(Game.automode3(ID, msg.content))
                    else:
                        await ctx.send(Game.bossatt(ID))
                        await ctx.send("You do not have enough mana to use a skill. Would you like to attack with your sword or quit? Please answer with either Sword or Quit. Answering something else will be considered quitting!")
                        msg = await client.wait_for('message', check=check)
                        await ctx.send(Game.automode3(ID, msg.content))
            else:
                await ctx.send("Would you like to attack with your sword, use a skill or quit?Quitting means losing all your hp. Please answer with either Sword,Skill or Quit. Answering something else will be considered quitting!")
                msg = await client.wait_for('message', check=check)
                await ctx.send(Game.automode3(ID, msg.content))
                while Game.hp2(ID) == None:
                    if Game.enoughmana(ID) != None:
                        await ctx.send(Game.bossatt(ID))
                        await ctx.send("Would you like to attack with your sword, use a skill or quit?Quitting means losing all your hp. Please answer with either Sword,Skill or Quit. Answering something else will be considered quitting!")
                        msg = await client.wait_for('message', check=check)
                        await ctx.send(Game.automode3(ID, msg.content))
                    else:
                        await ctx.send(Game.bossatt(ID))
                        await ctx.send("You do not have enough mana to use a skill. Would you like to attack with your sword or quit? Please answer with either Sword or Quit. Answering something else will be considered quitting!")
                        msg = await client.wait_for('message', check=check)
                        await ctx.send(Game.automode3(ID, msg.content))
        else:
            await ctx.send("You'll need to beat the Floorboss one day to continue your adventure.")
    elif Game.checkskill(ID) == "exists but no skill":
        await ctx.send("Please finish the second part of the divine ceremony by using ^learnskill before trying to fight the floorboss!")
    else:
        await ctx.send("You did not create a character yet. Please create one using ^start.")







client.run("your bot token")
