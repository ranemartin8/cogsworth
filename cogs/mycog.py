import discord
from discord.ext import commands
import aiohttp
import asyncio
import logging
import requests
#import pandas as pd

#log = logging.getLogger("red.owner")

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycom(self):
        """This does stuff!"""
        url = 'https://sheets.googleapis.com/v4/spreadsheets/15Yj-AA3pMYKICzLporqAZTutCdT7fNA8Z3uScmM3guo/values/syn!a1:z100?majorDimension=ROWS&key=AIzaSyBugcjKbOABZEn-tBOxkj0O7j5WGyz80uA&prettyPrint=true'
        async with aiohttp.get(url) as response:
            syn = await response.json()
            #crop_syn = syn[:20]
        try:
            #cid = '102';
            keys = syn['values'][0]
            vals = syn['values']
            syn_map = {}
            dic_map = dict()
            for index, a_row in enumerate(vals):
                dic_map = dict(zip(keys, a_row[index]))
                syn_map = ",".join(dic_map)
            #cinfo = syn_map[100]
            #cval = cinfo['name']
            await self.bot.say('Result: {}'.format(dic_map1))
            #self.log('Success! {}'.format(cval))
        except:
            raise
        #    await self.bot.say('SAD!')
        #    self.log('{}'.format(crop_syn))
def setup(bot):
    bot.add_cog(Mycog(bot))
