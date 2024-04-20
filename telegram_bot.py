from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes


class TelegramWeatherBot:
    def __init__(self,token,bot_username):
        self.token = token
        self.bot_username = bot_username
        self.subscribed_id = []
        print("Starting bot...")
        app = Application.builder().token(token).build()
        app.add_handler(CommandHandler('start',self.start_command))
        app.add_handler(CommandHandler('help',self.help_command))
        app.add_handler(CommandHandler('weather',self.weather_command))
        app.add_handler(CommandHandler('auto',self.auto_command))
        app.add_handler(CommandHandler('stop',self.stop_command))

        job_queue = app.job_queue
        self.job_minute = job_queue.run_repeating(self.callback_minute,interval=60,first=10)
        app.add_handler(MessageHandler(filters.TEXT,self.handle_message))
        app.add_error_handler(self.error)
        print("Polling...")
        app.run_polling(poll_interval=3,)

    async def start_command(self,update: Update, context:ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hola :)")

    async def help_command(self,update: Update, context:ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hola te ayudo")

    async def weather_command(self,update: Update, context:ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hoy esta soleado")

    async def auto_command(self,update: Update, context:ContextTypes.DEFAULT_TYPE):
        self.subscribed_id.append(context._chat_id)
    async def stop_command(self,update: Update, context:ContextTypes.DEFAULT_TYPE):
        self.subscribed_id.remove(context._chat_id)


    def handle_response(self,text: str) -> str:
        processed = text.lower()
        if 'hola' in processed:
            return "Hola!"
        if 'clima' in processed:
            return "El clima hoy es ---"
        if 'chau' in processed:
            return "Chau nos vemos!"
        else:
            return "No entendi :("
        
    async def handle_message(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_tpe:str = update.message.chat.type
        text: str = update.message.text
        self.chat_id = update.message.chat_id
        print(f'User ({update.message.chat.id}) in {message_tpe}: {text}')
        if(message_tpe == 'group'):
            if BOT_USERNAME in text:
                new_text: str = text.replace(BOT_USERNAME,'').strip()
                response: str = self.handle_response(new_text)
            else:
                return
        else :
            response : str = self.handle_response(text)
        print('Bot',response)
        await update.message.reply_text(response)

    async def callback_minute(self,context: ContextTypes.DEFAULT_TYPE):
        for chat_id in self.subscribed_id:
            await context.bot.send_message(chat_id=chat_id,text="Mensaje automatico!")

    async def error(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'Update {update} cause error {context.error}')

    

