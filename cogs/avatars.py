import os
from disnake.ext import commands, tasks
from random import choice


class AvatarRandomizer(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.avatar_list = [
            f"profile_pics/{fn}"
            for fn in os.listdir("profile_pics")
            if not fn.startswith(".")
        ]

        self.update_avatar.start()

    @tasks.loop(hours=4)
    async def update_avatar(self) -> None:
        new_avatar = choice(self.avatar_list)
        print("updating avatar!")
        
        with open(new_avatar, "rb") as img:
            await self.bot.user.edit(avatar=img.read())

    @update_avatar.before_loop
    async def update_avatar_before_loop(self) -> None:
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot) -> None:
    bot.add_cog(AvatarRandomizer(bot))
