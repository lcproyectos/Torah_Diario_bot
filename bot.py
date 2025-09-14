import os
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

with open('parashot.json', 'r', encoding='utf-8') as f:
    parashot_data = json.load(f)

parashot_keys = list(parashot_data.keys())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Bienvenido al Bot de la Torá!\n\n"
        "Escribe el nombre de una *Parashat* (ej: 'Bereshit', 'Noaj')\n"
        "o pregunta algo como: '¿Qué dice la Torá sobre la creación?'"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Comandos disponibles:\n"
        "/start - Iniciar\n"
        "/current - Parashat de esta semana\n"
        "Escribe el nombre de una parashat (ej: 'Vayera') para saber más.\n"
        "También puedes preguntar: '¿Qué es la Torá?'"
    )

async def current_parashah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_week = "bereshit"
    data = parashot_data.get(current_week)
    if data:
        response = (
            f"🌟 *Parashat de la semana: {data['name']} ({data['hebrew']})*\n\n"
            f"📖 Versículos: {data['verses']}\n\n"
            f"📝 Resumen: {data['summary']}\n\n"
            f"💡 Lección clave: {data['key_lesson']}"
        )
        await update.message.reply_text(response, parse_mode='Markdown')
    else:
        await update.message.reply_text("No pude encontrar la parashat actual. Intenta escribir el nombre.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()

    for key in parashot_keys:
        if key in text or parashot_data[key]['name'].lower() in text:
            data = parashot_data[key]
            response = (
                f"🌟 *{data['name']} ({data['hebrew']}) *\n\n"
                f"📖 Versículos: {data['verses']}\n\n"
                f"📝 Resumen: {data['summary']}\n\n"
                f"💡 Lección clave: {data['key_lesson']}"
            )
            await update.message.reply_text(response, parse_mode='Markdown')
            return

    if "torá" in text or "torah" in text:
        await update.message.reply_text(
            "La Torá (תורה) es el conjunto de los cinco libros de Moisés: Génesis, Éxodo, Levítico, Números y Deuteronomio. "
            "Es la base de la ley judía y contiene 613 mandamientos. Se lee en sinagogas cada semana en una porción llamada Parashat haShavua."
        )
    elif "creación" in text:
        await update.message.reply_text(
            "Según la Torá, Dios creó el mundo en seis días y descansó el séptimo. En el primer día creó la luz, "
            "en el segundo el firmamento, en el tercero la tierra y plantas, en el cuarto sol y estrellas, "
            "en el quinto animales marinos y aves, y en el sexto animales terrestres y al ser humano a Su imagen."
        )
    else:
        await update.message.reply_text(
            "Lo siento, no entendí tu pregunta. 😊\n"
            "Prueba preguntando por una parashat, como 'Bereshit' o 'Noaj'.\n"
            "O usa /current para ver la parashat de esta semana."
        )

def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("❌ No se encontró el token de Telegram. Configúralo en Render.com como variable de entorno.")
    
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("current", current_parashah))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot de la Torá iniciado en la nube... ¡Funcionando 24/7!")
    application.run_polling()

if __name__ == '__main__':
    main()