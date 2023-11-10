import disnake
import os
from disnake.ext import commands
from dotenv import load_dotenv

from cogs.webserver import Webserver
from cogs.github import GithubCmds

load_dotenv()

intents = disnake.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.InteractionBot(intents=intents)
bot.add_cog(Webserver(bot))
bot.add_cog(GithubCmds(bot))


@bot.event
async def on_ready() -> None:
    print(f"We have logged in as {bot.user}")


@bot.event
async def on_message(message: disnake.Message) -> None:
    if message.author == bot.user:
        return

    if "blender" in message.content.lower():
        await message.add_reaction("blender:1166462167571238922")
        await message.add_reaction("👀")


bot.run(os.getenv("CLIENT_TOKEN"))
