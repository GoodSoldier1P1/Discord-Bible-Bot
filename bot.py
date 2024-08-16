import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

BASE_BIBLE_URL = "https://bible-api.com/"


@bot.event
async def on_ready():
    """Prep bot for entering a server"""

    print(f'Logged in as {bot.user.name} ({bot.user.id})')


@bot.event
async def on_member_join(member):
    """DM member when they join the server"""
    await member.send(f'Welcome to the server, {member.name}!\n**Commands**:\n*Random Verse*: !verse or !random\n\n*Specific Verse Example*: !find 2 Timothy 2:3')


@bot.command()
async def hello(ctx):
    """Responds with a greeting"""
    await ctx.send("Hello there!")
    

@bot.command(name="verse", aliases=["random"])
async def random_verse(ctx):
    """Fetches and displays a random Bible verse"""
    random_url = BASE_BIBLE_URL + "?random=verse"
    
    response = requests.get(random_url)
    if response.status_code == 200:
        try:
            verse_data = response.json()
            reference = verse_data['reference']
            text = verse_data['verses'][0]['text']
            await ctx.send(f"{text} \n**{reference}**")
        except KeyError as e:
            await ctx.send("Sorry, I couldn't retrieve a verse at this time.")
            print(f"KeyError: {e}")
        except ValueError:
            await ctx.send("Sorry, there was an error processing the response.")
    else:
        await ctx.send(f"Failed to fetch Bible verse. Status code: {response.status_code}")


@bot.command(name="find")
async def find_verse(ctx, *, verse_reference: str):
    """Fetches and displays a specific Bible verse based on user input"""
    # Construct the API URL based on user input, ensuring it is case insensitive
    verse_reference = verse_reference.strip()
    api_url = BASE_BIBLE_URL + verse_reference

    # Fetch the verse from the API
    response = requests.get(api_url)
    if response.status_code == 200:
        try:
            verse_data = response.json()
            reference = verse_data['reference']
            text = verse_data['verses'][0]['text']
            await ctx.send(f"{text}\n**{reference}**")
        except KeyError as e:
            await ctx.send("Sorry, I couldn't retrieve the verse at this time.")
            print(f"KeyError: {e}")
        except ValueError:
            await ctx.send("Sorry, there was an error processing the response.")
    else:
        await ctx.send(f"Failed to fetch Bible verse. Status code: {response.status_code}")


@bot.listen('on_message')
async def on_message(message):
    """Listens for mentions of Bible Verses"""

    # Ensure the bot doesn't respond to its own messages
    if message.author == bot.user:
        return


    if "hello" in message.content.lower():
        await message.add_reaction("❤️")


    #Checks if it's a command message
    ctx = await bot.get_context(message)
    if ctx.valid:   # If it's a command
        return

    # Add logic here if you want to handle specific words or phrases
    # that should trigger a Bible verse lookup




# Run the bot
bot.run(TOKEN)