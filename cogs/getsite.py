import discord
from discord.ext import commands
import aiohttp
import asyncio
import logging
import requests
import re
import pprint


class anothercog:
    """This command translates Hooks JS synergies file into a readable json file"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def syn(self,ctx):
        """stuff"""
        url = 'https://raw.githubusercontent.com/hook/champions/master/src/data/synergies.js'
        async with aiohttp.get(url) as response:
            hook = await response.text()# hlen = len(hook)
            fm_str = '...fromId('
            to_end = '].map((synergy'
            find_start = hook.find(fm_str)
            find_end = hook.find(to_end)
            hk_slice = hook[find_start:find_end].split('...fromId') #slice out all syns & split into blocks by "from" champion
            c_all = {}
            for champblock in hk_slice:
                syn_blk = champblock.split('...fromStars') #separate into lines by "to" champion
                i = 0
                synrows = {}
                ch_dict = {}
                for champline in syn_blk:

                    pattern_fromchamp = re.compile(r'(?<=CHAMPION\.)(\w+)')
                    pattern_tochamp = re.compile(r'\(\d+,\s\d')

                    if pattern_tochamp.match(champline):
                        stars = re.search(r'(\d+),\s(\d+)',champline)
                        effect = re.search(r'(?<=EFFECT\.)(\w+)',champline)
                        ch_count = champline.count('CHAMPION')
                        if ch_count > 1:
                            cnt = 0
                            while cnt < ch_count:
                                champname = re.findall(r'(?<=CHAMPION\.)\w+',champline)
                                tochamp = [champname[cnt],effect.group(0),stars.group(1),stars.group(2)]
                                synrows.update({"{}".format(i) : tochamp})
                                cnt += 1
                                i += 1
                        else:
                            champname = re.search(r'(?<=CHAMPION\.)(\w+)',champline)
                            tochamp = [champname.group(0),effect.group(0),stars.group(1),stars.group(2)]
                            synrows.update({"{}".format(i) : tochamp})
                            i += 1
                    elif pattern_fromchamp.search(champline):
                        frmchamp = champline.strip()
                        fchamp = re.search(r'(?<=CHAMPION\.)(\w+)',frmchamp)
                        fromchamp = fchamp.group(0)
                        ch_dict.update({fromchamp : [synrows]})
                c_all.update(ch_dict)


            if find_start > 0:
                try:
                    text_file = open("Synergies.json", "w")
                    str_all = str(c_all).replace('\'',"\"")
                #    pretty_call = pprint(str_all)
                    text_file.write(str_all)
                #    text_file.write(pretty_call.replace('\'',"\""))
                    text_file.close()
                    await self.bot.send_file(ctx.message.channel,"Synergies.json")
                except:
                    raise
            else:
                await self.bot.say("nada")

def setup(bot):
    bot.add_cog(anothercog(bot))
