import logging
import os
import random
import time
from random import choice

# import PyNaCl
import aiohttp
import psycopg2
import pymorphy2
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from discord_buttons_plugin import *
from discord_components import ButtonStyle
from discord_components import ComponentsBot, Button, Select, SelectOption
from dislash import SelectOption

import discord
from bulls_and_cows import bulls_and_cows
from config import settings
from discord import FFmpegPCMAudio
from yandex_music import ClientAsync, Client

client = ClientAsync()
client.init()
client = Client(settings['token_ya'])
logging.basicConfig(level=logging.INFO)
morph = pymorphy2.MorphAnalyzer()

try:
    import os

    os.system('pip install SpeechRecognition')
    # os.system('python3 -m pip install -U discord.py[voice]')
    # os.system("pip install pynacl")

except:
    print('ошибка при установке')

song = 'song.mp3'

a = False
# path = 'main/Songs'

program_path = os.getcwd()  # путь до файла, где запускается программа
path = os.path.join(program_path, 'Songs')
DW_SONG = []
DONATE = []
DONATE1 = []
DONATE_SERVER = []
PLAY = True
DEVELOPERS = ['0891', '0603']

cycles = dict(game=True)
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
bot = ComponentsBot("!")
buttons = ButtonsClient(bot)
bot.remove_command('help')
queues = {}
music_id = []
bot_queue = []
news2 = ''

xod = True
a, b, c = 0, 0, 0
start = True
n, x = 0, 0
m = 'Q W E R T Y U I O P A S D F G H J K L Z X C V B N M q w e r t y u i o p a s d f g h j k l z x c v b n m'.split(' ')
m.sort()

con = None
try:
    con = psycopg2.connect(settings['DATABASE_URL'])
    cur2 = con.cursor()
    cur = con.cursor()
    cur2.execute('select * from donat')
    cur.execute('select * from donat_server')

    # display the PostgreSQL database server version
    result = cur2.fetchall()
    result2 = cur.fetchall()
    for i in result:
        DONATE.append(i)

    # for i in result2:
    #     DONATE_SERVER.append(i)
    con.commit()
    cur2.close()
    cur.close()
except Exception as error:
    print('Cause: {}'.format(error))

finally:
    if con is not None:
        con.close()
        print('Database connection closed.')


####################################################
# ТУТ ГОЛОСОВОЕ УПРАВЛЕНИЕ:
# @bot.command()
# async def join(ctx: commands.Context):
#     """Joins a voice channel"""
#     voice(ctx)
#####################################################


def check_queue(ctx, id):
    if queues[id] != {}:
        voice = ctx.guild.voice_client
        print(queues)
        source = queues[id].pop(0)
        bot_queue.pop(0)
        voice.play(source, after=lambda x=0: check_queue(ctx, ctx.message.guild.id))


def tr(c):
    a = {'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'Zh',
         'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
         'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Tc',
         'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ы': 'Y', 'Э': 'E', 'Ю': 'Iu', 'Я': 'Ya',
         ' ': '_', 'Ь': '', 'Ъ': ''}
    b = []
    for i in c:
        if i not in a and i.upper() in a:
            b.append(a[i.upper()].lower())
        elif i in a:
            b.append(a[i])
        else:
            b.append(i)
    return ''.join(b)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(type=discord.ActivityType.listening, name='!help'))
    # DiscordComponents(bot)


@bot.command()
async def play(ctx, *arg):
    def convert_tuple(c_tuple):
        str = ' '.join(c_tuple)
        return str

    if ctx.guild.voice_client in bot.voice_clients and ctx.voice_client.is_playing():
        await ctx.send(f'{ctx.message.author.mention}, поставил в очередь!')

        name = convert_tuple(arg)
        print(name)
        search_result = client.search(name)
        music_id.append(f'{search_result.best.result.id}:{search_result.best.result.albums[0].id}')
        song1 = f'{str(len(music_id))}.mp3'

        try:
            print(f'{search_result.best.result.id}:{search_result.best.result.albums[0].id}')
            client.tracks([music_id[-1]])[0].download(f'{path}/{song1}')
        except Exception as e:
            # await ctx.send(traceback.format_exc())
            pass

        if len(music_id) == 11:
            music_id.clear()

        voice = ctx.guild.voice_client
        source = FFmpegPCMAudio(f'{path}/{song1}')
        guild_id = ctx.message.guild.id

        bot_queue.append(f'•{search_result.best.result.title} - {search_result.best.result.artists[0].name}')

        guild_id = ctx.message.guild.id
        if guild_id in queues:
            queues[guild_id].append(source)
        else:
            queues[guild_id] = [source]

        embed = discord.Embed(title=f'{search_result.best.result.title} - {search_result.best.result.artists[0].name}',
                              color=0x8c00ff)
        embed.set_author(name=f'{search_result.best.result.artists[0].name}',
                         icon_url=f'https://{search_result.best.result.artists[0]["cover"].uri.replace("%%", "600x600")}')
        embed.add_field(name='Альбом:', value=f'{search_result.best.result.albums[0].title}', inline=False)
        embed.add_field(name='Год выпуска:', value=f'{search_result.best.result.albums[0].year}', inline=False)

        if search_result.best.result.cover_uri == None:
            embed.set_image(url=f'https://music.yandex.ru/blocks/meta/i/og-image.png')
        else:
            embed.set_image(url=f'https://{search_result.best.result.cover_uri.replace("%%", "600x600")}')

        embed.set_footer(text="Никогда не используйте ’ в запросах!")

        await buttons.send(
            embed=embed,
            channel=ctx.channel.id,
            components=[
                ActionRow([
                    Button(
                        label="Пауза ⏸️",
                        style=ButtonType().Primary,
                        custom_id="pause_button"
                    ),
                    # Refer to line 13
                    Button(
                        label="Продолжить ✅",
                        style=ButtonType().Success,
                        custom_id="resume_button"  # Refer to line 17

                    ), Button(
                        label="Стоп 🔶",
                        style=ButtonType().Danger,
                        custom_id="stop_button"  # Refer to line 21
                    )
                ])
            ]
        )

    # elif ctx.guild.voice_client in bot.voice_clients and not ctx.voice_client.is_playing():

    else:
        name = convert_tuple(arg)
        print(name)
        search_result = client.search(name)
        try:
            print(f'{search_result.best.result.id}:{search_result.best.result.albums[0].id}')
            client.tracks([f'{search_result.best.result.id}:{search_result.best.result.albums[0].id}'])[0].download(
                os.path.join(f'{path}/{song}'))
        except Exception as e:
            pass
            # await ctx.send(traceback.format_exc())
        print('скачал трек')

        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            # try:

            if not ctx.guild.voice_client in bot.voice_clients:
                voice = await channel.connect()
                print(voice)
                print('пришёл в гс')
            else:
                voice = ctx.voice_client
            source = FFmpegPCMAudio(os.path.join(f'{path}/{song}'))
            voice.play(source, after=lambda x=0: check_queue(ctx, ctx.message.guild.id))
            print('начал проигрывать песню')
            # except:
            #     print('ошибка в 123 строке')
        else:
            await ctx.send("Зайдите в любой голосовой канал, чтобы использовать эту команду!")
        # player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id)) # or "path/to/your.mp3"

        embed = discord.Embed(title=f'{search_result.best.result.title} - {search_result.best.result.artists[0].name}',
                              color=0x8c00ff)
        embed.set_author(name=f'{search_result.best.result.artists[0].name}',
                         icon_url=f'https://{search_result.best.result.artists[0]["cover"].uri.replace("%%", "600x600")}')
        embed.add_field(name='Альбом:', value=f'{search_result.best.result.albums[0].title}', inline=False)
        embed.add_field(name='Год выпуска:', value=f'{search_result.best.result.albums[0].year}', inline=False)
        # print(f'{search_result.best.result.cover_uri}, {search_result.best.result}')

        if search_result.best.result.cover_uri == None:
            embed.set_image(url=f'https://music.yandex.ru/blocks/meta/i/og-image.png')
        else:
            embed.set_image(url=f'https://{search_result.best.result.cover_uri.replace("%%", "600x600")}')

        embed.set_footer(text="Никогда не используйте ’ в запросах!")
        # await ctx.send(embed=embed)

        await buttons.send(
            embed=embed,
            channel=ctx.channel.id,
            components=[
                ActionRow([
                    Button(
                        label="Пауза ⏸️",
                        style=ButtonType().Primary,
                        custom_id="pause_button"
                    ),
                    # Refer to line 13
                    Button(
                        label="Продолжить ✅",
                        style=ButtonType().Success,
                        custom_id="resume_button"  # Refer to line 17

                    ), Button(
                        label="Стоп 🔶",
                        style=ButtonType().Danger,
                        custom_id="stop_button"  # Refer to line 21
                    )
                ])
            ]
        )


@bot.command()
async def chart(ctx):
    chart = client.chart('world').chart

    text = [f'🏆 {chart.title}', chart.description, '', 'Треки:']

    for track_short in chart.tracks:
        track, chart = track_short.track, track_short.chart
        artists = ''
        if track.artists:
            artists = ' - ' + ', '.join(artist.name for artist in track.artists)

        track_text = f'{track.title}{artists}'

        if chart.progress == 'down':
            track_text = '🔻 ' + track_text
        elif chart.progress == 'up':
            track_text = '🔺' + track_text
        elif chart.progress == 'new':
            track_text = '🆕 ' + track_text
        elif chart.position == 1:
            track_text = '👑 ' + track_text

        track_text = f'{chart.position} {track_text}'
        text.append(track_text)

    embed = discord.Embed(title='Треки, популярные на Яндекс.Музыке прямо сейчас:',
                          color=0x8c00ff)
    embed.set_author(name=f'🏆 Чарт Яндекс.Музыки',
                     icon_url=f'https://music.yandex.ru/blocks/meta/i/og-image.png')
    embed.add_field(name='\u200b', value="\n".join(text[4:14]), inline=False)
    # embed.set_footer(text="Никогда не используйте ’ в запросах!")

    await ctx.send(embed=embed)
    # print('kj')


@bot.command()
async def play_chart(ctx):
    await ctx.send(f'{ctx.message.author.mention}, поставил в очередь!')
    chart = client.chart('world').chart

    for track_short in chart.tracks[:10]:
        track, chart = track_short.track, track_short.chart
        artists = ''
        if track.artists:
            artists = ' - ' + ', '.join(artist.name for artist in track.artists)

        track_text = f'{track.title}{artists}'

        print(f'{track_text} {track.cover_uri} {track.track_id} {track.artists[0].name} {track.artists[0].cover.uri}')

        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            # try:

            if not ctx.guild.voice_client in bot.voice_clients:
                voice = await channel.connect()
                print('пришёл в гс')

                search_result = client.search(track_text)
                try:

                    client.tracks([f'{search_result.best.result.id}:{search_result.best.result.albums[0].id}'])[
                        0].download(
                        os.path.join(f'{path}/{song}'))
                except Exception as e:
                    pass
                    # await ctx.send(traceback.format_exc())
                print('скачал трек')

                # voice = ctx.voice_client
                source = FFmpegPCMAudio(f'{path}/{song}')
                voice.play(source, after=lambda x=0: check_queue(ctx, ctx.message.guild.id))
                print('начал проигрывать песню')

            else:
                if ctx.voice_client.is_playing():
                    music_id.append(f'{track.track_id}')
                    song1 = f'{str(len(music_id))}.mp3'
                    source = FFmpegPCMAudio(f'{path}/{song1}')

                    try:
                        print(f'{track_text}')
                        client.tracks([music_id[-1]])[0].download(f'{path}/{song1}')
                    except Exception as e:
                        pass
                        # await ctx.send(traceback.format_exc())

                    if len(music_id) == 11:
                        music_id.clear()

                    bot_queue.append(f'•{track_text}')

                    guild_id = ctx.message.guild.id
                    if guild_id in queues:
                        queues[guild_id].append(source)
                    else:
                        queues[guild_id] = [source]

                else:
                    search_result = client.search(track_text)
                    try:

                        client.tracks([f'{search_result.best.result.id}:{search_result.best.result.albums[0].id}'])[
                            0].download(
                            os.path.join(f'{path}/{song}'))
                    except Exception as e:
                        pass
                        # await ctx.send(traceback.format_exc())
                    print('скачал трек')

                    voice = ctx.voice_client
                    source = FFmpegPCMAudio(f'{path}/{song}')
                    voice.play(source, after=lambda x=0: check_queue(ctx, ctx.message.guild.id))
                    print('начал проигрывать песню')

            # except:
            #     print('ошибка в 123 строке')
        else:
            await ctx.send("Зайдите в любой голосовой канал, чтобы использовать эту команду!")

        # voice.play(source, after=lambda x=0: check_queue(ctx, ctx.message.guild.id))
        search_result = client.search(track_text)

        embed = discord.Embed(title=f'{search_result.best.result.title} - {search_result.best.result.artists[0].name}',
                              color=0x8c00ff)
        embed.set_author(name=f'{search_result.best.result.artists[0].name}',
                         icon_url=f'https://{search_result.best.result.artists[0]["cover"].uri.replace("%%", "600x600")}')
        embed.add_field(name='Альбом:', value=f'{search_result.best.result.albums[0].title}', inline=False)
        embed.add_field(name='Год выпуска:', value=f'{search_result.best.result.albums[0].year}', inline=False)
        # print(f'{search_result.best.result.cover_uri}, {search_result.best.result}')

        if search_result.best.result.cover_uri == None:
            embed.set_image(url=f'https://music.yandex.ru/blocks/meta/i/og-image.png')
        else:
            embed.set_image(url=f'https://{search_result.best.result.cover_uri.replace("%%", "600x600")}')

        embed.set_footer(text="Никогда не используйте ’ в запросах!")
        # await ctx.send(embed=embed)

        await buttons.send(
            embed=embed,
            channel=ctx.channel.id,
            components=[
                ActionRow([
                    Button(
                        label="Пауза ⏸️",
                        style=ButtonType().Primary,
                        custom_id="pause_button"
                    ),
                    # Refer to line 13
                    Button(
                        label="Продолжить ✅",
                        style=ButtonType().Success,
                        custom_id="resume_button"  # Refer to line 17

                    ), Button(
                        label="Пропуск 🔶",
                        style=ButtonType().Danger,
                        custom_id="skip_button"  # Refer to line 21
                    )
                ])
            ]
        )


@bot.command()
async def dw(ctx, *arg):
    author = ctx.message.author
    con = None
    DONATE.clear()
    count = 0
    try:
        con = psycopg2.connect(settings['DATABASE_URL'])
        cur2 = con.cursor()
        cur2.execute('select * from donat')
        cur = con.cursor()
        cur.execute('select * from donat_server')

        result2 = cur.fetchall()
        result = cur2.fetchall()

        for i in result:
            DONATE.append(i)

        for i in result2:
            DONATE.append(i)
        con.commit()
        cur2.close()
    except Exception as error:
        print('Cause: {}'.format(error))

    finally:
        if con is not None:
            con.close()
            print('Database connection closed.')

    for i in DONATE:
        if author.discriminator in i[0] or str(ctx.guild.id) in i[0]:
            seconds = time.time()
            if int(i[1]) + 2678400 > int(seconds):
                def convert_tuple(c_tuple):
                    str = ' '.join(c_tuple)
                    return str

                name = convert_tuple(arg)
                print(name)
                search_result = client.search(name)
                dw_song = f'{search_result.best.result.title}-{search_result.best.result.artists[0].name}.mp3'
                DW_SONG.append(f'{search_result.best.result.title}-{search_result.best.result.artists[0].name}.mp3')
                await ctx.send(f'Скачиваю...')
                try:
                    print(f'{search_result.best.result.id}:{search_result.best.result.albums[0].id}')
                    client.tracks([f'{search_result.best.result.id}:{search_result.best.result.albums[0].id}'])[
                        0].download(
                        os.path.join(f'{path}/{dw_song}'))
                except Exception as e:
                    pass
                    # await ctx.send(traceback.format_exc())

                embed = discord.Embed(
                    title=f'{search_result.best.result.title} - {search_result.best.result.artists[0].name}',
                    color=0x8c00ff)
                embed.set_author(name=f'{search_result.best.result.artists[0].name}',
                                 icon_url=f'https://{search_result.best.result.artists[0]["cover"].uri.replace("%%", "600x600")}')
                embed.add_field(name='Альбом:', value=f'{search_result.best.result.albums[0].title}', inline=False)
                embed.add_field(name='Год выпуска:', value=f'{search_result.best.result.albums[0].year}', inline=False)

                if search_result.best.result.cover_uri == None:
                    embed.set_image(url=f'https://music.yandex.ru/blocks/meta/i/og-image.png')
                else:
                    embed.set_image(url=f'https://{search_result.best.result.cover_uri.replace("%%", "600x600")}')

                embed.set_footer(text="Никогда не используйте ’ в запросах!")

                await ctx.send(f'{author.mention}, отправил вам в ЛС')
                await author.send(embed=embed)
                await author.send(file=discord.File(f'{path}/{"".join(DW_SONG)}'))

                os.remove(f'{path}/{"".join(DW_SONG)}')
                DW_SONG.clear()

            else:
                con = None
                try:
                    con = psycopg2.connect(settings['DATABASE_URL'])
                    cur2 = con.cursor()
                    cur2.execute(f"""delete from donat where discriminator = '{author.discriminator}'""")
                    con.commit()
                    cur2.close()
                except Exception as error:
                    print('Cause: {}'.format(error))

                finally:
                    if con is not None:
                        con.close()
                        print('Database connection closed.')

                await ctx.send(
                    f'{author.mention}, Срок действия подписки уже истёк 😢, напишите `!pro`, чтобы продлить её.')
        elif author.discriminator not in i[0]:
            count += 1

    if count >= len(DONATE):
        await ctx.send(f'{author.mention}, Для выполнения этой команды требуется **👑Salmon-pro**.')


@buttons.click
async def pause_button(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.reply("Поставил на паузу!")
    else:
        await ctx.send('Нечего ставить на паузу')


@buttons.click
async def resume_button(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.reply("Возобновил проигрывание!")
    else:
        await ctx.reply('Нет песни на паузе')


@buttons.click
async def stop_button(ctx):
    await ctx.reply("Музыка остановлена!")
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    # await ctx.voice_client.disconnect()


@buttons.click
async def skip_button(ctx):
    await ctx.reply("Песня пропущена!")
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()


@bot.command()
async def queue(ctx):
    if len(bot_queue) == 0:
        await ctx.send('В очереди ничего нет')
    embed = discord.Embed(title='🥁 Очередь музыки:',
                          color=0xf37944)
    embed.add_field(name='\u200b', value='\n'.join(bot_queue), inline=False)
    # embed.set_footer(text="Никогда не используйте ’ в запросах!")

    await ctx.send(embed=embed)


@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.reply('Нечего ставить на паузу')


@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send('Нет песни на паузе')


@bot.command()
async def stop(ctx):
    await ctx.reply("Музыка остановлена!")
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.voice_client.disconnect()
    # await ctx.send('Нет песни на паузе')


@bot.command()
async def stop_game(ctx):
    cycles["game"] = False


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
    print(f'{member.avatar_url}')
    embed.add_field(name='📆 Дата создания:', value=f'{member.created_at}', inline=False)
    embed.add_field(name='💥 Высшая роль:', value=f'{member.top_role.mention}', inline=False)
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

    embed.add_field(name='\u200b', value='**🎧Музыка**', inline=False)
    embed.add_field(name='`!play (название музыки)`', value='Проиграет указанную музыку', inline=True)
    embed.add_field(name='`!chart`', value='Покажет топ-10 песен из чарта Яндекс Музыки', inline=True)
    embed.add_field(name='\u200b', value='\u200b', inline=False)
    embed.add_field(name='👑`!dw (название песни)`', value='Скачает абсолютно любую музыку', inline=True)
    embed.add_field(name='`!play_chart`', value='Проиграет песни из чарта   Яндекс Музыки ', inline=True)
    embed.add_field(name='\u200b', value='\u200b', inline=False)
    embed.add_field(name='`!queue`', value='Выведет очередь музыки', inline=True)

    embed.add_field(name='\u200b', value='**🍿Фильмы**', inline=False)
    embed.add_field(name='`!film (фильм)`', value='Покажет информацию о фильме, а также скинет\
     ссылку на его просмотр на Кинопоиске', inline=True)

    embed.add_field(name='\u200b', value='**🎲Мини-игры🎲**', inline=False)
    embed.add_field(name='`!bc`', value='Поиграет с вами в "Быки и коровы" - игру, в \
    ходе которой вы должены определить, какое число я задумал.', inline=True)
    embed.add_field(name='`!logo`', value='Поиграет в "угадайку" названия компании по логотипу', inline=True)
    embed.add_field(name='\u200b', value='\u200b', inline=False)
    embed.add_field(name='`!stop game`', value='Остановка игр', inline=True)
    embed.add_field(name='`!nim`', value='Сыграет в Ним - игру, в которой есть несколько кучек с камнями, \
        где ваша цель будет забрать последни камень', inline=True)
    embed.add_field(name='`!ln`', value='Поиграет в отгадывание языка по \n фразе', inline=False)

    embed.add_field(name='\u200b', value='**🔍Другое**', inline=False)
    embed.add_field(name='`!info (@<упомяните человека>)`', value='Покажет \
    краткую информацию об упомянутом человеке.', inline=True)
    embed.add_field(name='`!wn (город)`', value='Покажет погоду в этом городе сегодня, \
    также вам будет доступна кнопочка `(Погода на завтра ⛅)`, кликнув по которой, \
    вы сможете узнать погоду на следующий день в том же городе.', inline=True)
    embed.add_field(name='\u200b', value='\u200b', inline=False)
    embed.add_field(name='`!news`', value='Покажет последние новости к этому часу, также вам будет доступна кнопка \n \
    `(➕ Больше новостей)`, при нажимании на неё бот пришлёт больше новостей.', inline=True)
    embed.add_field(name='\u200b', value='\u200b', inline=False)

    embed.add_field(name='**👑Salmon pro👑**', value='Подписка на бота с помощью которой, вы сможете **скачивать музыку \
    буквально в два клика**', inline=False)
    embed.add_field(name='`!pro`', value='Покажет \
        подробную информацию о подписке', inline=True)

    embed.add_field(name='\u200b',
                    value='Более подробную информацию ищите здесь - https://clck.ru/eAsPG',
                    inline=False)
    # embed.add_field(name="\u200B", value='<https://github.com/savateevdmit/Salmon.git>', inline=False)
    await ctx.send(embed=embed)
    print(ctx.guild.id)


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command()
async def film(ctx, *kino):
    kino = ' '.join([i for i in kino])
    try:
        html = requests.get(
            f'https://ru.wikipedia.org/w/index.php?search={kino}+фильм&title=Служебная%3AПоиск&go=Перейти&ns0=1').text
        soup = BeautifulSoup(html, 'html.parser')
        find_text = str(soup.find('div', {'class': 'mw-search-result-heading'}))
        a = find_text.split(' ')[3].split('=')[1][1:-1]
        html = requests.get(f'https://ru.wikipedia.org/{a}').text
        soup = BeautifulSoup(html, 'html.parser')
        find_text = str(soup.findAll('span', {'class': 'no-wikidata'}))
        b = find_text.split(' ')
        for i in b:
            if 'src' in i:
                b = i.split('=')[1][1:-1]
                break
        # print(b)
        picture = f'https:{b}'
        find_text = str(soup.find('h1', {'class': 'firstHeading mw-first-heading'}))
        g = '+'.join(find_text.split('=')[-1].split('>')[-2][:-4].split(' '))
        film_name = find_text.split('=')[-1].split('>')[-2][:-4]
        html = requests.get(f'https://www.kinopoisk.ru/index.php?kp_query={g}').text
        soup = BeautifulSoup(html, 'html.parser')
        find_text = str(soup.findAll('p', {'class': 'name'}))
        c = find_text.split(' ')
        try:
            d = find_text.split('/')[7][2:-1]
        except:
            ss = f'https://www.kinopoisk.ru/index.php?kp_query={g}'
        pp = 10
        k = 0
        n = 0
        try:
            for i in d.lower():
                if i in film_name.lower():
                    n += 1
            k = len(film_name) / n
            n = 0
            while k < 0.8:
                d = find_text.split('/')[7 + pp][2:-1]
                for i in d.lower():
                    if i in film_name.lower():
                        n += 1
                k = n / len(film_name)
                n = 0
                pp += 10
            o = pp / 10 * 2 - 2
            for i in c:
                if i[-2] in numbers and o == 0:
                    c = i.split('=')[1][1:-1]
                    break
                if i[-2] in numbers:
                    o -= 1
            ss = f'https://www.kinopoisk.ru/film/{c}/'
        except Exception as e:
            print(e)

        html = requests.get(f'https://ru.wikipedia.org/{a}').text
        soup = BeautifulSoup(html, 'html.parser')
        find_text = str(soup.find('span', {'data-wikidata-property-id': 'P272'}))
        e = find_text.split(' ')
        h = []
        if e[0] == "None":
            find_text = str(soup.find('div', {'data-wikidata-property-id': 'P272'}))
            e = find_text.split(' ')
        for i in e:
            if 'href' in i:
                h.append(i.split('/')[2][:-1])
        find_text = str(soup.find('span', {'data-wikidata-property-id': 'P2047'}))
        time = find_text.split('>')[1].split('<')[0]
        find_text = str(soup.find('span', {'data-wikidata-property-id': 'P2130'}))
        budget = find_text
        try:
            budget = budget[:budget.index('<a')] + budget[budget.index('a>') + 2:]

        except:
            pass
        budget = budget.split('">')[1].split('<sup')[0]
        find_text = str(soup.find('span', {'data-wikidata-property-id': 'P2142'}))
        sbori = find_text.split('">')[1].split('<sup')[0]
        cc1 = h[0]
        cc2 = 0
        try:
            cc2 = h[1]
        except:
            pass
        html = requests.get(f'https://ru.wikipedia.org/wiki/{cc1}').text
        soup = BeautifulSoup(html, 'html.parser')
        find_text = str(soup.findAll('span', {'class': 'no-wikidata'}))
        k = find_text.split(' ')
        for i in k:
            if 'src' in i:
                k = i.split('=')[1][1:-1]
                break
        # print(b)
        picture1 = f'https:{k}'
        html = requests.get(f'https://ru.wikipedia.org/{a}').text
        soup = BeautifulSoup(html, 'html.parser')
        find_text = str(soup.find('span', {'data-wikidata-property-id': 'P345'}))
        s = find_text.split(' ')
        for i in s:
            if 'href' in i:
                s = i.split('=')[1][1:-1]
        html = requests.get(s).text
        soup = BeautifulSoup(html, 'html.parser')
        find_text = str(soup.find('span', {'class': 'sc-7ab21ed2-1 jGRxWM'}))
        rating = find_text.split(' ')[-1].split('>')[-2].split('<')[0]
        find_text = str(soup.find('div', {'class': 'ipc-html-content ipc-html-content--base'}))
        s = find_text.split('<div>')[1].split('<span')[0]
        while True:
            try:
                s = s[:s.index('(')] + s[s.index(')') + 1:]
            except:
                break
    except:
        await ctx.reply('Я не понял запрос(\nПопробуйте уточнить!')
    try:
        opisanie = GoogleTranslator(source='auto', target='ru').translate(s)
        opisanie = GoogleTranslator(source='auto', target='ru').translate(s)
        embed = discord.Embed(title=f'🍿{film_name}',
                              color=0x1ba300)
        if len(picture1) > 12:
            if cc2 != 0:
                embed.set_author(name=f'{cc1} and {cc2}',
                                 icon_url=picture1)
            else:
                embed.set_author(name=cc1,
                                 icon_url=picture1)
        if len(time) > 1:
            embed.add_field(name='Длительность:', value=time, inline=False)
        if len(rating) > 0:
            embed.add_field(name='IMDb рейтинг:', value=f'{rating}/10', inline=False)
        if len(opisanie) > 1:
            embed.add_field(name='Краткое описание:', value=opisanie, inline=False)
        if len(ss) > 1:
            embed.add_field(name='Ссылка на просмотр:', value=f'{ss}', inline=False)
        if len(picture) > 1:
            embed.set_image(url=picture)
        embed.set_footer(text="Никогда не используйте ’ в запросах!")

        await ctx.send(embed=embed)
    except:
        await ctx.reply('Возникла непредвиденная ошибка!\nПожалуйста, обратитесь в тех. поддержку!')


@bot.command()
async def logo(ctx):
    global PLAY
    if PLAY:
        PLAY = False
        con = None
        number = random.sample(range(1, 60), 1)
        # number = 56
        count = 0
        word = morph.parse('секунда')[0]

        try:
            con = psycopg2.connect(settings['DATABASE_URL'])
            cur = con.cursor()
            cur.execute(f'SELECT * from logo where id = {number[0]}')

            # display the PostgreSQL database server version
            result = cur.fetchone()
            print(result)

            # close the communication with the HerokuPostgres
            cur.close()
        except Exception as error:
            print('Cause: {}'.format(error))

        finally:
            if con is not None:
                con.close()
                print('Database connection closed.')

        embed = discord.Embed(title='❗Правила❗', color=0xf5e000)

        embed.add_field(name='❓Угадайка логотип❔',
                        value='🔰 У вас есть 10 попыток, чтобы угадать логотип по картинке. \
                        Писать можно как на русском, так и на английском.',
                        inline=False)
        embed.add_field(name='\u200b',
                        value='**♻Игра уже началась, вот первый логотип!♻**',
                        inline=False)
        embed.set_image(
            url=f'{result[3]}')
        await ctx.send(embed=embed)
        time0 = time.time()

        while True:
            message = await bot.wait_for('message', check=logo)
            if message.content == '!stop game':
                await ctx.send(f'❌{message.author.mention}, игра остановлена!❌')
                return
            else:
                id = message.author.id
                if message.content.lower() == result[1].lower() or \
                        message.content.lower() == result[2].lower():
                    # message.content.lower() in result[1].lower() or\
                    # message.content.lower() in result[2].lower():
                    time1 = time.time()
                    embed = discord.Embed(title='❓Угадайка логотип❔', color=0x4fde02)
                    embed.add_field(name='🎉' + f'**Поздравляем!**',
                                    value=f'<@!{id}>' + f', вы угадали за **{int(time1 - time0)}\
                                            {word.make_agree_with_number(int(time1 - time0)).word}**',
                                    inline=False)
                    embed.set_image(
                        url=f'{result[4]}')
                    # embed.set_footer(text='Продолжайте!')
                    await message.channel.send(embed=embed)
                    count = 0
                    PLAY = True
                    return
                elif count == 10:
                    embed = discord.Embed(title='❓Угадайка логотип❔', color=0xf25a07)
                    embed.add_field(name=f'Игра была закончена, так как никто не смог ответить(',
                                    value=f'Ответ: **{result[2]}**',
                                    inline=False)
                    embed.set_image(
                        url=f'{result[4]}')
                    # embed.set_footer(text='Продолжайте!')
                    await message.channel.send(embed=embed)
                    count = 0
                    PLAY = True
                    return
                else:
                    count += 1

        embed = discord.Embed(title='Угадайка логотип', color=0xf25a07)
        embed.add_field(name=f'Игра была закончена, так как никто не смог ответить(',
                        value=f'Ответ: **{result[2]}**',
                        inline=False)
        embed.set_image(
            url=f'{result[4]}')
        # embed.set_footer(text='Продолжайте!')
        await message.channel.send(embed=embed)
        count = 0
        PLAY = True
        return

    else:
        await ctx.send(f'{ctx.message.author.mention}, пожалуйста завершите начатую игру!')


@bot.command()
async def add(ctx, arg, server=False):
    flag = False
    author = ctx.message.author
    if author.discriminator in DEVELOPERS:
        con = None
        try:
            if not server:
                con = psycopg2.connect(settings['DATABASE_URL'])
                cur = con.cursor()
                cur2 = con.cursor()
                cur3 = con.cursor()
                seconds = time.time()
                cur.execute(f"""INSERT INTO donat VALUES ('{arg}', {seconds})""")
                cur3.execute('select * from donat_server')
                cur2.execute('select * from donat')

                # display the PostgreSQL database server version
                result = cur2.fetchall()[:-1]
                result2 = cur3.fetchall()[:-1]
                for i in result:
                    DONATE1.append(f'🔹 {i[0]}')
                    if arg in i[0]:
                        flag = True

                for i in result2:
                    DONATE_SERVER.append(f'🔹 {i[0]}')
                    if arg in i[0]:
                        flag = True
                if flag:
                    await ctx.send(f'❌Ошибка! {arg}, уже был добавлен❌')
                    await ctx.send(f'🔰Список пользователей с премиумом:')
                    await ctx.send('\n'.join(DONATE1))
                    await ctx.send(f'🔰Список серверов с премиумом:')
                    await ctx.send('\n'.join(DONATE_SERVER))
                # close the communication with the HerokuPostgres
                else:
                    con.commit()
                    await ctx.send(f'✅{arg}, добавлен✅')
                    await ctx.send(f'🔰Список пользователей с премиумом:')
                    await ctx.send('\n'.join(DONATE1))
                    await ctx.send(f'🔰Список серверов с премиумом:')
                    await ctx.send('\n'.join(DONATE_SERVER))

                cur.close()
                cur2.close()
                # cur3.close()

            else:
                con = psycopg2.connect(settings['DATABASE_URL'])
                cur = con.cursor()
                cur2 = con.cursor()
                cur3 = con.cursor()
                seconds = time.time()
                cur3.execute(f"""INSERT INTO donat_server VALUES ('{arg}', {seconds})""")
                cur2.execute('select * from donat_server')
                cur.execute('select * from donat')

                # display the PostgreSQL database server version
                result2 = cur2.fetchall()[:-1]
                result = cur.fetchall()[:-1]
                for i in result:
                    DONATE1.append(f'🔹 {i[0]}')
                    if arg in i[0]:
                        flag = True

                for i in result2:
                    DONATE_SERVER.append(f'🔹 {i[0]}')
                    if arg in i[0]:
                        flag = True

                if flag:
                    await ctx.send(f'❌Ошибка! {arg}, уже был добавлен❌')
                    await ctx.send(f'🔰Список пользователей с премиумом:')
                    await ctx.send('\n'.join(DONATE1))
                    await ctx.send(f'🔰Список серверов с премиумом:')
                    await ctx.send('\n'.join(DONATE_SERVER))
                # close the communication with the HerokuPostgres
                else:
                    con.commit()
                    await ctx.send(f'✅{arg}, добавлен✅')
                    await ctx.send(f'🔰Список пользователей с премиумом:')
                    await ctx.send('\n'.join(DONATE1))
                    await ctx.send(f'🔰Список серверов с премиумом:')
                    await ctx.send('\n'.join(DONATE_SERVER))

                cur.close()
                cur2.close()
                cur3.close()

        except Exception as error:
            print('Cause: {}'.format(error))

        finally:
            if con is not None:
                con.close()
                print('Database connection closed.')
                DONATE1.clear()
                DONATE_SERVER.clear()
    else:
        await ctx.send('Эта команда только для разработчиков!')


weather = ''


@bot.command()
async def wn(ctx, *c):
    global weather
    weather = c
    region = tr(' '.join(c))
    html = requests.get(f'https://pogoda.mail.ru/prognoz/{region}/').text
    r = 0
    soup = BeautifulSoup(html, 'html.parser')
    find_text = str(soup.find('h1', {'class': 'information__header__left__place__city'}))
    city = find_text.split('>')[1].split('<')[0]
    find_text = str(soup.find('div', {'class': 'information__header__left__date'}))
    date = find_text.split('>')[1].split('<')[0][7:-6]
    find_text = str(soup.find('div', {'class': 'information__content__temperature'}))
    temp = find_text.split(' ')[-1].split('span>')[1].split("<")[0][:-8]
    sost = find_text.split('="')[-1].split('">')[0]
    find_text = str(soup.find('div', {'class': 'information__content__additional__item'}))
    ohyh = find_text.split('e="')[1].split('">')[0].split(' ')[-1]
    find_text = str(soup.findAll('div', {'class': 'information__content__additional__item'}))
    dav = find_text.split('e="')[2 + r].split('">')[0].split(': ')[1]
    if '+' in dav or '-' in dav:
        r = 1
    dav = find_text.split('e="')[2 + r].split('">')[0].split(': ')[1]
    vlag = find_text.split('e="')[3 + r].split('">')[0].split(': ')[1]
    veter = find_text.split('e="')[4 + r].split('">')[0].split(': ')[1]
    ulfil = find_text.split('e="')[5 + r].split('">')[0].split(': ')[1]
    find_text = str(soup.findAll('div', {'class': 'information__content__additional__item__sun'}))
    sunup = ''
    sundown = ''
    try:
        sunup = find_text.split('e="')[1].split('">')[0].split(': ')[1]
        sundown = find_text.split('e="')[2].split('">')[0].split(': ')[1]
    except:
        pass
    # print(temp, ohyh, sost, dav, vlag, veter, ulfil, )
    embed = discord.Embed(title=f'⛅ {city}', description=f'{date}',
                          color=0x0084ff)
    embed.add_field(name='🌡️ Температура:', value=temp, inline=True)
    embed.add_field(name='🪁 Но ощущается как:', value=ohyh, inline=True)
    embed.add_field(name='🌦️ Состояние:', value=sost, inline=False)
    embed.add_field(name='🩺 Давление:', value=dav, inline=True)
    embed.add_field(name='💧 Влажность:', value=vlag, inline=False)
    embed.add_field(name='🍃 Ветер:', value=veter, inline=True)
    embed.add_field(name='☀️ Индекс ультрафиолета:', value=ulfil, inline=False)
    if sunup != '':
        embed.add_field(name='🌅 Восход:', value=sunup, inline=True)
        embed.add_field(name='🌇 Закат:', value=sundown, inline=True)
    embed.set_footer(text="Никогда не используйте ’ в запросах!")

    await ctx.send(embed=embed,
                   components=[[Button(label="Погода на завтра ⛅", custom_id="wt", style=ButtonStyle.green)]])

    interaction = await bot.wait_for("button_click")
    if interaction.component.custom_id == 'wt':
        region = tr(' '.join(weather))
        html = requests.get(f'https://pogoda.mail.ru/prognoz/{region}/14dney/#day2').text
        soup = BeautifulSoup(html, 'html.parser')
        find_text = str(soup.findAll('div', {'class': 'day__temperature'}))
        temp = find_text.split('e">')[7].split('</')[0]
        find_text = str(soup.findAll('div', {'class': 'day__description'}))
        ohyh = ''.join(find_text.split('e="')[14].split('">')[0].split(' ')[2:])
        sost = find_text.split('e="')[15].split('">')[0]
        find_text = str(soup.findAll('div', {'class': 'day__additional'}))
        dav = ' '.join(find_text.split('e="')[31].split('">')[0].split(' ')[1:])
        vlag = ' '.join(find_text.split('e="')[32].split('">')[0].split(' ')[1:])
        veter = ' '.join(find_text.split('e="')[33].split('">')[0].split(' ')[1:])
        ulfil = ' '.join(find_text.split('e="')[34].split('">')[0].split(' ')[2:])
        find_text = str(soup.findAll('div', {'class': 'history-meteo__info'}))
        sunup = find_text.split('\n\t\t\t\t\t\t\t\t\t\t\t\t')[5].split('\n\t')[0]
        sundown = find_text.split('\n\t\t\t\t\t\t\t\t\t\t\t\t')[6].split('\n\t')[0]
        find_text = str(soup.findAll('div', {'class': 'heading heading_minor heading_line'}))
        date = find_text.split('e">')[2].split('\t')[-1].split(' <s')[0][1:]
        html = requests.get(f'https://pogoda.mail.ru/prognoz/{region}/').text
        soup = BeautifulSoup(html, 'html.parser')
        find_text = str(soup.find('h1', {'class': 'information__header__left__place__city'}))
        city = find_text.split('>')[1].split('<')[0]
        embed = discord.Embed(title=f'⛅ {city}', description=date,
                              color=0x0084ff)
        embed.add_field(name='🌡️ Температура:', value=temp, inline=True)
        embed.add_field(name='🪁 Но ощущается как:', value=ohyh, inline=True)
        embed.add_field(name='🌦️ Состояние:', value=sost, inline=False)
        embed.add_field(name='🩺 Давление:', value=dav, inline=True)
        embed.add_field(name='💧 Влажность:', value=vlag, inline=False)
        embed.add_field(name='🍃 Ветер:', value=veter, inline=True)
        embed.add_field(name='☀️ Индекс ультрафиолета:', value=ulfil, inline=False)
        if sunup != '':
            embed.add_field(name='🌅 Восход:', value=sunup, inline=True)
            embed.add_field(name='🌇 Закат:', value=sundown, inline=True)
        embed.set_footer(text="Никогда не используйте ’ в запросах!")

        await interaction.send(embed=embed, ephemeral=False)


@bot.command()
async def news(ctx, *c):
    global news2
    html = requests.get(f'https://news.mail.ru/?').text
    soup = BeautifulSoup(html, 'html.parser')
    find_text = str(soup.findAll('a', {'class': 'list__text'}))
    news = {}
    for i in find_text.split('"'):
        if 'http' in i:
            news[find_text.split('"')[find_text.split('"').index(i) + 1][1:-15]] = i
    pnews = {}
    find_text = str(soup.findAll('a', {'class': 'newsitem__title link-holder'}))
    pnews[find_text.split('href="')[1].split('"><')[0]] = find_text.split('ner">')[1].split('</span')[0]
    find_text = str(soup.findAll('a', {'class': 'link link_flex'}))
    for i in find_text.split('"'):
        if 'http' in i:
            pnews[find_text.split('"')[find_text.split('"').index(i) + 3][1:-22]] = i

    for i in pnews:
        if 'http' in i:
            a = i

    del pnews[a]
    b = []
    for i in news:
        b.append(f'{i} ([подробнее]({news[i]}))\n\n')
    b = ''.join(b)
    embed = discord.Embed(title='🔍 Последние новости!', description=b,
                          color=0xf5cc00)
    await ctx.send(embed=embed,
                   components=[[Button(label="➕ Больше новостей", custom_id="news", style=ButtonStyle.green)]])

    b = []
    for i in pnews:
        b.append(f'{i} ([подробнее]({pnews[i]}))\n\n')
    b = ''.join(b)
    embed = discord.Embed(title='🔍 Последние новости!', description=b,
                          color=0xf5cc00)
    news2 = embed

    interaction = await bot.wait_for("button_click")

    if interaction.component.custom_id == 'news':
        await interaction.send(embed=news2, ephemeral=False)


@bot.command()
async def nim(ctx):
    global xod, a, b, c, start, m, n, x
    options = [
        SelectOption(label='1', value='1'),
        SelectOption(label='2', value='2'),
        SelectOption(label='3', value='3')
    ]
    await ctx.send(
        f'❗Правила❗\n🔰 Имеется несколько куч камней. Каждый игрок в свой ход может забрать из любой кучи любое (ненулевое) количество камней(кроме игры с 1 кучи, там можно от 1 до 3 камней). Выигрывает тот, кто забрал последний камень из последней кучи.\n'
        'В игру со скольки кучами вы хотите сыграть?',
        components=[
            Select(
                placeholder="Выберите кол-во куч",
                options=options,
                custom_id='a',
            )
        ],
    )

    interaction = await bot.wait_for(
        "select_option", check=lambda inter: inter.custom_id == "a")
    values = int(interaction.values[0])
    zz = []
    options = [
        SelectOption(label='1', value='1'),
        SelectOption(label='2', value='2'),
        SelectOption(label='3', value='3'),
        SelectOption(label='4', value='4'),
        SelectOption(label='5', value='5'),
        SelectOption(label='6', value='6'),
        SelectOption(label='7', value='7'),
        SelectOption(label='8', value='8'),
        SelectOption(label='9', value='9'),
        SelectOption(label='10', value='10'),
        SelectOption(label='11', value='11'),
        SelectOption(label='12', value='12'),
        SelectOption(label='13', value='13'),
        SelectOption(label='14', value='14'),
        SelectOption(label='15', value='15'),
        SelectOption(label='16', value='16'),
        SelectOption(label='17', value='17'),
        SelectOption(label='18', value='18'),
        SelectOption(label='19', value='19'),
        SelectOption(label='20', value='20'),
        SelectOption(label='21', value='21'),
        SelectOption(label='22', value='22'),
        SelectOption(label='23', value='23'),
        SelectOption(label='24', value='24'),
        SelectOption(label='25', value='25')

    ]
    for i in range(1, values + 1):
        await interaction.send(
            f'Сколько камней будет в {i} куче?',
            components=[
                Select(
                    placeholder=f"Выберите кол-во камней в {i} куче",
                    options=options,
                    custom_id='b',
                )
            ], ephemeral=False,
        )
        interaction = await bot.wait_for(
            "select_option", check=lambda inter: inter.custom_id == "b")
        zz.append(interaction.values[0])
        interaction.send(f'Вы выбрали {interaction.values[0]} камней', ephemeral=False)
    word2 = morph.parse('камень')[0]
    try:
        c = int(zz[2])
    except:
        pass
    try:
        b = int(zz[1])
    except:
        pass
    try:
        a = int(zz[0])
    except:
        pass
    if start:
        embed = discord.Embed(title='❗Условия❗',
                              color=0xd1ff52)

        embed.add_field(name='1 куча:', value=f'{a} {word2.make_agree_with_number(a).word}', inline=True)
        if b != 0:
            embed.add_field(name='2 куча:', value=f'{b} {word2.make_agree_with_number(b).word}', inline=True)
        if c != 0:
            embed.add_field(name='3 куча:', value=f'{c} {word2.make_agree_with_number(c).word}', inline=True)
        await interaction.send(embed=embed, ephemeral=False)
        start = False
    if a != 0 and b != 0 and c != 0:
        while a != 0 or b != 0 or c != 0:
            x = 0  # количество камней, забираемых из кучи
            n = 0
            if a == b == 0:
                n = 3
                x = c
            elif a == c == 0:
                n = 2
                x = b
            elif b == c == 0:
                n = 1
                x = a
            # проверяю если в какой-то куче 0 камней, то стараюсь выровнять кучи
            # если две другие кучи уже равны, то уменьшаю одну из куч на 1 камень
            elif a == 0 and b != 0 and c != 0:
                if b == c:
                    n = 2
                    x = 1
                elif b > c:
                    n = 2
                    x = b - c
                else:
                    n = 3
                    x = c - b
            elif b == 0 and a != 0 and c != 0:
                if a == c:
                    n = 1
                    x = 1
                elif a > c:
                    n = 1
                    x = a - c
                else:
                    n = 3
                    x = c - a
            elif c == 0 and a != 0 and b != 0:
                if a == b:
                    n = 1
                    x = 1
                elif a > b:
                    n = 1
                    x = a - b
                else:
                    n = 2
                    x = b - a
            # проверяю если в каких-то двух кучах одинаковое количество камней, то
            # обнуляю третью кучу
            elif b == c and a != 0:
                n = 1
                x = a
            elif a == c and b != 0:
                n = 2
                x = b
            elif a == b and c != 0:
                n = 3
                x = c
            # проверяю проигрышность ситуации любой другой комбинации
            # если комбинация проигрышная вычитаю 1 камень из наибольшей кучи
            else:
                aa = a
                bb = b
                cc = c
                s = 0
                x = 0
                r = 0
                while aa != 0 or bb != 0 or cc != 0:
                    s = aa % 2 + bb % 2 + cc % 2
                    if s % 2 != 0:
                        x += 2 ** r
                        razr = r
                    aa = aa // 2
                    bb = bb // 2
                    cc = cc // 2
                    r += 1
                if x == 0:
                    x = 1
                    if a > b and a > c:
                        n = 1
                    elif b > a and b > c:
                        n = 2
                    else:
                        n = 3
                else:
                    aaa = a
                    while aaa > 0:
                        aa = aaa
                        bb = b
                        cc = c
                        nim = 0
                        r = 0
                        while aa != 0 or bb != 0 or cc != 0:
                            s = aa % 2 + bb % 2 + cc % 2
                            if s % 2 != 0:
                                nim += 2 ** r
                            aa = aa // 2
                            bb = bb // 2
                            cc = cc // 2
                            r += 1
                        if nim == 0:
                            n = 1
                            x = a - aaa
                            aaa = 0
                        aaa -= 1
                    if n == 0:
                        bbb = b
                        while bbb > 0:
                            aa = a
                            bb = bbb
                            cc = c
                            nim = 0
                            r = 0
                            while aa != 0 or bb != 0 or cc != 0:
                                s = aa % 2 + bb % 2 + cc % 2
                                if s % 2 != 0:
                                    nim += 2 ** r
                                aa = aa // 2
                                bb = bb // 2
                                cc = cc // 2
                                r += 1
                            if nim == 0:
                                n = 2
                                x = b - bbb
                                bbb = 0
                            bbb -= 1
                    if n == 0:
                        ccc = c
                        while ccc > 0:
                            aa = a
                            bb = b
                            cc = ccc
                            nim = 0
                            r = 0
                            while aa != 0 or bb != 0 or cc != 0:
                                s = aa % 2 + bb % 2 + cc % 2
                                if s % 2 != 0:
                                    nim += 2 ** r
                                aa = aa // 2
                                bb = bb // 2
                                cc = cc // 2
                                r += 1
                            if nim == 0:
                                n = 3
                                x = c - ccc
                                ccc = 0
                            ccc -= 1
            if n == 1:
                a -= x
            elif n == 2:
                b -= x
            else:
                c -= x
            embed = discord.Embed(title='🪨Ним🪨', description='Мой ход:',
                                  color=0xd1ff52)
            embed.add_field(name='\u200b', value=f'**🔸Я взял {x} {word2.make_agree_with_number(x).word}**',
                            inline=True)
            embed.add_field(name=f'🔸Из {n} кучи', value=f'------------------------', inline=False)
            # embed.add_field(name='------------------------', value='\u200b', inline=False)
            embed.add_field(name='1 куча:', value=f'{a} {word2.make_agree_with_number(a).word}', inline=True)
            embed.add_field(name='2 куча:', value=f'{b} {word2.make_agree_with_number(b).word}', inline=True)
            embed.add_field(name='3 куча:', value=f'{c} {word2.make_agree_with_number(c).word}', inline=True)
            if a == b == c == 0:
                embed.add_field(name='🏆Я выиграл!', value=f'А ты нет :)', inline=False)
                await ctx.send(embed=embed)
                break
            await ctx.send(embed=embed)
            embed = discord.Embed(title='🪨Ним🪨', description='♻️Твой ход',
                                  color=0xd1ff52)
            embed.add_field(name='\u200b', value=f'**Из какой кучи ты возьмешь камни?**', inline=False)
            options = [
                SelectOption(label='1', value='1'),
                SelectOption(label='2', value='2'),
                SelectOption(label='3', value='3')
            ]
            if a == 0:
                del options[0]
            if b == 0:
                del options[1]
            if c == 0:
                del options[2]
            await ctx.send(
                embed=embed,
                components=[
                    Select(
                        placeholder=f"Выбери номер кучи!",
                        options=options,
                        custom_id='c',
                    )
                ],
            )
            interaction = await bot.wait_for(
                "select_option", check=lambda inter: inter.custom_id == "c")
            n = int(interaction.values[0])
            if n == 1:
                kk = a
            elif n == 2:
                kk = b
            else:
                kk = c
            options = []
            for i in range(1, kk + 1):
                options.append(SelectOption(label=i, value=i))
            await interaction.send(
                'Сколько камней хотите взять?',
                components=[
                    Select(
                        placeholder=f"Выбери число камней!",
                        options=options,
                        custom_id='d',
                    )
                ], ephemeral=False,
            )
            interaction = await bot.wait_for(
                "select_option", check=lambda inter: inter.custom_id == "d")
            x = int(interaction.values[0])
            if n == 1:
                a -= x
            elif n == 2:
                b -= x
            else:
                c -= x
            embed = discord.Embed(title='🪨Ним🪨', description='Твой ход:',
                                  color=0xd1ff52)
            embed.add_field(name='\u200b', value=f'**🔸Ты взял {x} {word2.make_agree_with_number(x).word}**',
                            inline=True)
            embed.add_field(name=f'🔸Из {n} кучи', value=f'------------------------', inline=False)
            # embed.add_field(name='------------------------', value='\u200b', inline=False)
            embed.add_field(name='1 куча:', value=f'{a} {word2.make_agree_with_number(a).word}', inline=True)
            embed.add_field(name='2 куча:', value=f'{b} {word2.make_agree_with_number(b).word}', inline=True)
            embed.add_field(name='3 куча:', value=f'{c} {word2.make_agree_with_number(c).word}', inline=True)
            if a == b == c == 0:
                embed.add_field(name='🏆Ты выиграл!', value=f'А я нет :(', inline=False)
            await interaction.send(embed=embed, ephemeral=False)
        a = b = c = 0

    if a != 0 and b != 0 and c == 0:
        while a > 0 or b > 0:
            if a > b:
                x = a - b
                a -= x
                embed = discord.Embed(title='🪨Ним🪨', description='Мой ход:',
                                      color=0xd1ff52)
                embed.add_field(name='\u200b', value=f'**🔸Я взял {x} {word2.make_agree_with_number(x).word}**',
                                inline=True)
                embed.add_field(name=f'🔸Из {1} кучи', value=f'------------------------', inline=False)
                # embed.add_field(name='------------------------', value='\u200b', inline=False)
                embed.add_field(name='1 куча:', value=f'{a} {word2.make_agree_with_number(a).word}', inline=True)
                embed.add_field(name='2 куча:', value=f'{b} {word2.make_agree_with_number(b).word}', inline=True)
            elif b > a:
                x = b - a
                b -= x
                embed = discord.Embed(title='🪨Ним🪨', description='Мой ход:',
                                      color=0xd1ff52)
                embed.add_field(name='\u200b', value=f'**🔸Я взял {x} {word2.make_agree_with_number(x).word}**',
                                inline=True)
                embed.add_field(name=f'🔸Из {2} кучи', value=f'------------------------', inline=False)
                # embed.add_field(name='------------------------', value='\u200b', inline=False)
                embed.add_field(name='1 куча:', value=f'{a} {word2.make_agree_with_number(a).word}', inline=True)
                embed.add_field(name='2 куча:', value=f'{b} {word2.make_agree_with_number(b).word}', inline=True)
            else:
                x = 1
                b -= x
                embed = discord.Embed(title='🪨Ним🪨', description='Мой ход:',
                                      color=0xd1ff52)
                embed.add_field(name='\u200b', value=f'**🔸Я взял {x} {word2.make_agree_with_number(x).word}**',
                                inline=True)
                embed.add_field(name=f'🔸Из {2} кучи', value=f'------------------------', inline=False)
                # embed.add_field(name='------------------------', value='\u200b', inline=False)
                embed.add_field(name='1 куча:', value=f'{a} {word2.make_agree_with_number(a).word}', inline=True)
                embed.add_field(name='2 куча:', value=f'{b} {word2.make_agree_with_number(b).word}', inline=True)
            if a == b == 0:
                embed.add_field(name='🏆Я выиграл!', value=f'А ты нет :)', inline=False)
                await ctx.send(embed=embed)
                break

            else:
                n = 0
                x = 0
                options = [
                    SelectOption(label='1', value='1'),
                    SelectOption(label='2', value='2')
                ]
                if a == 0:
                    del options[0]
                if b == 0:
                    del options[1]
                await ctx.send(
                    embed=embed,
                    components=[
                        Select(
                            placeholder=f"Выбери номер кучи!",
                            options=options,
                            custom_id='e',
                        )
                    ],
                )
                interaction = await bot.wait_for(
                    "select_option", check=lambda inter: inter.custom_id == "e")
                n = int(interaction.values[0])
                options = []
                if n == 1:
                    kk = a
                elif n == 2:
                    kk = b
                for i in range(1, kk + 1):
                    options.append(SelectOption(label=i, value=i))
                await interaction.send(
                    'Сколько камней хотите взять?',
                    components=[
                        Select(
                            placeholder=f"Выбери число камней!",
                            options=options,
                            custom_id='f',
                        )
                    ], ephemeral=False,
                )
                interaction = await bot.wait_for(
                    "select_option", check=lambda inter: inter.custom_id == "f")
                x = int(interaction.values[0])
                if n == 1:
                    a -= x
                    embed = discord.Embed(title='🪨Ним🪨', description='Твой ход:',
                                          color=0xd1ff52)
                    embed.add_field(name='\u200b', value=f'**🔸Ты взял {x} {word2.make_agree_with_number(x).word}**',
                                    inline=True)
                    embed.add_field(name=f'🔸Из {n} кучи', value=f'------------------------', inline=False)
                    # embed.add_field(name='------------------------', value='\u200b', inline=False)
                    embed.add_field(name='1 куча:', value=f'{a} {word2.make_agree_with_number(a).word}', inline=True)
                    embed.add_field(name='2 куча:', value=f'{b} {word2.make_agree_with_number(b).word}', inline=True)
                else:
                    b -= x
                    embed = discord.Embed(title='🪨Ним🪨', description='Твой ход:',
                                          color=0xd1ff52)
                    embed.add_field(name='\u200b', value=f'**🔸Ты взял {x} {word2.make_agree_with_number(x).word}**',
                                    inline=True)
                    embed.add_field(name=f'🔸Из {n} кучи', value=f'------------------------', inline=False)
                    # embed.add_field(name='------------------------', value='\u200b', inline=False)
                    embed.add_field(name='1 куча:', value=f'{a} {word2.make_agree_with_number(a).word}', inline=True)
                    embed.add_field(name='2 куча:', value=f'{b} {word2.make_agree_with_number(b).word}', inline=True)
                if a == b == 0:
                    embed.add_field(name='🏆Я выиграл!', value=f'А ты нет :)', inline=False)
                    await interaction.send(embed=embed, ephemeral=False)
                    break
                await interaction.send(embed=embed, ephemeral=False)
        a = b = 0
    if a != 0 and b == 0 and c == 0:
        while a != 0:
            if a % 4 == 1:
                x = 1
            elif a % 4 == 2:
                x = 2
            elif a % 4 == 3:
                x = 3
            else:
                x = 2
            if a == 1:
                x = 1
            elif a == 2:
                x = 2
            elif a == 3:
                x = 3
            a = a - x
            if a == 0:
                embed = discord.Embed(title='🪨Ним🪨', description='Мой ход:',
                                      color=0xd1ff52)
                embed.add_field(name='\u200b', value=f'**🔸Я взял {x} {word2.make_agree_with_number(x).word}**',
                                inline=True)
                embed.add_field(name=f'🔸Из единственной кучи', value=f'------------------------', inline=False)
                # embed.add_field(name='------------------------', value='\u200b', inline=False)
                embed.add_field(name='1 куча:', value=f'{a} {word2.make_agree_with_number(a).word}', inline=True)
                embed.add_field(name='🏆Я выиграл!', value=f'А ты нет :)', inline=False)
                await ctx.send(embed=embed)
                break
            else:
                embed = discord.Embed(title='🪨Ним🪨', description='Мой ход:',
                                      color=0xd1ff52)
                embed.add_field(name='\u200b', value=f'**🔸Я взял {x} {word2.make_agree_with_number(x).word}**',
                                inline=True)
                embed.add_field(name=f'🔸Из единственной кучи', value=f'------------------------', inline=False)
                # embed.add_field(name='------------------------', value='\u200b', inline=False)
                embed.add_field(name='1 куча:', value=f'{a} {word2.make_agree_with_number(a).word}', inline=True)
                options = [
                    SelectOption(label='1', value='1'),
                    SelectOption(label='2', value='2'),
                    SelectOption(label='3', value='3')
                ]
                if a == 2:
                    options = options[:-1]
                if a == 1:
                    options = options[0]
                await ctx.send(
                    'Сколько камней хотите взять?',
                    components=[
                        Select(
                            placeholder=f"Выбери число камней!",
                            options=options,
                            custom_id='h',
                        )
                    ], ephemeral=False,
                )
                interaction = await bot.wait_for(
                    "select_option", check=lambda inter: inter.custom_id == "h")
                x = int(interaction.values[0])
                a -= x
                if a == 0:
                    embed = discord.Embed(title='🪨Ним🪨', description='Твой ход:',
                                          color=0xd1ff52)
                    embed.add_field(name='\u200b', value=f'**🔸Ты взял {x} {word2.make_agree_with_number(x).word}**',
                                    inline=True)
                    embed.add_field(name=f'🔸Из единственной кучи', value=f'------------------------', inline=False)
                    # embed.add_field(name='------------------------', value='\u200b', inline=False)
                    embed.add_field(name='1 куча:', value=f'{a} {word2.make_agree_with_number(a).word}', inline=True)
                    embed.add_field(name='🏆Ты выиграл!', value=f'А я нет :(', inline=False)
                    await interaction.send(embed=embed, ephemeral=False)
                    break
                else:
                    embed = discord.Embed(title='🪨Ним🪨', description='Твой ход:',
                                          color=0xd1ff52)
                    embed.add_field(name='\u200b', value=f'**🔸Ты взял {x} {word2.make_agree_with_number(x).word}**',
                                    inline=True)
                    embed.add_field(name=f'🔸Из единственной кучи', value=f'------------------------', inline=False)
                    # embed.add_field(name='------------------------', value='\u200b', inline=False)
                    embed.add_field(name='1 куча:', value=f'{a} {word2.make_agree_with_number(a).word}', inline=True)
                    await interaction.send(embed=embed, ephemeral=False)
        a = 0


@bot.command()
async def pro(ctx):
    author = ctx.message.author
    await ctx.send(f'{author.mention}, отправил информацию вам в ЛС')

    embed = discord.Embed(title='👑 Salmon-pro', color=0xd1ff52)
    embed.add_field(name='🔰 Описание подписки:', value='С помощью этой подписки \
                вы сможете без труда \n __скачивать абсолютно любую музыку__, просто напишите боту `!dw (песня)`, \n \
                и бот __автоматически начнёт поиск и скачивание__, а потом отправит её вам в личные \
                сообщения. Вся процедура займёт __не более 15 секунд__, что намного быстрее, чем ручной поиск!',
                    inline=False)

    embed.add_field(name='\u200b', value='\u200b',
                    inline=False)

    embed.add_field(name='🧮 Тарифы:', value='🔸**1.** На одного человека **НА МЕСЯЦ** - 40р  \n \
                                            🔸**2**. На сервер с __любым количеством участников__ **НА МЕСЯЦ** - 180р',
                    inline=False)

    await author.send(
        embed=embed,
        components=[
            Select(
                placeholder="Выберите тариф",
                options=[
                    SelectOption(label="1. На одного человека", value="one"),
                    SelectOption(label="2. На весь сервер", value="all"),
                ],
                custom_id="tarif",
            )
        ],
    )

    interaction = await bot.wait_for(
        "select_option", check=lambda inter: inter.custom_id == "tarif"
    )
    if interaction.values[0] == 'one':
        embed = discord.Embed(title='👑 Salmon-pro', color=0xd1ff52)
        embed.add_field(name='💰Подписка для одного человека - 40р', value='\u200b',
                        inline=False)

        embed.add_field(name='🧾Итого: 40р', value='Выберете способ оплаты и следуйте дальнейшим инструкциям',
                        inline=False)

        await interaction.send(ephemeral=False, embed=embed)

        msg = await author.send(components=[[Button(label="🪙Юмани", custom_id="yoomoney", style=ButtonStyle.green),
                                             Button(label="💳Перевод по номеру карты", custom_id="card",
                                                    style=ButtonStyle.green)]])

        interaction = await bot.wait_for("button_click")
        if interaction.component.custom_id == 'yoomoney':
            embed = discord.Embed(title='👑 Salmon-pro', color=0xd1ff52)
            embed.set_thumbnail(url='http://qrcoder.ru/code/?https%3A%2F%2Fyoomoney.ru%2Fto%2F4100110960641547&4&0')
            embed.add_field(name='🪙Юмани', value='\u200b',
                            inline=False)

            embed.add_field(name='❗Обязательно', value=f'Поставьте галочку в строке\
            `Добавить назначение платежа` и введите туда это - **`{author.discriminator}`**, а \
                             в строку `Сколько` - 40!',
                            inline=False)
            embed.set_footer(text='Если вы хотите поменять способ оплаты, напишите !pro заново')

            await msg.delete()
            await interaction.send(embed=embed, ephemeral=False)
            await author.send(components=[
                [Button(label="🪙Юмани", url='https://yoomoney.ru/to/4100110960641547', style=ButtonStyle.URL)]])


        else:
            embed2 = discord.Embed(title='👑 Salmon-pro', color=0xd1ff52)
            embed2.add_field(name='💳Перевод по номеру карты', value='\u200b',
                             inline=False)
            embed2.set_thumbnail(
                url='http://qrcoder.ru/code/?https%3A%2F%2Fwww.tinkoff.ru%2Frm%2Fsavateev.dmitriy12%2FJgqwn3240&4&0')

            embed2.add_field(name='❗Обязательно', value=f'Напишите в строке `Сообщение` это - **`{author.discriminator}`**, \
                             в строке `Сумма` - 40!',
                             inline=False)
            embed2.set_footer(text='Если вы хотите поменять способ оплаты, напишите !pro заново')

            await msg.delete()
            await interaction.send(embed=embed2, ephemeral=False)
            await author.send(components=[[Button(label="💳Перевод по номеру карты",
                                                  url='https://www.tinkoff.ru/rm/savateev.dmitriy12/Jgqwn3240',
                                                  style=ButtonStyle.URL)]])

    else:
        embed = discord.Embed(title='👑 Salmon-pro', color=0xd1ff52)
        embed.add_field(name='💰Подписка на сервер - 180р', value='\u200b',
                        inline=False)

        embed.add_field(name='🧾Итого: 180р', value='Выберете способ оплаты и следуйте дальнейшим инструкциям',
                        inline=False)

        await interaction.send(ephemeral=False, embed=embed)

        msg = await author.send(components=[[Button(label="🪙Юмани", custom_id="yoomoney", style=ButtonStyle.green),
                                             Button(label="💳Перевод по номеру карты", custom_id="card",
                                                    style=ButtonStyle.green)]])

        interaction = await bot.wait_for("button_click")
        if interaction.component.custom_id == 'yoomoney':
            embed = discord.Embed(title='👑 Salmon-pro', color=0xd1ff52)
            embed.set_thumbnail(url='http://qrcoder.ru/code/?https%3A%2F%2Fyoomoney.ru%2Fto%2F4100110960641547&4&0')
            embed.add_field(name='🪙Юмани', value='\u200b',
                            inline=False)

            embed.add_field(name='❗Обязательно', value=f'Поставьте галочку в строке\
                        `Добавить назначение платежа` и введите туда это - **`{ctx.guild.id}`**, а\
                                         в строку `Сколько` - 180!',
                            inline=False)
            embed.set_footer(text='Если вы хотите поменять способ оплаты, напишите !pro заново')

            await msg.delete()
            await interaction.send(embed=embed, ephemeral=False)
            await author.send(components=[
                [Button(label="🪙Юмани", url='https://yoomoney.ru/to/4100110960641547', style=ButtonStyle.URL)]])

        if interaction.component.custom_id == 'card':
            try:
                embed2 = discord.Embed(title='👑 Salmon-pro', color=0xd1ff52)
                embed2.add_field(name='💳Перевод по номеру карты', value='\u200b',
                                 inline=False)
                embed2.set_thumbnail(
                    url='http://qrcoder.ru/code/?https%3A%2F%2Fwww.tinkoff.ru%2Frm%2Fsavateev.dmitriy12%2FJgqwn3240&4&0')

                embed2.add_field(name='❗Обязательно',
                                 value=f'Напишите в строке `Сообщение` это - **`{ctx.guild.id}`**, \
                                 в строке `Сумма` - 180!',
                                 inline=False)
                embed2.set_footer(text='Если вы хотите поменять способ оплаты, напишите !pro заново')

                await msg.delete()
                await interaction.send(embed=embed2, ephemeral=False)

                await author.send(components=[[Button(label="💳Перевод по номеру карты",
                                                      url='https://www.tinkoff.ru/rm/savateev.dmitriy12/Jgqwn3240',
                                                      style=ButtonStyle.URL)]])

            except:
                await author.send(
                    '❌Пожалуйста, напишите эту команду на сервере, для которого хотите подключить подписку!❌')

        # await interaction2.send(embed=embed2, ephemeral=False)


@bot.command()
async def ln(ctx):
    await ctx.send('Подбираю язык...')
    phrases = [
        'Привет! Меня зовут Лосось',
        'Мы играем в игру "угадай языки"',
        'Ты посоветуешь меня своим друзьям?)',
        'Может посмотрим фильм?',
        'Не смей даже думать о том, чтобы меня пожарить!',
        'Ты уже слушал мою музыку?'
    ]
    lng = [
        'Китайский',
        'Хинди',
        'Английский',
        'Испанский',
        'Бенгальский',
        'Португальский',
        'Японский',
        'Корейский',
        'Французский',
        'Яванский',
        'Телугу',
        'Маратхи',
        'Вьетнамский',
        'Тамильский',
        'Итальянский',
        'Турецкий',
        'Урду',
        'Панджаби',
        'Украинский',
        'Гуджарати',
        'Тайский',
        'Польский',
        'Малаялам',
        'Каннада',
        'Бирманский',
        'Азербайджанский',
        'Персидский',
        'Сунданский',
        'Пушту',
        'Румынский',
        'Бходжпури',
        'Хауса',
        'Малайский',
        'Сербохорватский',
        'Узбекский',
        'Йоруба',
        'Нидерландский',
        'Синдхи',
        'Игбо',
        'Амхарский',
        'Индонезийский',
        'Тагальский',
        'Непальский',
        'Ассамский',
        'Венгерский',
        'Читтагонг',
        'Чжуанский',
        'Марвари',
        'Харьянви',
        'Греческий',
        'Чешский',
        'Дакхни',
        'Малагасийский',
        'Белорусский'
    ]
    b = choice(lng)
    print(b)

    ln = GoogleTranslator(source='auto', target='english').translate(b).lower()
    phrase = choice(phrases)
    try:
        rphrase = GoogleTranslator(source='auto', target=ln).translate(phrase)
    except:
        del lng[lng.index(b)]
        b = choice(lng)
        print(b)
        ln = GoogleTranslator(source='auto', target='english').translate(b).lower()
        phrase = choice(phrases)
        rphrase = GoogleTranslator(source='auto', target=ln).translate(phrase)
    lngs = []
    while len(lngs) < 8:
        a = choice(lng)
        if a not in lngs and GoogleTranslator(source='auto', target='english').translate(a).lower() != ln:
            lngs.append(a)
    lngs.insert(random.randrange(9), b)
    lngs.append('Я не знаю(')
    embed = discord.Embed(title='🌍 Угадай язык', description='Выбери правильный вариант ответа',
                          color=0xff8534)
    embed.add_field(name='📖 Оригинальная фраза:', value=phrase, inline=False)
    embed.add_field(name='🪧 Переведенная фраза:', value=rphrase, inline=False)
    options = [SelectOption(label=lngs[i], value=lngs[i]) for i in range(9)]
    options.append(SelectOption(label=lngs[9], value=lngs[9]))
    await ctx.send(
        embed=embed,
        components=[
            Select(
                placeholder=f"Выберите язык, который считаете правильным!",
                options=options,
                custom_id='j',
            )
        ],
    )
    intr = await bot.wait_for(
        "select_option", check=lambda inter: inter.custom_id == "j")
    x = intr.values[0]
    if x == b:

        await intr.send('🙂 Вы молодец! Это правильный ответ!', ephemeral=False)
    elif x == 'Я не знаю(':
        await intr.send(f'🤷‍♂️ Это был {b} язык, попробуйте ещё раз!', ephemeral=False)
    else:
        await intr.send(f'😢 Неверно! Это {b} язык', ephemeral=False)


# Развлекательный бот с мини-играми, высококачественной музыкой от Яндекс Музыки и голосовым управлением
bot.run(settings['token'])
