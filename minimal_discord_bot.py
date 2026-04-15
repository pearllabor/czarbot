import discord
import discord_values

# secret credential that logs in the bot, should be kept private and not shared
TOKEN = discord_values.get_token()

# id that tells the bot which channel to read and send messages in, should be kept private and not shared
CHANNEL_ID_GENERAL = discord_values.get_channel_id()['General']  # replace with your channel ID
CHANNEL_ID_ANNOUNCEMENTS = discord_values.get_channel_id()['Announcements']  # replace with your channel ID

# tells the bot what to pay attention to. In this case, we want to read message content, so we need to enable that intent.
intents = discord.Intents.default()
intents.message_content = True

# sets up communication with the Discord API using the provided intents
client = discord.Client(intents=intents)


@client.event

# this function runs when the bot has successfully connected to Discord and is ready to operate
async def on_ready():
    print(f"Logged in as {client.user}")

    channel = await client.fetch_channel(CHANNEL_ID_ANNOUNCEMENTS)
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

    if message.channel.id == CHANNEL_ID_GENERAL:
        print("New live message received:")
        print(f"[{message.channel}] {message.author}: {message.content}")
    
    # Example: respond to a command

    if message.content == "!ping":
        await send_message(message.channel, "pong!")

    if message.author.id == discord_values.get_member_id()['Joey']:
        await send_message(message.channel, "did I ask?")

client.run(TOKEN)

def labor_preferences():
    # ========== LABOR PREFERENCES ========== #
    preferences = workbook.read_sheet(address, "Labor Preferences!A3:AB200")
    preferences_dict = dict.fromkeys(names, [])
    # turn preferences into a dataframe
    preferences_df = pd.DataFrame(preferences[1:], columns=preferences[0])
    # remove certain columns that we don't need
    preferences_df = preferences_df.drop(columns=['Hours', 'Name Update', 'Notes', 'Medical Conditions', 'Context'])
    # populate preferences_dict with each person's preferences, only keeping the most recent form for each person
    for name in names:
        preferences_dict[name] = dict.fromkeys(preferences_df.columns, 0)
        for index, row in preferences_df.iterrows():
            if row['Name'] == name:
                # only keep the most recent form for each person, so overwrite the previous one if there are multiple forms
                if preferences_dict[name]['Time/Exempt'] == 0:
                    for column in preferences_df.columns[2:]:
                        preferences_dict[name][column] = row[column]
                elif datetime.strptime(row['Time/Exempt'], "%m/%d/%Y %H:%M:%S") > datetime.strptime(preferences_dict[name]['Time/Exempt'], "%m/%d/%Y %H:%M:%S"):
                    for column in preferences_df.columns[2:]:
                        preferences_dict[name][column] = row[column]

