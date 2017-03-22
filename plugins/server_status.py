import discord
from discord.ext import commands
from util import byond, setup_file
from util.checks import server_admin

from multiprocessing import Process
import asyncio

class ServerStatus:
    def __init__(self, bot):
        self.bot = bot
        self.server = setup_file["server"]
        self.byond = byond.Byond()
        self.monitoring = False
    
    @commands.command(name='info')
    async def server_info(self):
        info = self.get_server_info()
        message = self.build_status(info)
        await self.bot.say(embed=message)
    
    @commands.command(name='start', pass_context=True)
    @commands.check(server_admin)
    async def monitor(self, context):
        if not self.monitoring:
            if context.message.channel.id == "288013065499443200" or context.message.channel.id == "286943853033029632":
                self.monitoring = True
                await self.start_monitoring(context)
                
    
    async def start_monitoring(self, context):
        msg = await self.bot.say(embed=self.build_status(self.get_server_info()))
        print('Started monitoring.')
        await self.bot.say('Started monitoring')
        while self.monitoring:
            new_info = self.build_status(self.get_server_info())
            await self.bot.edit_message(msg, embed=new_info)
            await asyncio.sleep(1)
            
    @commands.command(name='stop')
    @commands.check(server_admin)
    async def stop_monitoring(self):
        self.monitoring = False
        await self.bot.say('Stopped monitoring')
        print('Stopped monitoring')
    
    def get_server_info(self):
        try:
            status = self.byond.request_topic(self.server['domain'], self.server['port'], "status")
            info = {'players': status['players'], 'round_duration': status["roundduration"], 'admins': status["admins"]}
        except discord.HTTPException:
            info = "Server is offline."
        return info
    
    def build_status(self, info):
        emb = discord.Embed()
        if type(info) is dict:
            emb.add_field(name='Server status', value='Server is online!', inline=False)
            emb.add_field(name='Players', value=info["players"])
            emb.add_field(name='Admins', value=info["admins"])
            emb.add_field(name='Server address', value=self.construct_server_url(), inline=False)
        else:
            emb.add_field(name='Server status', value=info)
        
        return emb
        
    def construct_server_url(self):
        return "byond://{0}:{1}".format(self.server['domain'], self.server['port'])

def setup(bot):
    bot.add_cog(ServerStatus(bot))