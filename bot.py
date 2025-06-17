import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from analyze_all import NganasanMorphAnalyzer


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class NganasanBot:
    def __init__(self, token):
        self.token = token
        self.analyzer = NganasanMorphAnalyzer()

    async def start(self, update: Update, context):
        """Обработчик команды /start"""
        welcome_text = (
            "👋 Привет! Я бот для морфологического разбора нганасанских слов.\n"
            "Просто пришли мне слово на нганасанском, и я его разберу.\n\n"
        )
        await update.message.reply_text(welcome_text)

    async def help_command(self, update: Update, context):
        """Обработчик команды /help"""
        help_text = (
            "📖 Справка по использованию бота:\n\n"
            "1. Пришлите любое слово на нганасанском языке\n"
            "2. Бот вернет его морфологический разбор\n\n"
            "Примеры анализируемых частей речи:\n"
            "- Существительные: таа, таагай, десьмё\n"
            "- Глаголы: ту\"ом, туйсузәм\n"
            "- Местоимения: мәне, нонәнте\n"
            "- Числительные: ситти"
        )
        await update.message.reply_text(help_text)

    async def example_command(self, update: Update, context):
        """Обработчик команды /example"""
        examples = {
            "таа": "NOUN, nom.sg - 'олень'",
            "таагай": "NOUN, dl - 'два оленя'",
            "ту\"ом": "VERB, past.1sg - 'я пришел'",
            "мәне": "PRON, 1sg - 'я'"
        }
        response = "📚 Примеры разбора:\n\n" + "\n".join(
            f"• {word}: {analysis}" for word, analysis in examples.items()
        )
        await update.message.reply_text(response)

    async def analyze_word(self, update: Update, context):
        """Основной обработчик для анализа слов"""
        word = update.message.text.strip()

        # Убираем вопросительный знак если есть
        clean_word = word.rstrip('?')

        try:
            analysis = self.analyzer.analyze(clean_word)
            response = self.format_analysis(word, analysis)
        except Exception as e:
            logging.error(f"Error analyzing {word}: {e}")
            response = f"⚠ Не удалось разобрать слово '{word}'\nОшибка: {str(e)}"

        await update.message.reply_text(response)

    def format_analysis(self, word, analysis):
        pos = analysis.get('pos', 'UNKN')
        features = analysis.get('features', {})
        stem = analysis.get('stem', '')
        features_str = ", ".join(
            f"{k}: {v}" for k, v in features.items()
            if v not in ('', None)
        )

        # Красивое форматирование для разных частей речи
        if pos == 'NOUN':
            response = f"📌 {word} — существительное\n"
            if stem:
                response += f"Основа: {stem}\n"
            if features_str:
                response += f"Граммемы: {features_str}"

        elif pos == 'VERB':
            response = f"🔧 {word} — глагол\n"
            if features_str:
                response += f"Характеристики: {features_str}"

        elif pos == 'PRON':
            response = f"💬 {word} — местоимение\n"
            if features_str:
                response += f"Тип: {features_str}"

        elif pos == 'NUM':
            response = f"🔢 {word} — числительное\n"
            if features_str:
                response += f"Разбор: {features_str}"

        else:
            response = f"❓ {word} — не удалось определить часть речи\n"
            if features_str:
                response += f"Найдены признаки: {features_str}"

        return response

    def run(self):
        application = Application.builder().token(self.token).build()
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("example", self.example_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.analyze_word))
        application.run_polling()


if __name__ == '__main__':
    BOT_TOKEN = "8090913723:AAGwsr0ftwvwsKLTR_xoouyF1804b30-WLw"

    bot = NganasanBot(BOT_TOKEN)
    bot.run()