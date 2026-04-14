import discord
import discord_values

# secret credential that logs in the bot, should be kept private and not shared
TOKEN = discord_values.get_token()

# id that tells the bot which channel to read and send messages in, should be kept private and not shared
CHANNEL_ID = discord_values.get_channel_id()['General']  # replace with your channel ID

# tells the bot what to pay attention to. In this case, we want to read message content, so we need to enable that intent.
intents = discord.Intents.default()
intents.message_content = True

# sets up communication with the Discord API using the provided intents
client = discord.Client(intents=intents)


@client.event

# this function runs when the bot has successfully connected to Discord and is ready to operate
async def on_ready():
    print(f"Logged in as {client.user}")

    channel = await client.fetch_channel(CHANNEL_ID)
    print(f"Found channel: {channel}")

    found_message = False
    async for message in channel.history(limit=5):
        found_message = True
        print("History message:")
        print(f"[{channel}] {message.author}: {message.content}")

    if not found_message:
        print("No history messages were returned.")

# --- function to send a message ---
async def send_message(channel, text: str):
    await channel.send(text)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id == CHANNEL_ID:
        print("New live message received:")
        print(f"[{message.channel}] {message.author}: {message.content}")
    
    # Example: respond to a command

    if message.content == "!ping":
        await send_message(message.channel, "pong!")

    # if message.author.id == 753267835979038883:
    #     await send_message(message.channel, "huh?")

client.run(TOKEN)