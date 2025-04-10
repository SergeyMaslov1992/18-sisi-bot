
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import re  # Для поиска ID в тексте

# Токен бота
TOKEN = '7806855143:AAFbt2TwbYp4JU9u_piT3yb7cLPJzUaWH2M'

# ID для отправки тебе заказов
OWNER_ID = 1368440460

# Клавиатура
menu = [["Что я умею"], ["Как заказать"], ["Задонатить"], ["Написать автору"]]
reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я пишу тексты за донат или за репост (первый заказ).\n\nВыбери, что тебя интересует:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    # Игнорировать сообщения от владельца и ответы на сообщения
    if user.id == OWNER_ID or update.message.reply_to_message:
        return

    if text == "Что я умею":
        await update.message.reply_text(
            "— Придумываю названия и слоганы\n"
            "— Пишу посты, статьи, описания\n"
            "— Помогаю с домашкой\n"
            "— Перевожу англ/рус\n"
            "\nПиши — помогу!"
        )

    elif text == "Как заказать":
        keyboard = [
            [InlineKeyboardButton("Репост бота", url="https://t.me/TextZaDonatBot")],
            [InlineKeyboardButton("Задонатить", url="https://www.sberbank.com/sms/pbpn?requisiteNumber=79775641805")]
        ]
        reply_markup_inline = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "1. Первый заказ — бесплатно за репост этого бота в свой канал/чат\n"
            "2. Последующие — после доната (от 10₽)\n"
            "3. Просто напиши задачу сюда — и я всё сделаю!",
            reply_markup=reply_markup_inline
        )

    elif text == "Задонатить":
        await update.message.reply_text(
            "Скинуть донат можно сюда:\n"
            "https://www.sberbank.com/sms/pbpn?requisiteNumber=79775641805"
        )

    elif text == "Написать автору":
        await update.message.reply_text("Пиши сюда: @sergoribak")

    else:
        msg_to_owner = (
            f"НОВЫЙ ЗАКАЗ от @{user.username or 'без username'}\n"
            f"Имя: {user.first_name}\n"
            f"ID: {user.id}\n"
            f"Сообщение:\n{text}"
        )
        await context.bot.send_message(chat_id=OWNER_ID, text=msg_to_owner)
        await update.message.reply_text("Спасибо! Задача отправлена автору. Ответ скоро прилетит!")

async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id == OWNER_ID and update.message.reply_to_message:
        reply_text = update.message.text
        original_text = update.message.reply_to_message.text

        match = re.search(r'ID:\s*(\d+)', original_text)
        if match:
            user_id = int(match.group(1))
            await context.bot.send_message(chat_id=user_id, text=reply_text)
            await update.message.reply_text("Ответ отправлен клиенту.")
        else:
            await update.message.reply_text("Не удалось найти ID пользователя в сообщении.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.User(OWNER_ID), reply_to_user))  # Важнее
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
