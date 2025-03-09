import discord
from discord.ext import commands
import asyncio
import os
from flask import Flask
from threading import Thread

# Укажи префикс команд и intents
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="sirena", intents=intents)

# Запускаем Flask-сервер для UptimeRobot
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает жестко!"

def run():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run).start()

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
    audio_source = discord.FFmpegPCMAudio("cskasirennew.mp3")
    if not audio_source:
        await ctx.send("Файл cskasiren.mp3 не найден!")
        await voice_client.disconnect()
        return

    voice_client.play(audio_source, after=lambda e: print('Завершено', e))
    await ctx.send("ДАЙТЕ ШУМУ БРАТЦЫ :pray: :pray: :pray: ")

    while voice_client.is_playing():
        await asyncio.sleep(1)

    await voice_client.disconnect()

# Запусти бота с токеном из переменных окружения
bot.run(os.environ['DISCORD_BOT_TOKEN'])
