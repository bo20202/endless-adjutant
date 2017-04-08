import discord
import logging
import argparse
from discord.ext import commands
from util import setup_file

parser = argparse.ArgumentParser(description='Discord bot parser')
parser.add_argument('--logging', dest="logging")
args = parser.parse_args()

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=args.logging, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class Adjutant(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=setup_file["command_prefix"], description="Your friendly neighbour.")
        self.initialized = False
    
    async def on_ready(self):
        print('Logged in with {0.user.name}'.format(self))
    
    async def on_command_error(self, exception, context):
        print(exception)
        if isinstance(exception, commands.errors.CommandNotFound):
            return
        if isinstance(exception, commands.errors.CheckFailure):
            await self.send_message(context.message.channel, "You don't have the required permissions to run this command.")
            return
        
    def run(self):
        self.load_extension('plugins.server_status')
        super().run(setup_file['token'])
        
if __name__ == "__main__":

    bot = Adjutant()
    bot.run()