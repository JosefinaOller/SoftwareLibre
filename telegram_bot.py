from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes

TOKEN = '7007180975:AAFK3P7eOyonHF5pSj_vStvWrGluN3Fohb8'
BOT_USERNAME = '@joelcoyos_bot'

async def start_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola :)")

async def help_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola te ayudo")

async def weather_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hoy esta soleado")

def handle_response(text: str) -> str:
    processed = text.lower()
    if 'hola' in processed:
        return "Hola!"
    if 'clima' in processed:
        return "El clima hoy es ---"
    if 'chau' in processed:
        return "Chau nos vemos!"
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_tpe:str = update.message.chat.type
    text: str = update.message.text
    print(f'User ({update.message.chat.id}) in {message_tpe}: {text}')

    if(message_tpe == 'group'):
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME,'').strip()
            response: str = handle_response(new_text)
        else:
            return
    else :
        response : str = handle_response(text)
    print('Bot',response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} cause error {context.error}')

if(__name__ == '__main__'):
    print("Starting bot...")

    app = Application.builder().token(TOKEN).build()

    #app.add_handler(CommandHandler('start',start_command))
    #app.add_handler(CommandHandler('help',help_command))
    #app.add_handler(CommandHandler('weather',weather_command))

    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3,)
