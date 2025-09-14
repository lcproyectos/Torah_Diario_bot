import os
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

# Cargar datos de las parashot
with open('parashot.json', 'r', encoding='utf-8') as f:
    parashot_data = json.load(f)

parashot_keys = list(parashot_data.keys())

def start(update: Update, context):
    update.message.reply_text(
        "👋 ¡Bienvenido al Bot de la Torá!\n\n"
        "Escribe el nombre de una *Parashat* (ej: 'Bereshit', 'Noaj')\n"
        "o pregunta algo como: '¿Qué dice la Torá sobre la creación?'"
    )

def help_command(update: Update, context):
    update.message.reply_text(
        "📌 Comandos disponibles:\n"
        "/start - Iniciar el bot\n"
        "/current - Ver la parashat de esta semana\n\n"
        "También puedes escribir el nombre de una parashat (ej: 'Vayera') para obtener información.\n"
        "O preguntar: '¿Qué es la Torá?'"
    )

def current_parashah(update: Update, context):
    # Puedes automatizar esto con fecha si lo deseas
    current_week = "bereshit"
    data = parashot_data.get(current_week)
    if data:
        response = (
            f"🌟 *Parashat de la semana: {data['name']} ({data['hebrew']})*\n\n"
            f"📖 Versículos: {data['verses']}\n\n"
            f"📝 Resumen: {data['summary']}\n\n"
            f"💡 Lección clave: {data['key_lesson']}"
        )
        update.message.reply_text(response, parse_mode='Markdown')
    else:
        update.message.reply_text("⚠️ No pude encontrar la parashat actual. Intenta escribir el nombre.")

def handle_message(update: Update, context):
    text = update.message.text.strip().lower()

    for key in parashot_keys:
        if key in text or parashot_data[key]['name'].lower() in text:
            data = parashot_data[key]
            response = (
                f"🌟 *{data['name']} ({data['hebrew']})*\n\n"
                f"📖 Versículos: {data['verses']}\n\n"
                f"📝 Resumen: {data['summary']}\n\n"
                f"💡 Lección clave: {data['key_lesson']}"
            )
            update.message.reply_text(response, parse_mode='Markdown')
            return

    if "torá" in text or "torah" in text:
        update.message.reply_text(
            "📚 La Torá (תורה) es el conjunto de los cinco libros de Moisés: Génesis, Éxodo, Levítico, Números y Deuteronomio.\n"
            "🕊️ Es la base de la ley judía y contiene 613 mandamientos.\n"
            "📖 Se lee cada semana en una porción llamada *Parashat haShavua*."
        )
    elif "creación" in text:
        update.message.reply_text(
            "🌍 Según la Torá, Dios creó el mundo en seis días y descansó el séptimo:\n"
            "1️⃣ Luz\n2️⃣ Firmamento\n3️⃣ Tierra y plantas\n4️⃣ Sol, luna y estrellas\n"
            "5️⃣ Animales marinos y aves\n6️⃣ Animales terrestres y el ser humano a Su imagen."
        )
    else:
        update.message.reply_text(
            "🤔 Lo siento, no entendí tu pregunta.\n"
            "Prueba escribiendo el nombre de una parashat como 'Bereshit' o 'Noaj'.\n"
            "O usa /current para ver la parashat de esta semana."
        )

def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("❌ No se encontró el token de Telegram. Configúralo en tu entorno.")

    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("current", current_parashah))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot de la Torá iniciado...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
