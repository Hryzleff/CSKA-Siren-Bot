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

# Функция для воспроизведения аудио
async def play_audio(ctx, audio_file):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("Сначала зайдите в голосовой канал!")
        return
    
    voice_channel = ctx.author.voice.channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if voice_client:
        if voice_client.is_playing():
            voice_client.stop()
        await voice_client.move_to(voice_channel)
    else:
        voice_client = await voice_channel.connect()
    
    audio_source = discord.FFmpegPCMAudio(audio_file)
    if not audio_source:
        await ctx.send(f"Файл {audio_file} не найден!")
        await voice_client.disconnect()
        return
    
    voice_client.play(audio_source, after=lambda e: print(f'Завершено: {e}'))
    await ctx.send(f"Проигрывается: {audio_file}")
    
    while voice_client.is_playing():
        await asyncio.sleep(1)
    
    await voice_client.disconnect()

# Команды для разных аудиофайлов
@bot.command()
async def ebash(ctx):
    await play_audio(ctx, "cskasiren.mp3")

@bot.command()
async def tishe(ctx):
    await play_audio(ctx, "tishe.mp3")

# Запуск бота с токеном
bot.run(os.environ['DISCORD_BOT_TOKEN'])
