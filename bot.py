# bot.py
import os # for importing env vars for the bot to use
import time,datetime # for uptime graceful output
import json # for import/export data like bot list
from twitchio.ext import commands

bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=os.environ['CHANNEL'],
)


start_time =time.time()
adminlist = ['your channel username','userername who need access','another username who need access' ] 
with open('twitchbotlist.txt', 'r') as filehandle:
    twitchbotlist = json.load(filehandle)


@bot.event
async def event_ready():
#    'Called once when the bot goes online.'
    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")


# Parse chat and replies

@bot.event
async def event_message(ctx):
#    'Runs every time a message is sent in chat.'

    # make sure the bot ignores itself and the streamer
    username = str(ctx.author.name.lower())
    await bot.handle_commands(ctx)

#There we can do block term list with scan chat.

    # await ctx.channel.send(ctx.content)

    if 'hello' in ctx.content.lower():
        if username not in twitchbotlist:
            await ctx.channel.send(f"Hi, @{ctx.author.name}!")

# Greeting newcomer
@bot.event
async def event_join(user):    
    if str(user.name.lower()) not in twitchbotlist:
        print([str(user.name)])
        await bot._ws.send_privmsg(str(user.channel), f"Привіт, {user.name} вітаємо на каналі та бажаємо гарного перегляду!")
 
# Check is bot an active
@bot.command(name='ping')
async def tested(ctx):
    await ctx.send('pong!')

# Display bot uptime
@bot.command(name='bot_up')
async def bot_uptime(ctx):
    bot_up_seconds =  int(time.time() - start_time)
    bot_up_format = str(datetime.timedelta(seconds=bot_up_seconds))
    await ctx.send(f"This bot up for {bot_up_format}")

# Add nickname to ungreetings list
@bot.command(name='bot_add')
async def bot_add(ctx):
    if str(ctx.author.name.lower()) in adminlist:
        bot_name = ctx.content.lower().lstrip('!bot_ad@').strip()
        if str(bot_name) not in twitchbotlist:
            twitchbotlist.append(bot_name)
            with open('twitchbotlist.txt', 'w') as filehandle:
                json.dump(twitchbotlist, filehandle)
        else:
            await ctx.send(f"{bot_name} - already unhelloed")
    else:
         await ctx.send(f"/w {ctx.author.name.lower()} !bot_add Permission denied")

if __name__ == "__main__":
        bot.run()

