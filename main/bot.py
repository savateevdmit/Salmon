try:
    import os
    os.system('pip install SpeechRecognition')
    os.system('pip3 install PyAudio-0.2.11-cp38-cp38-win32.whl')
except Exception:
    pass

import discord
from discord.ext import commands
from config import settings
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
import wave  # создание и чтение аудиофайлов формата wav
import json  # работа с json-файлами и json-строками
import os  # работа с файловой системой
from discord.ext.commands import Bot
import discord.ext
import discord.ext.commands

from discord.utils import get
a = False
client = Bot(command_prefix="8")
recognizer = speech_recognition.Recognizer()
microphone = speech_recognition.Microphone()





def record_and_recognize_audio(*args: tuple):
    with microphone:
        recognized_data = ""
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            audio = recognizer.listen(microphone, 6, 6)
            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())
        except speech_recognition.WaitTimeoutError:
            return
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()
        except speech_recognition.UnknownValueError:
            pass
        except speech_recognition.RequestError:
            print("Trying to use offline recognition...")

        return recognized_data


bot = commands.Bot(command_prefix = settings['prefix'])

@bot.command(aliases = ['start']) # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
async def hello(ctx): # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author # Объявляем переменную author и записываем туда информацию об авторе.

    while True:

        # старт записи речи с последующим выводом распознанной речи
        # и удалением записанного в микрофон аудио
        try:
            channel = ctx.author
            voice_input = record_and_recognize_audio()
            os.remove("microphone-results.wav")
            if voice_input == 'стоп':
                break
            elif 'иди' in voice_input and 'лосось' in voice_input:
                cha = ctx.author.voice.channel
                if cha != None:
                    await cha.connect()
                    continue
                continue
            elif 'уйди' in voice_input and 'лосось' in voice_input and channel.voice != None:
                await ctx.voice_client.disconnect()
                continue
            await ctx.send(voice_input)

        except:
            pass

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel

    await channel.connect()
@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена
