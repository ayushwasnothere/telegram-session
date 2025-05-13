import os

from dotenv import load_dotenv
from pyrogram.client import Client as PyroClient
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") or ""
API_ID = os.getenv("API_ID") or 2
API_HASH = os.getenv("API_HASH") or ""

SELECTING_LIB, PHONE_NUMBER, CODE = range(3)

CANCEL_BUTTON = KeyboardButton("❌ Cancel")
EXCLUDE_REGEX = filters.Regex(r"^❌ Cancel|🔁 Again$")

HELP_MESSAGE = (
    "🤖 *Telegram Session Generator Help*\n\n"
    "This bot helps you generate session strings for *Telethon* and *Pyrogram* libraries.\n\n"
    "📋 *Available Commands:*\n"
    "/start – Start the bot and choose between Telethon or Pyrogram\n"
    "/generate – Begin the session string generation process\n"
    "/cancel – Cancel the current operation at any time\n"
    "/help – Show this help message\n\n"
    "💡 *How It Works:*\n"
    "1. Choose the library: ⚡ Telethon or 🔥 Pyrogram\n"
    "2. Enter your phone number (e.g., `+911234567890`)\n"
    "3. Enter the verification code sent to your Telegram app\n"
    "4. You'll receive your session string to use in your scripts\n\n"
    "⚠️ *Note:* Keep your session string private. It grants full access to your Telegram account.\n\n"
    "Built with ❤️ for developers."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    buttons = [
        [KeyboardButton("⚡ Telethon")],
        [KeyboardButton("🔥 Pyrogram")],
    ]
    await update.message.reply_text(
        "Welcome! Please select a library:",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
    )
    return SELECTING_LIB


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text(HELP_MESSAGE, parse_mode="Markdown")


async def choose_lib(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    lib = str(update.message.text).strip()
    if lib not in ["⚡ Telethon", "🔥 Pyrogram"]:
        await update.message.reply_text(
            "Please choose a valid option.",
            reply_markup=ReplyKeyboardMarkup([[CANCEL_BUTTON]], resize_keyboard=True),
        )
        return SELECTING_LIB
    context.user_data["lib"] = lib
    await update.message.reply_text(
        "Enter your phone number (e.g., +911234567890):",
        reply_markup=ReplyKeyboardMarkup([[CANCEL_BUTTON]], resize_keyboard=True),
    )
    return PHONE_NUMBER


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not context.user_data:
        return
    context.user_data["phone"] = str(update.message.text).strip()
    lib = context.user_data["lib"]

    try:
        if lib == "⚡ Telethon":
            client = TelegramClient(StringSession(), int(API_ID), API_HASH)
            await client.connect()
            await client.send_code_request(context.user_data["phone"])
            context.user_data["client"] = client
        else:
            client = PyroClient(
                name=":memory:",
                api_id=API_ID,
                api_hash=API_HASH,
            )
            await client.connect()
            code_hash = await client.send_code(context.user_data["phone"])
            context.user_data["code_hash"] = code_hash
            context.user_data["client"] = client

        await update.message.reply_text(
            "Code sent! Now enter the code you received:",
            reply_markup=ReplyKeyboardMarkup([[CANCEL_BUTTON]], resize_keyboard=True),
        )
        return CODE
    except Exception as e:
        await update.message.reply_text(
            f"❌ Unexpected Error. Try again",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END


async def get_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not context.user_data:
        return
    code = str(update.message.text).strip()
    lib = context.user_data["lib"]
    phone = context.user_data["phone"]
    client = context.user_data["client"]
    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton("🔁 Again")]], resize_keyboard=True
    )

    try:
        if lib == "⚡ Telethon":
            await client.sign_in(phone=phone, code=code)
            session_str = client.session.save()
            await client.disconnect()
            await update.message.reply_text(
                f"✅ *Telethon session string:*\n```\n{session_str}\n```",
                parse_mode="Markdown",
                reply_markup=reply_markup,
            )
        else:
            await client.sign_in(
                phone_number=phone,
                phone_code_hash=context.user_data["code_hash"].phone_code_hash,
                phone_code=code,
            )
            session_str = client.export_session_string()
            await client.stop()
            await update.message.reply_text(
                f"✅ *Pyrogram session string:*\n```\n{session_str}\n```",
                parse_mode="Markdown",
                reply_markup=reply_markup,
            )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error: {str(e)}", reply_markup=ReplyKeyboardRemove()
        )

    return ConversationHandler.END


async def again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    buttons = [
        [KeyboardButton("⚡ Telethon")],
        [KeyboardButton("🔥 Pyrogram")],
    ]
    await update.message.reply_text(
        "Let's try again!\nPlease select a library:",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
    )
    return SELECTING_LIB


async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    buttons = [
        [KeyboardButton("⚡ Telethon")],
        [KeyboardButton("🔥 Pyrogram")],
    ]
    await update.message.reply_text(
        "Let's generate a string!\nPlease select a library:",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
    )
    return SELECTING_LIB


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text("❌ Cancelled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("generate", generate),
        ],
        states={
            SELECTING_LIB: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND & ~EXCLUDE_REGEX, choose_lib
                )
            ],
            PHONE_NUMBER: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND & ~EXCLUDE_REGEX, get_phone
                )
            ],
            CODE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND & ~EXCLUDE_REGEX, get_code
                )
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("again", again),
            MessageHandler(filters.TEXT & filters.Regex("^❌ Cancel$"), cancel),
            MessageHandler(filters.TEXT & filters.Regex("^🔁 Again$"), again),
        ],
        allow_reentry=True,
        conversation_timeout=600,
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("help", help))
    app.run_polling()


if __name__ == "__main__":
    main()
