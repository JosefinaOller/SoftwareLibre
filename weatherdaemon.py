from daemon import daemon
from telegram_bot import TelegramWeatherBot

class WeatherDaemon(daemon):
    def __init__(self, pidfile,token,bot_id):
        super().__init__(pidfile)
        self.token = token
        self.bot_id = bot_id
    
    def run(self):
        self.weatherbot = TelegramWeatherBot(self.token,self.bot_id)