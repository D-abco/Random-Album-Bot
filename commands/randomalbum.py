import os
import json
import random
from pathlib import Path

import aiohttp
import hikari
import lightbulb
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Last.fm API key from environment variables
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")

# Function to check if the Last.fm API key is valid
async def is_lastfm_api_key_valid(api_key: str) -> bool:
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "album.getinfo",
        "api_key": api_key,
        "artist": "test",
        "album": "test",
        "format": "json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            # Return False if the API key is invalid
            if response.status == 403:
                return False
            return True

# Function to fetch the album description from Last.fm
async def fetch_album_description(artist: str, album: str) -> str:
    # Check if the Last.fm API key is valid
    if not LASTFM_API_KEY or not await is_lastfm_api_key_valid(LASTFM_API_KEY):
        return None
    
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "album.getinfo",
        "api_key": LASTFM_API_KEY,
        "artist": artist,
        "album": album,
        "format": "json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                description = data.get("album", {}).get("wiki", {}).get("summary")
                if description:
                    # Replace HTML anchor tag with Discord markdown link
                    if '<a href="' in description:
                        start_link = description.find('<a href="') + 9
                        end_link = description.find('">', start_link)
                        url = description[start_link:end_link]
                        start_text = end_link + 2
                        end_text = description.find('</a>', start_text)
                        text = description[start_text:end_text]
                        description = description[:start_link-9] + f"[{text}]({url})" + description[end_text+4:]
                    return description
            return None

# Function to normalize artist names by removing spaces and converting to lowercase
def normalize_artist_name(artist: str) -> str:
    return artist.lower().replace(" ", "")

# Function to load albums for a given artist from the JSON file
def load_albums(artist: str):
    albums_path = Path(__file__).parent.parent / "albums"
    artist_to_filename = {normalize_artist_name(file.stem): file.stem for file in albums_path.glob("*.json")}
    artist_key = normalize_artist_name(artist)
    file_path = albums_path / f"{artist_to_filename.get(artist_key, artist_key)}.json"
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["artist"], data["albums"] 
    return None, [] 

# Function to get a list of all artists from the JSON files
def get_artists():
    albums_path = Path(__file__).parent.parent / "albums"
    artists = []
    for file in albums_path.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            artists.append(data["artist"])
    return artists

# Define the /randomalbum command
def load(bot):
    @bot.command()
    @lightbulb.option("artist", "The artist to get a random album from", required=True, autocomplete=True)
    @lightbulb.command("randomalbum", "Get a random album from a specified artist!")
    @lightbulb.implements(lightbulb.SlashCommand)
    async def random_album(ctx: lightbulb.Context) -> None:
        artist = ctx.options.artist
        artist_name, albums = load_albums(artist)
        if albums:
            album = random.choice(albums)
            description = await fetch_album_description(artist_name, album)
            if description:
                await ctx.respond(f"🎵{artist_name}: {album}🎵\n-# {description}")
            else:
                await ctx.respond(f"🎵{artist_name}: {album}🎵")
        else:
            await ctx.respond(f"No albums found for {ctx.options.artist}.")
        
    # Handle autocomplete interactions for the /randomalbum command
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