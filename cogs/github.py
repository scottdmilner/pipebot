from disnake.ext import commands
import disnake
from dotenv import load_dotenv
from enum import Enum
from pprint import pprint
from github import Github
from github import Auth
import os

load_dotenv()


class PipeCategory(str, Enum):
    Discord = "discord"
    Farm = "renderfarm"
    Houdini = "houdini"
    Maya = "maya"
    Nuke = "nuke"
    Other = "other"
    ShotGrid = "shotgrid"
    Substance = "substance"
    Unreal = "unreal"


class GithubCmds(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        authtoken = Auth.Token(os.getenv("GITHUB_ACCESS_TOKEN"))
        self.g = Github(auth=authtoken)
        self.repo = self.g.get_repo(os.getenv("GITHUB_REPO"))

    @commands.slash_command()
    async def bug_report(
        self,
        inter: disnake.ApplicationCommandInteraction,
        category: PipeCategory,
        description: str,
        image1: disnake.Attachment = None,
        image2: disnake.Attachment = None,
    ) -> None:
        """
        Report a bug to the pipeline team. Please be detailed!

        Parameters
        ----------
        category: What are you having an issue with?
        description: A detailed description of the issue
        image1: Attach an image of the issue (optional)
        image2: Attach an image of the issue (optional)
        """
        pprint(inter.data)
        await inter.response.send_message("OK", ephemeral=True)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Github(bot))
