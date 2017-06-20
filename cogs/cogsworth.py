import discord
from discord.ext import commands
import aiohttp
import asyncio
import logging
import requests
import re
import pprint
import json

class anothercog:
    """This is a cog."""

    def __init__(self, bot):
        self.bot = bot
    @commands.command(pass_context=True)
    async def findsyn(self,ctx, *, champs: str):
        """finds syneries"""
        #print(len(champs))
        if len(champs) > 0:
            with open('data.json') as data_file:
                data = json.load(Synergies.json)
            import os
            dir_path = os.path.dirname(os.path.realpath(__file__))
            pprint(data)
            url = 'https://raw.githubusercontent.com/ranemartin8/cogsworth/master/Synergies.json'
            async with aiohttp.get(url) as response:
                synergies = await response.json()
            try:
                champs_list = champs.split(",")
                #syn_text = ''
                #out_text = ''
                for champ in champs_list:
                    if synergies[champ]:
                        tochampions = synergies[champ][0]
                        i = 0
                        for tochamp in tochampions:
                            idx = "{}".format(i)
                            c_line = tochampions[idx]
                            c_name = c_line[0]
                            c_syn = c_line[1]
                            if champ == c_name:
                                #print(c_name)
                                tochamp_name = c_name
                                tochamp_syn = c_syn
                                #out_text = 'this'
                            out_text = ' ' + 'Champ: {} - Synergy: {} '.format(tochamp_name,tochamp_syn)
                            i += 1
                    else:
                        await self.bot.say("no synergies found")
                print(out_text)
                await self.bot.say("Result: {}".format(out_text))

            except:
                raise
        else:
            await self.bot.say("No champs provided.")

    @commands.command(pass_context=True)
    async def syn(self,ctx):
        """This command translates Hooks JS synergies file into a readable json file"""
        url = 'https://raw.githubusercontent.com/hook/champions/master/src/data/synergies.js'
        async with aiohttp.get(url) as response:
            hook = await response.text()
            find_start = hook.find('...fromId(') #finds first occurance of "...fromId"
            find_end = hook.find('].map((synergy') #finds first occurance of "].map((synergy"
            hk_slice = hook[find_start:find_end].split('...fromId') #slice out all syns & split into blocks by "from" champion
            c_all = {} #define output dictionary
            for champblock in hk_slice:
                syn_blk = champblock.split('...fromStars') #separate into rows by "to" champion
                i = 0
                synrows = {} #define row dictionary
                ch_dict = {} #define championblock dictionary
                for champline in syn_blk:
                    pattern_fromchamp = re.compile(r'(?<=CHAMPION\.)(\w+)') #regex matching text immediately after "CHAMPION."
                    pattern_tochamp = re.compile(r'\(\d+,\s\d') #regex matching "(#, #..."
                    if pattern_tochamp.match(champline):  #if the line starts with "(#, #..." aka a 'toChamp' line
                        stars = re.search(r'(\d+),\s(\d+)',champline) #find numbers (star values)
                        effect = re.search(r'(?<=EFFECT\.)(\w+)',champline) #find effect values
                        ch_count = champline.count('CHAMPION') #count # of "CHAMPION" occurances
                        if ch_count > 1: #if there are more than 1 champions listed in this line, give each it's own line
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
                            synrows.update({"{}".format(i) : tochamp}) #set contains of synergy row
                            i += 1
                    elif pattern_fromchamp.search(champline): #if the line contains "CHAMPION.#####"
                        frmchamp = champline.strip()
                        fchamp = re.search(r'(?<=CHAMPION\.)(\w+)',frmchamp)
                        fromchamp = fchamp.group(0)
                        ch_dict.update({fromchamp : [synrows]}) #set contents of champion block with champ name and syn rows
                c_all.update(ch_dict) #append all champion blocks to final output dictionary
            if find_start > 0:
                try:
                    text_file = open("Synergies.json", "w")
                    str_all = str(c_all).replace('\'',"\"") #convert to string. alnd json doesn't like single quotes
                    text_file.write(str_all) #overwrites existing content
                    text_file.close()
                    await self.bot.send_file(ctx.message.channel,"Synergies.json")
                except:
                    raise #idk...
            else:
                await self.bot.say("nada")

def setup(bot):
    bot.add_cog(anothercog(bot))
