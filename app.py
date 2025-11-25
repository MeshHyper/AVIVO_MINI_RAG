from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler
from src.generator import generator   

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I'm ready.\nUse /ask, /image, or /help."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/ask <question> – Ask the RAG engine\n"
        "/image – Upload an image for description\n"
        "/help – Show usage instructions"
    )


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    full_text = update.message.text
    question = full_text.replace("/ask", "", 1).strip()

    if not question:
        await update.message.reply_text("Please write a question after /ask.")
        return

    try:
        answer = generator(question)
    except Exception as e:
        answer = f"Error in RAG: {str(e)}"

    await update.message.reply_text(answer)



async def cancel_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END


def main():
    app = ApplicationBuilder().token("8078660648:AAGvZpLDm19QlhOUihxndIPY0L85J_gdrNc").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ask", ask))

    app.run_polling()


if __name__ == "__main__":
    main()
