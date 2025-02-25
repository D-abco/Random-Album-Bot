import random
import json
import hikari
import lightbulb
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

def load_albums(artist: str):
    file_path = Path(__file__).parent / "albums" / f"{artist}.json"
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["artist"], data["albums"] 
    return None, [] 

def get_artists():
    albums_dir = Path(__file__).parent / "albums"
    return [file.stem for file in albums_dir.glob("*.json")]

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = lightbulb.BotApp(token=BOT_TOKEN, intents=hikari.Intents.GUILD_MESSAGES)

@bot.command()
@lightbulb.option("artist", "The artist to get a random album from", required=True, autocomplete=True)
@lightbulb.command("randomalbum", "Get a random album from a specified artist!")
@lightbulb.implements(lightbulb.SlashCommand)
async def random_album(ctx: lightbulb.Context) -> None:
    artist = ctx.options.artist.lower().replace(" ", "_")
    artist_name, albums = load_albums(artist)
    if albums:
        album = random.choice(albums)
        await ctx.respond(f"🎵{artist_name}: {album}🎵")
    else:
        await ctx.respond(f"No albums found for {ctx.options.artist}.")

@bot.listen(hikari.InteractionCreateEvent)
async def on_interaction(event: hikari.InteractionCreateEvent) -> None:
    interaction = event.interaction
    if isinstance(interaction, hikari.AutocompleteInteraction):
        if interaction.command_name == "randomalbum":
            for option in interaction.options:
                if option.name == "artist": 
                    search = option.value.lower()
                    artists = get_artists()
                    suggestions = [artist for artist in artists if search in artist.lower()]  
                    choices = [hikari.CommandChoice(name=artist, value=artist) for artist in suggestions[:5]]
                    await interaction.create_response(choices=choices)

bot.run()