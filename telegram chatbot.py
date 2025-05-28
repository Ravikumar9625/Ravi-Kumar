import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters


OPEN_WEATHER_API_KEY = "e73c2cd7e6048afad5bc41df1a6d1a8c"


BOT_TOKEN = "7150781796:AAG_Kq_kcanuWWJ3QL7G1H_eAGvEmPy_be5Nw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌤 Привет! Напиши название города, и я покажу тебе погоду там.")

async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    await update.message.reply_text(f"🔍 Ищу погоду в городе: {city}")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={'e73c2cd7e6048afad5bc41df1a6d1a8c'}&units=metric&lang=ru"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            await update.message.reply_text('❌ Город не найден. Попробуй снова.')
            return

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]

        msg = (
            f'🌍 Погода в городе: {city}\n'
            f'🌦 {weather.capitalize()}\n'
            f'🌡 Температура: {temp}°C (ощущается как {feels_like}°C)\n'
            f'💧 Влажность: {humidity}%'
        )
        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather))

    print("🤖 Бот запущен...")
    app.run_polling()
