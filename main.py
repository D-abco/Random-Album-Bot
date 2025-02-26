import os
import hikari
import lightbulb
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Discord bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize the bot with the specified token and intents
bot = lightbulb.BotApp(token=BOT_TOKEN, intents=hikari.Intents.GUILD_MESSAGES)

# Import and add commands from the commands folder
from commands import randomalbum

randomalbum.load(bot)

# Run the bot
bot.run()