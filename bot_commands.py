import  discord
from    discord.ext import commands
from    MusicCommands import music
import  asyncio


class commands(commands.Cog, music):

  def __init__(self, client):
    self.client = client
    super().__init__()

  @commands.command(aliases = ['join'])
  async def j(self, ctx):
    await music.join(self, ctx) # don't ask me why I have to pass self here and in the other commands I have no idea but it works

  @commands.command(aliases = ['disconnect'])
  async def dc(self, ctx):
    await music.disconnect(self, ctx)

  @commands.command(aliases = ['play'])
  async def p(self, ctx, *, url):    # * here to allow multi-word argument
    await music.play(self, ctx, url)
 
  @commands.command(aliases = ['playing', 'nowplaying', 'currentsong'])
  async def np(self, ctx):
    await music.nowplaying(self, ctx)

  @commands.command(aliases = ['q'])
  async def queue(self, ctx):
    await music.queue(self, ctx)

  @commands.command()
  async def pause(self, ctx):
    await music.pause(self, ctx)

  @commands.command(aliases = ['r'])
  async def resume(self, ctx):
    await music.resume(self, ctx)

  @commands.command()
  async def stop(self, ctx):
    await music.stop(self, ctx)

  @commands.command(aliases = ['skip'])
  async def s(self, ctx):
    await music.skip(self, ctx)

  @commands.command(aliases = ['help', 'Help', 'github'])
  async def commands(self, ctx):
    await music.helpembed(self, ctx)

async def setup(client):
  await client.add_cog(commands(client))
