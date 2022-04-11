import logging
import os
import random
import traceback

# from discord_components import DiscordComponents, Button, ButtonStyle
# from voice import voice
import aiohttp
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
from discord_buttons_plugin import *

# from discord.ext.audiorec import NativeVoiceClient
from bulls_and_cows import bulls_and_cows
from config import settings
from yandex_music import ClientAsync, Client

client = ClientAsync()
client.init()
client = Client(settings['token_ya'])
logging.basicConfig(level=logging.INFO)

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
DONATE = ['0891', '0603']

cycles = dict(game=True)
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
bot = commands.Bot(command_prefix=settings['prefix'])
buttons = ButtonsClient(bot)
bot.remove_command('help')
queues = {}
music_id = []
bot_queue = []

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
            await ctx.send(traceback.format_exc())

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
            await ctx.send(traceback.format_exc())
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
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command!")
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
                        custom_id="stop_button"# Refer to line 21
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
                    await ctx.send(traceback.format_exc())
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
                        await ctx.send(traceback.format_exc())

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
                        await ctx.send(traceback.format_exc())
                    print('скачал трек')

                    voice = ctx.voice_client
                    source = FFmpegPCMAudio(f'{path}/{song}')
                    voice.play(source, after=lambda x=0: check_queue(ctx, ctx.message.guild.id))
                    print('начал проигрывать песню')


            # except:
            #     print('ошибка в 123 строке')
        else:
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command!")

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
    if author.discriminator in DONATE:
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
            client.tracks([f'{search_result.best.result.id}:{search_result.best.result.albums[0].id}'])[0].download(
                os.path.join(f'{path}/{dw_song}'))
        except Exception as e:
            await ctx.send(traceback.format_exc())

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

        await ctx.send(f'{author.mention}, отправил в Личные сообщения')
        await author.send(embed=embed)
        await author.send(file=discord.File(f'{path}/{"".join(DW_SONG)}'))

        os.remove(f'{path}/{"".join(DW_SONG)}')
        DW_SONG.clear()
    else:
        await ctx.send(f'{author.mention}, Для выполнения этой команды требуется **Премиум!**')


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
    embed = discord.Embed(title='Очередь музыки:',
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
    print(ctx.guild.id)


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


# Развлекательный бот с мини-играми, высококачественной музыкой от Яндекс Музыки и голосовым управлением
bot.run(settings['token'])  # Обращаемся к словарю settings с ключом token, для получения токена
