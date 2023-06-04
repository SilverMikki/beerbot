from __future__ import unicode_literals
import asyncio
from asyncore import dispatcher
from cgitb import handler
import datetime
from random import randint
import time
from aiogram import Bot, types
from aiogram import Dispatcher, Router
import sqlite3
import mysql.connector
from pytube import YouTube
import os
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import yt_dlp as youtube_dl
from youtubesearchpython import VideosSearch
import pprint
import os
import spotdl
import concurrent.futures
from pathlib import Path
from aiogram.types import Audio
import random
import subprocess
from aiogram.filters import Command
from aiogram.types import FSInputFile


token = "1855074508:AAEFuvZkVIgZy0SB18dXRe2JK2xBV66O2eQ"
spotify_cleint_id = ('a80a3df5206a4f33962b0ded511276cb')
spotify_client_secret_id = ('6af5aeb40bbf4a57a25b32a89303b04b')
auth_manager = SpotifyClientCredentials(client_id=spotify_cleint_id, client_secret=spotify_client_secret_id)
spotify = spotipy.Spotify(auth_manager=auth_manager)
router = Router()

spot = spotdl.Spotdl(client_id='a80a3df5206a4f33962b0ded511276cb', client_secret='6af5aeb40bbf4a57a25b32a89303b04b')

def download_song(song_id):
    # Create an instance of spotdl.Downloader
    
    #spot1 = spotdl.Downloader()

    try:
        # Download the song
        song1 = spotdl.Song.from_url(song_id)
        song = spot.downloader.download_song(song1)
    except Exception as e:
        print(str(e))

async def download_song_async(song_id):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, download_song, song_id)
        return result
    
async def download_song(url):
    try:
        # Опции для youtube_dl
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl': '%(title)s.%(ext)s',
            'ffmpeg_location': 'C:\\Users\\choco\\.spotdl'
            }
        
        # Загрузка аудио с помощью youtube_dl
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            ydl.download([url])
        
        # Возвращение пути к загруженному файлу
        return f"{info['title']}.mp3"
    except Exception as e:
        print(f'Error downloading song: {e}')
        return None

@router.message(Command(commands=['spotify']))
async def spotify_download(message: types.Message):
    url = message.text.replace('/spotify ', '')
    parsed_url = url.replace("https://open.spotify.com/", "").split("/")
    #print(parsed_url[0],parsed_url[1].split("?")[0])
    text = "spotify:track:" + str(parsed_url[1].split("?")[0])
    #print(text)
    item = spotify.track(track_id=parsed_url[1].split("?")[0])
    track_name = item['name']
    pprint.pprint(item['uri'])
    #pprint.pprint(text)
    #print(track_name)
    #success = await download_song_async(url)
    alb = spotify.album(album_id=item['album']['id'],)
    #download_song(url)
    #print(item['name'] + ' - ' + item['artists'][0]['name'] + '.mp3')
    #while not os.path.exists(str(item['artists'][0]['name'] + ' - ' + item['name'] + '.mp3')):
    #    time.sleep(5)
    #file1 = types.InputFile(str(item['artists'][0]['name'] + ' - ' + item['name'] + '.mp3'), str(item['artists'][0]['name'] + ' - ' + item['name'] + '.mp3'))
    #file = types.InputMediaAudio(str(item['artists'][0]['name'] + ' - ' + item['name'] + '.mp3'))
    await message.reply_photo(photo=alb['images'][0]['url'], caption=f"🎧 Title : `{item['name']}`\n🎤 Artist : `{item['artists'][0]['name']}`\n💽 Album : `{alb['name']}`\n🗓 Release Year: `{alb['release_date']}`\nTrack id: `{item['id']}`", parse_mode="Markdown")
    await message.reply_audio(audio=f"{item.get('preview_url')}")
    
    #await bot.send_audio(chat_id=message.chat.id, audio=file1.get_file())
    #os.remove(file1.get_file())

@router.message(Command(commands=['youtube']))
async def music_download(message: types.Message):
    try:
        text = message.text.replace('/youtube ', '')
        song_file = await download_song(text)
        print(song_file)
        if song_file:
            file = FSInputFile(song_file)
            await message.reply_audio(audio=file)
        
        # Удалите загруженный файл после отправки
            os.remove(song_file)
        else:
        # Сообщите пользователю об ошибке загрузки
            await message.reply('Не удалось загрузить песню.')
    except Exception as e:
        print(e)
        

@router.message()
async def message_controller(message: types.Message):
    text = message.text.lower()
    if 'пиво' in text.lower() or 'пива' in text.lower():
        arr_beer = ['пей пиво на заре, пей пиво перед сном!', 'пей пиво пенным, будет пузо здоровенным!', 'Лучше пузо от пива, чем горб от работы', 
                    'Ничто так не согревает душу, как холодное пиво', 'Что вы выберете — пиво или спасение души?', 'лучше выпить пива литр, чем лизать солёный клитор!',
                    'бабы шлюхи, бабы бляди, а пиво всегда пенное, прохладное. такое вкусное, такое стабильное...',
                    'Хто п\'є пиво, той добре спить. Хто добре спить, той не може грішити. Хто не грішить, той потрапляє в рай. Амінь.',
                    'Після перемоги ти заслуговуєш на пиво, після поразки воно тобі необхідне', 'Якщо пиво не розв\'язує твої проблеми, то, мабуть, ти п\'єш занадто повільно.',
                    'Я не п\'ю пиво, я проводжу з ним якісний час.', 'Пиво - це мій основний вітамін B(eer).', 'пиво - це вирішення багатьох проблем, наприклад, недостаток пива.',
                    'Хто сказав, що за гроші не купиш щастя? Спробуйте купити пиво і не посміхнутись!', 'Пивний закон: кожен, хто випиває одну пляшку, автоматично виробляє потребу у ще одній.']
        num = len(arr_beer) - 1
        await message.answer(arr_beer[random.randint(0, num)])

    if text == 'здарова':
        await message.send_message(message.chat.id, "может по пивку?")

async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token, parse_mode="Markdown")
    # And the run events dispatching
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    try:
        print('[+] Starting the telegram bot...')
        asyncio.run(main())
    except KeyboardInterrupt:
            print('[+] Quiting bot...\n')
            exit()