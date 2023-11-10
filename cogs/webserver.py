import disnake
import hmac
import json
import os
from aiohttp import web
from disnake.ext import commands, tasks
from hashlib import sha1
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()


class Webserver(commands.Cog):
    # see https://stackoverflow.com/a/62481294
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.webserver_port = os.getenv("LISTEN_PORT")
        self.app = web.Application()
        routes = web.RouteTableDef()

        self.web_server.start()

        @routes.get("/")
        async def welcome(request: web.Request) -> web.Response:
            return web.Response(body="", status=400)

        @routes.post("/shotgrid")
        async def shotgrid(request: web.Request) -> web.Response:
            raw = await request.read()
            hashcheck = (
                "sha1="
                + hmac.new(os.getenv("SHOTGRID_SECRET").encode(), raw, sha1).hexdigest()
            )
            if hashcheck != request.headers["x-sg-signature"]:
                print("Error: hashes do not match")
                return web.Response(body="", status=401)

            data = await request.json()
            pprint(data)
            await self.testing_channel.send("```json\n" + json.dumps(data) + "\n```")
            return web.Response(status=200)

        self.app.add_routes(routes)

    @tasks.loop()
    async def web_server(self) -> None:
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, host="0.0.0.0", port=self.webserver_port)
        await site.start()

    @web_server.before_loop
    async def web_server_before_loop(self) -> None:
        await self.bot.wait_until_ready()

        # for some reason `get_channel` doesn't work but `fetch_channel` does
        testing_channel = await self.bot.fetch_channel(os.getenv("TESTING_CHANNEL_ID"))
        if not isinstance(testing_channel, disnake.TextChannel):
            raise TypeError("Channel is invalid")

        self.testing_channel = testing_channel


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Webserver(bot))
