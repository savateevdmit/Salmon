# try:
#     import os
#     os.system('pip install SpeechRecognition')
#     os.system('python PyAudio-0.2.11/setup.py install')
# except Exception:
#     pass

from discord.ext import commands

from config import settings
from voice import voicee

a = False

bot = commands.Bot(command_prefix=settings['prefix'])


#####################################################
# ТУТ ГОЛОСОВОЕ УПРАВЛЕНИЕ:
# @bot.command()  # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
# async def start(ctx):  # Создаём функцию и передаём аргумент ctx.
#     voicee(ctx)
######################################################


@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


bot.run(settings['token'])  # Обращаемся к словарю settings с ключом token, для получения токена
