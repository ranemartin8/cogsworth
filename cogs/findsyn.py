import discord
from discord.ext import commands
import aiohttp
import asyncio
import logging
import requests
import re
import pprint


class anothercog:
    """This is a cog."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def findsynn(self,ctx):
        """This command translates Hooks JS synergies file into a readable json file"""
        await self.bot.say("this is it.")

def setup(bot):
    bot.add_cog(anothercog(bot))
