import discord
from discord.ext import commands
from discord.ui import Button, View
from AI_Handler import generate_response, clear_user_conversation
import asyncio
import os



# Loading the Bot Token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)


class ClearButton(Button):
    async def callback(self, interaction):
        await interaction.response.send_message("Chat Cleared For Current User.")
        clear_user_conversation(str(interaction.user.id))


@bot.event
async def on_ready():
    print(f"Bot Logged in as {bot.user.name} (ID: {bot.user.id})")

    # Startup message on the first text channel the bot has access to
    for channel in bot.get_all_channels():
        if isinstance(channel, discord.TextChannel):
            await channel.send("Bot initialized, ready to assist you!")
            break


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if message.content.startswith(f"<@{bot.user.id}>") or message.content.startswith(f"<@!{bot.user.id}>"):
        user_input = message.content.split(" ", 1)[1].strip()

        if not user_input:
            return

        if user_input == "[start new chat]":
            clear_user_conversation(str(message.author.id))
            await message.reply("Conversation history cleared. You can start a new chat.")
            return

        async with message.channel.typing():
            # Adds a clear chat button
            clear_button = ClearButton(label="Clear Chat", style=discord.ButtonStyle.danger)
            view = View(timeout=180)
            view.add_item(clear_button)

            # Generates the response from the API
            response = generate_response(str(message.author.id), user_input)
            messages = response.choices[0].message.content.strip()

            if messages:
                await message.reply(messages, view=view)
                await asyncio.sleep(2)
            else:
                await message.reply("I couldn't generate a response. Please try again.")

bot.run(BOT_TOKEN)
