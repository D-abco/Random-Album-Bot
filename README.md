# Random Album Bot

Random Album Bot is a Discord bot that fetches a random album from a specified artist and provides a description of the album using the Last.fm API.

## Features

- Fetch a random album from a specified artist.
- Provide a description of the album using the Last.fm API.

## Prerequisites

- Python 3.7+
- A Discord bot token
- A Last.fm API key (optional)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/randomalbumbot.git
    cd randomalbumbot
    ```

2. Create a virtual environment and activate it:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a [.env](http://_vscodecontentref_/0) file in the project directory and add your Discord bot token and Last.fm API key:

    ```env
    BOT_TOKEN=your_discord_bot_token
    LASTFM_API_KEY=your_lastfm_api_key #optional
    ```

5. Create a directory named [albums](http://_vscodecontentref_/1) in the project directory and add JSON files for each artist. Each JSON file should be named after the artist and contain the following structure:

    ```json
    {
        "artist": "Artist Name",
        "albums": ["Album 1", "Album 2", "Album 3"]
    }
    ```

## Usage

1. Run the bot:

    ```sh
    python main.py
    ```

2. Invite the bot to your Discord server using the OAuth2 URL with the `applications.commands` and `bot` scopes.

3. Use the `/randomalbum` command in your Discord server to fetch a random album from a specified artist.

## Example

```sh
/randomalbum artist: "King Gizzard & The Lizard Wizard"