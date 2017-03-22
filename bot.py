import discord
from discord.ext import commands
from util import setup_file

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