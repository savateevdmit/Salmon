import asyncio
from config import settings
from discord.ext import commands
from discord.ext.audiorec import NativeVoiceClient
bot = commands.Bot(command_prefix=settings['prefix'])


def voice(ctx):
    async def main(ctx):
        channel: discord.VoiceChannel = ctx.author.voice.channel  # type: ignore
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect(cls=NativeVoiceClient)
        while True:
            ctx.voice_client.record(lambda e: print(f"Exception: {e}"))
            await ctx.send(f'Start Recording')
            await asyncio.sleep(10)
            wav_bytes = await ctx.voice_client.stop_record()
            await ctx.send(f'Stop Recording')
            f = open("rec.txt")
            lines = f.readlines()
            if 'быки' or 'коровы' in lines[0]:
                await ctx.invoke(bot.get_command('bc'))

    asyncio.get_running_loop().create_task(main(ctx))
