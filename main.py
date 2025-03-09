import discord
from discord.ext import commands
import asyncio
import os
import nacl.utils  # PyNaCl import


# Укажи префикс команд и intents
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="sirena", intents=intents)

# Проверяем готовность бота
@bot.event
async def on_ready():
    print(f'Бот {bot.user} запущен!')

# Подключаемся к голосовому каналу и проигрываем локальный трек
@bot.command()
async def ebash(ctx):
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.send("Сначала зайдите в голосовой канал!")
        return

    voice_client = await voice_channel.connect()

    # Воспроизведение локального файла
    audio_source = discord.FFmpegPCMAudio("cskasiren.mp3")
    if not audio_source:
        await ctx.send("Файл cskasiren.mp3 не найден!")
        await voice_client.disconnect()
        return

    voice_client.play(audio_source, after=lambda e: print('Завершено', e))
    await ctx.send("Воспроизводится: cskasiren.mp3")

    while voice_client.is_playing():
        await asyncio.sleep(1)

    await voice_client.disconnect()

# Запусти бота с токеном из переменных окружения
bot.run(os.environ['DISCORD_BOT_TOKEN'])