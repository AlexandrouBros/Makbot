import  discord
from    discord.ext import commands
import  youtube_dl
from    Queue import Queue
import  asyncio

skip = False  # boolean true when skipping (not implemented yet)
adding_firstsong = False # boolean true when bot is fetching an initial song to play, i.e a song not from the queue
creating_queue = False # boolean true when adding a song to an empty queue

FFMPEG_OPTIONS = {
      'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
      'options': '-vn'
    }

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}


async def create_qdict(video):
    audioURL = video['formats'][0]['url'] #store audio source URL
    title = video['title'] #store video title
    thumbnail = video['thumbnail'] #store url of thumbnail
    source = await discord.FFmpegOpusAudio.from_probe(audioURL, **FFMPEG_OPTIONS)
    song = {
    "title": title,
    "thumbnail": thumbnail,
    "audiosource": source
    }
    return song

class music():
  
  def __init__(self):
    self.queue = Queue()
    print('music_init')

  async def join(self, ctx):
    if ctx.author.voice is None:
      await ctx.send("No voice channel detected")
    vc = ctx.author.voice.channel
    if ctx.voice_client is None:
      await vc.connect()
    else:
      await ctx.voice_client.move_to(vc)


  async def disconnect(self, ctx):
    self.queue.clearall()
    await ctx.voice_client.disconnect()


  async def play(self, ctx, url):
    global adding_firstsong
    global creating_queue

    await self.join(ctx)

    vc = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      try:  
        video = ydl.extract_info(url, download=False) #extract info if user input is a URL
      except:
        video = ydl.extract_info(f"ytsearch1:{url}", download=False)['entries'][0] #search youtube for user input and extract info from first search result
      if vc.is_playing() or adding_firstsong == True:
            if self.queue.length() == 0:
                creating_queue = True
            song = await create_qdict(video)
            self.queue.add(song)
            qlen = self.queue.length()
            await self.addqueue_embed(ctx, song['title'], song['thumbnail'], qlen)
            creating_queue = False
      else:
            adding_firstsong = True
            loop = asyncio.get_event_loop() # Store event loop in variable
            song =  await create_qdict(video) # Create dictionary to be stored in the queue
            self.queue.add(song) # Store dict in queue
            await self.npembed(ctx, song['title'], song['thumbnail']) #display now playing msg using npembed function
            vc.play(song['audiosource'], after = lambda x=0: self.playnext(ctx, loop))
            adding_firstsong = False


  async def nowplaying(self, ctx):
    song = self.queue.curSong()
    await self.npembed(ctx, song['title'], song['thumbnail'])


  async def queue(self, ctx):  # x * 10 + 1 for upper limit, (x-1)*10 + 1 for lower limit
    kleinblue = 0x002199
    if not self.queue.isEmpty():
        em = discord.Embed(title="Queue", color=kleinblue)
        for i in range(1, 11):
            if i <= self.queue.length():
                song = self.queue.returnSong(i)
                em.add_field(name = str(i) + ".", value = song['title'], inline=False)
    else: em = discord.Embed(title="No songs enqueued", color=kleinblue)
    await ctx.send(embed = em)


  async def clear(self, ctx):
    kleinblue = 0x002199
    if not self.queue.isEmpty():
        em = discord.Embed(title="Queue cleared", color=kleinblue)
        self.queue.clear()
    else: em = discord.Embed(title="Queue already empty", color=kleinblue)
    await ctx.send(embed = em)


  async def pause(self, ctx):
    vc = ctx.voice_client
    if vc.is_playing() and not vc.is_paused():
        ctx.voice_client.pause()
        em = discord.Embed(title="Paused ⏸", color=0xff2c2c)
        await ctx.send(embed=em)


  async def resume(self, ctx):
    vc = ctx.voice_client
    if vc.is_paused():
        vc.resume()
        em = discord.Embed(title="Resumed ▶", colour=0xff2c2c)
        await ctx.send(embed=em)


  async def stop(self, ctx):
    self.queue.clearall()
    ctx.voice_client.stop()
    await ctx.send("Stopping playback")


  async def skip(self, ctx):
    global creating_queue

    while(creating_queue):
        await asyncio.sleep(0.5)
    ctx.voice_client.stop()


  def playnext(self, ctx, loop):
    print('playnext')
    vc = ctx.voice_client
    song = self.queue.skip(ctx)
    self.playnext_embed(ctx, loop, song['title'], song['thumbnail'])
    vc.play(song['audiosource'], after = lambda x=0: self.playnext(ctx, loop))


  def playnext_embed(self, ctx, loop, title, thumbnail):
    coro = self.npembed(ctx, title, thumbnail)
    next = asyncio.run_coroutine_threadsafe(coro, loop)
    try:
         next.result(1)
    except:
        # an error happened during the coroutine
        pass


  async def npembed(self, ctx, body, thumbnail):
        green = 0x00FF00
        #file = discord.File("./images/Makbot.JPG", filename="Makbot.JPG")
        embed=discord.Embed(title="Now playing:", description=body, color=green)
        #embed.set_author(name="Makbot", icon_url="attachment://Makbot.JPG")
        embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text= "Requested by: {}".format(ctx.author.display_name))
        await ctx.send(embed=embed)
        #Commented out author code as I think looks better without
        #Also need to add file=file to ctx.send if want to implement

  async def addqueue_embed(self, ctx, body, thumbnail, position):
        pos = str(position)
        kleinblue = 0x002199
        embed=discord.Embed(title=f"Added to queue\nPosition: {pos}", description=body, color=kleinblue)
        embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text= "Requested by: {}".format(ctx.author.display_name))
        await ctx.send(embed=embed)

  async def helpembed(self, ctx):
        purple = 0xA020F0
        embed=discord.Embed(title="For info about the bot and a list of available commands, please see the bot's github:", description='https://github.com/AlexandrouBros/Makbot', url='https://github.com/AlexandrouBros/Makbot', color=purple)
        embed.set_thumbnail(url='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')
        await ctx.send(embed=embed)


#   async def skip_old(self, ctx): # skip happening twice so need to fix (skip and after) 
#     print('skip')
#     global skip
#     skip = True
#     vc = ctx.voice_client
#     song = self.queue.skip(ctx)
#     # await self.npembed(ctx, song['title'], song['thumbnail']) #display now playing msg using npembed function
#     vc.play(song['audiosource'], after = lambda x=0: self.playnext(ctx))


#   def playnextsimple(self, ctx):
#     print('playnext1')
#     global skip
#     if not skip:
#         vc = ctx.voice_client
#         song = self.queue.skip(ctx)
#         print('playnext2')
#         vc.play(song['audiosource'], after = lambda x=0: self.playnext(ctx))
#     skip = False