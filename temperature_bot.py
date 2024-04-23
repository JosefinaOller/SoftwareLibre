import os
from threading import Thread
import telebot
import logging, logging.config
from geopy.geocoders import Nominatim
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import configparser
import syslog

from weather import Weather

class TelegramWeatherBot():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.BOT_TOKEN = self.config.get('Tokens','telegram_token')
        print(self.BOT_TOKEN)
        self.WEATHER_TOKEN = self.config.get('Tokens','weather_token')
        self.bot = telebot.TeleBot(self.BOT_TOKEN)
        self.weather = Weather(self.WEATHER_TOKEN)
        self.command_handler()

        self.subscribed_dict = {}

        logging.basicConfig(filename='weather.log',
                    filemode='a',
                    format='%(levelname)s %(asctime)s,%(msecs)d %(name)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

        logging.info("Weather Telegram")
        self.logger = logging.getLogger(__name__)

        self.scheduler = BlockingScheduler()
        auto_hour = self.config.get('Weather','hour')
        auto_minute = self.config.get('Weather','minute')
        #self.scheduler.add_job(self.send_automatic_weather,"cron",hour=auto_hour,min=auto_minute)
        #self.scheduler.add_job(self.send_automatic_weather,"interval",minutes=1)
        Thread(target=self.schedule_checker).start()

        print('Starting...')

        print("Starting polling...")
        self.bot.infinity_polling()

    def schedule_checker(self):
        while True:
            self.scheduler.start()

    def command_handler(self):
        @self.bot.message_handler(commands=['hola'])
        def send_welcome(message):
            self.bot.send_message(message.chat.id, 'Hola!!')
            logging.info('Llego un comando /hola desde ' + str(message.chat.id))

        @self.bot.message_handler(commands=['clima'])
        def send_weather(message):
            location = '¿Qué ciudad te interesa? '
            logging.info('Llego un comando /clima desde ' + str(message.chat.id))
            sent_message = self.bot.send_message(message.chat.id, location, parse_mode='Markdown')
            self.bot.register_next_step_handler(sent_message, callback=self.send_weather)
            return location
        
        @self.bot.message_handler(commands=['auto'])
        def auto_weather(message):
            logging.info('Llego un comando /auto desde ' + str(message.chat.id))
            self.bot.send_message(message.chat.id, 'Te estas subscribiendo al sistema automatico')
            sent_message = self.bot.send_message(message.chat.id, '¿Qué ciudad te interesa?')
            self.bot.register_next_step_handler(sent_message, callback=self.subscribe_weather)
        
        @self.bot.message_handler(func=lambda msg: True)
        def echo_all(message):
            self.bot.send_message(message.chat.id, 'No entendi :(')

    def send_weather(self,message):
        logging.info('El usuario selecciono la ciudad ' + str(message.text))
        weather_message = self.weather.fetch_weather(message.text)
        self.bot.send_message(message.chat.id, 'Ahí está el clima!')
        self.bot.send_message(message.chat.id, weather_message, parse_mode='Markdown')
        url = 'https://openweathermap.org/img/wn/{}@2x.png'.format('10n')
        self.bot.send_photo(message.chat.id, photo= url)

    def send_automatic_weather(self):
        for chat_id,location in self.subscribed_dict.items():
            weather_message = self.weather.fetch_weather(location)
            self.bot.send_message(chat_id, 'Ahí está el clima!')
            self.bot.send_message(chat_id, weather_message, parse_mode='Markdown')
            url = 'https://openweathermap.org/img/wn/{}@2x.png'.format('10n')
            self.bot.send_photo(chat_id, photo= url)

    def subscribe_weather(self,message):
        logging.info('El usuario se suscribio a la ciudad ' + str(message.text))
        self.subscribed_dict[message.chat.id] = message.text
        self.bot.send_message(message.chat.id, 'Te subscribiste al sistema automatico!')

    def echo_all(self,message):
        '''
        echoes back any other messages bot receives from user
        '''
        self.bot.reply_to(message, message.text)

weatherbot = TelegramWeatherBot()
#create_config()