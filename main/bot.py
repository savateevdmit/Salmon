import random

import aiohttp
import discord
from discord.ext import commands

from bulls_and_cows import bulls_and_cows
from config import settings

try:
    import os

    os.system('pip install SpeechRecognition')
except:
    pass

a = False
url = 'https://dtf.ru/kek/entries/new'
cycles = dict(game=True)
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
bot = commands.Bot(command_prefix=settings['prefix'])
bot.remove_command('help')


#####################################################
# ТУТ ГОЛОСОВОЕ УПРАВЛЕНИЕ:
# @bot.command()  # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
# async def start(ctx):  # Создаём функцию и передаём аргумент ctx.
#     voicee(ctx)
######################################################

@bot.command()
async def stop_game(ctx):
    print('jn')
    cycles["game"] = False


@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command()
async def meme(ctx):
    embed = discord.Embed(title="", colour=0xfff70a)

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)


@bot.command()
async def info(ctx, member: discord.Member = None):
    embed = discord.Embed(color=0xff781f)
    embed.set_author(name=f'{member}', icon_url=f'{member.avatar_url}')
    embed.add_field(name='Дата создания:', value=f'{member.created_at}', inline=False)
    embed.add_field(name='Высшая роль:', value=f'{member.top_role.mention}', inline=False)
    embed.set_image(url=f'{member.avatar_url}')

    await ctx.send(embed=embed)

    await ctx.channel.send('\u200b')


@bot.command()
async def bc(ctx):
    embed = discord.Embed(title='❗Правила❗', color=0x4fde02)

    embed.add_field(name='🐄 Быки и коровы 🐂',
                    value='🔰 Бот загадывает число, состоящие из четырёх разных цифр. Задача угадать загаданное число. '
                          'Отправляйте боту четырёхзначные числа. Результат каждого хода оценивается числом **БЫКОВ** '
                          'и **КОРОВ**. Если совпадает цифра и её позиция, то это **БЫК**. Если цифра совпадает, '
                          'но её позиция нет, то это **КОРОВА**.',
                    inline=False)
    embed.add_field(name='\u200b',
                    value='**♻Игра уже началась, отправляйте числа!♻**',
                    inline=False)
    embed.set_image(
        url='https://lh3.googleusercontent.com/6oHWaM1Z9NELHkkO7VKjwrzkAlG-rTyHGhWJcCnxWHhfJhubkinI_PfnkKS-7bC3t_k=h500')
    await ctx.send(embed=embed)
    number = random.sample(range(1, 10), 4)
    print(number)

    while True:
        message = await bot.wait_for('message', check=bc)
        if message.content == '!stop game':
            await ctx.send(f'❌{message.author.mention}, игра остановлена!❌')
            return
        else:
            count = 0
            id = message.author.id
            if message.author.discriminator != '7918':
                if len(message.content) == 4:
                    for i in message.content:
                        if i in numbers:
                            count += 1
                    if count == 4:
                        if len(bulls_and_cows(int(message.content), number)) > 25:
                            embed = discord.Embed(title='🐄 Быки и коровы 🐂', color=0xf25a07)
                            embed.add_field(name='\u200b',
                                            value='😥' + f'<@!{id}>' + f'**, {bulls_and_cows(int(message.content), number)}**',
                                            inline=False)
                            embed.set_footer(text='Продолжайте!')
                            await message.channel.send(embed=embed)
                        else:
                            embed = discord.Embed(title='🐄 Быки и коровы 🐂', color=0x4fde02)
                            embed.add_field(name='\u200b',
                                            value='🎉' + f'<@!{id}>' + f'**, {bulls_and_cows(int(message.content), number)}**',
                                            inline=False)
                            count += 1
                            await message.channel.send(embed=embed)
                            # await ctx.send('stoped')
                            return


@bot.command()
async def help(ctx):
    embed = discord.Embed(color=0x08e7f7)

    embed.set_author(name='📒 Справкa')

    embed.add_field(name='`!play`', value='Проигрывание музыки', inline=True)
    embed.add_field(name='`!stop`', value='Остановка музыки', inline=True)
    embed.add_field(name='`!join`', value='Присоединение бота к голосовому каналу', inline=True)
    embed.add_field(name='`!bc`', value='Запуск игры "Быки и коровы"', inline=True)
    embed.add_field(name='`!meme`', value='Показ рандомного мема из интернета', inline=True)
    embed.add_field(name='`!logo`', value='Угадывание названия компании по логотипу на время', inline=True)
    embed.add_field(name='`!stop game`', value='Остановка игры', inline=True)

    embed.add_field(name='\u200b',
                    value='Более подробную информацию ищите здесь - https://clck.ru/eAsPG',
                    inline=False)
    # embed.add_field(name="\u200B", value='<https://github.com/savateevdmit/Salmon.git>', inline=False)
    await ctx.send(embed=embed)


bot.run(settings['token'])  # Обращаемся к словарю settings с ключом token, для получения токена
