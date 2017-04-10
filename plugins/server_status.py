import discord
from discord.ext import commands
from util import byond, setup_file
from util.checks import server_admin

from multiprocessing import Process
import asyncio

class ServerStatus:
    def __init__(self, bot):
        self.bot = bot
        self.servers = setup_file["servers"]
        self.byond = byond.Byond()
        self.allowed_channels = setup_file["allowed_channels"]
        self.monitoring = False
    
    @commands.command(name='start', pass_context=True)
    @commands.check(server_admin)
    async def monitor(self, context):
        if not self.monitoring:
            if context.message.channel.id in self.allowed_channels:
                self.monitoring = True
                await self.start_monitoring(context)
                
    
    async def start_monitoring(self, context):
        for server in self.servers:
            info = self.get_server_info(server)
            status = self.build_status(info)
            msg = await self.bot.say(embed=status)
            server['message'] = msg
            server['old_info'] = info
        print('Started monitoring.')
        while self.monitoring:
            for server in self.servers:
                new_info = self.get_server_info(server)
                if(new_info != server['old_info']):
                    new_status = self.build_status(new_info)
                    print('im here!')
                    await self.bot.edit_message(server['message'], embed=new_status)
            await asyncio.sleep(5)
            
    @commands.command(name='stop')
    @commands.check(server_admin)
    async def stop_monitoring(self):
        self.monitoring = False
        await self.bot.say('Stopped monitoring')
        print('Stopped monitoring')
    
    def get_server_info(self, server):
        try:
            status = self.byond.request_topic(server['domain'], server['port'], "status")
            server_url = self.construct_server_url(server['domain'], server['port'])
            info = {'players': status['players'], 'round_duration': status["roundduration"], 'server_name': server['name'], 'admins': status["admins"], 'address': server_url}
            
        except discord.HTTPException:
            info = "{0} is offline.".format(server["name"])
            
        except TypeError:
            info = "{0} is offline".format(server["name"])
        return info
    
    def build_status(self, info):
        emb = discord.Embed()
        if type(info) is dict:
            emb.add_field(name='Server status', value='{0} is online!'.format(info['server_name']), inline=False)
            emb.add_field(name='Players', value=info["players"])
            emb.add_field(name='Admins', value=info["admins"])
            emb.add_field(name='Server address', value=info['address'], inline=False)
        else:
            emb.add_field(name='Server status', value=info)
        return emb
        
        
    def construct_server_url(self, domain, port):
        return "byond://{0}:{1}".format(domain, port)

def setup(bot):
    bot.add_cog(ServerStatus(bot))