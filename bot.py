import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WELCOME_TEXT = (
    "Привет! Меня зовут Галия. Всего 3 года назад я была в отчаянии: по уши в долгах, "
    "денег не хватало даже на продукты. Мы буквально выживали — жили от зарплаты до зарплаты "
    "и считали каждую копейку.\n\n"
    "Но я нашла выход — и моя жизнь кардинально изменилась! Подробности — на моей странице в Instagram.\n\n https://www.instagram.com/gallyu_abdullina?igsh=MTd6NnR2MHc5MWpsNA=="
    "За последние 2,5 года я заработала более <b>10 миллионов рублей</b>, используя только телефон. "
    "Сейчас у меня свыше 30 учениц — они каждый день радуют меня своими успехами.\n\n"
    "Хочешь узнать, как начать зарабатывать онлайн без опыта? Жми скорее!"
)

SUBSCRIBE_TEXT = (
    "Прежде чем я раскрою все секреты заработка, сделай небольшой шаг — подпишись на мой личный канал 💛\n\n"
    "Там ты найдёшь:\n"
    "• реальные истории учениц и их успехи;\n"
    "• честные отзывы;\n"
    "• мои достижения и немного закулисья жизни.\n\n"
    "Так ты убедишься, что я — живой человек, а не просто картинка из рекламы 😊\n\n"
    "👉 Ссылка: https://t.me/+p53UUtIURY9hY2Fi"
    "После подписки возвращайся сюда — и жми кнопку 👇"
)

DIRECTIONS_TEXT = (
    "Давай тезисно пропишу, какие варианты есть:\n\n"
    "👩‍💼 <b>Куратор онлайн‑школы</b> — от 200 000 руб./мес.\n\n"
    "💻 <b>Онлайн‑специалист</b> — более 25 профессий, от 70 000 руб.\n\n"
    "🎨 <b>Инфографика для маркетплейсов</b> — от 50 000 руб./мес.\n\n"
    "📋 <b>Заработок на заданиях</b> — от 15 000 руб., старт уже сегодня.\n\n"
    "Что тебе ближе?"
)

CURATOR_TEXT = (
    "<b>Куратор онлайн‑школы</b> — специалист по сопровождению учеников.\n"
    "Работа только с входящими заявками — активный поиск клиентов не нужен!\n\n"
    "Вы получите:\n"
    "✅ Пошаговое обучение\n"
    "✅ Готовые инструменты (посты, макеты, презентации)\n"
    "✅ Полный доступ к проекту\n\n"
    "💰 Доход напрямую на карту — <b>от 100 000 р./мес.</b>"
)

CURATOR_TARIFF_TEXT = (
    "<b>Все тарифы включают:</b>\n"
    "• Возможность стать куратором\n"
    "• Бесплатные обновления\n"
    "• Бессрочный доступ к материалам\n"
    "• Доступ ко всем рабочим чатам\n"
    "• 6 месяцев кураторства по орг. вопросам\n"
    "• Курс с заданиями в подарок\n\n"
    "⭐ <b>VIP‑тариф</b> — в подарок мой авторский канал со всеми знаниями!\n"
    "Мой результат: более 300 000 р./мес., рекорд за день — 500 500 р.\n\n"
    "Сделайте выбор в пользу своего успеха!"
)

PAYMENT_TEXT = (
    "Сейчас действуют <b>специальные цены</b>:\n\n"
    "📦 <b>Тариф «Всё включено»</b>\n"
    "<b>9 990 р.</b> <s>14 990 р.</s>\n"
    "Ожидаемый доход: от 50 000 р./мес.\n"
    "Ссылка на оплату: [добавьте ссылку]\n\n"
    "💎 <b>Тариф «Премиум»</b>\n"
    "<b>19 990 р.</b> <s>24 990 р.</s>\n"
    "Включает: бессрочное наставничество + авторский канал.\n"
    "Ожидаемый доход: от 200 000 р./мес.\n"
    "Ссылка на оплату: [добавьте ссылку]\n\n"
    "⏰ Успейте воспользоваться предложением по сниженной стоимости!"
)

SPECIALIST_TEXT = (
    "<b>Онлайн‑специалист</b> — освойте удалённую профессию!\n\n"
    "Более <b>30 направлений</b> по востребованным профессиям.\n\n"
    "<b>Как проходит обучение:</b>\n"
    "1. Выбор направления\n"
    "2. Прохождение курса\n"
    "3. Сдача итогового теста\n"
    "4. Именной сертификат\n"
    "5. Формирование портфолио\n"
    "6. Первые реальные заказы\n\n"
    "✅ Бессрочный доступ, бесплатные обновления, поддержка.\n\n"
    "💰 Уже в первый месяц — доход <b>от 50 000 р.</b>"
)

SPECIALIST_TARIFF_TEXT = (
    "<b>Все тарифы включают:</b>\n"
    "• Бессрочный доступ к материалам\n"
    "• Бесплатные обновления\n"
    "• Доступ ко всем рабочим чатам\n"
    "• 6 месяцев кураторства\n"
    "• Канал с моими рекомендациями\n"
    "• Курс с заданиями в подарок\n\n"
    "⭐ <b>VIP‑тариф</b> — именно с него начинала я!\n"
    "Мой результат: более 300 000 р./мес., рекорд — 500 000 р. за день.\n\n"
    "Выбор за вами!"
)

INFOGRAPHIC_TEXT = (
    "<b>Инфографика: профессия с доходом от 1 500 р. в день</b>\n\n"
    "• Стоимость одной картинки — ~500 р. (~20 мин. работы)\n"
    "• В карточке товара 5–10 изображений\n"
    "• Доход с одного заказа — от 2 500 до 5 000 р. (~2 часа)\n\n"
    "Уже в первые дни — <b>от 1 500 р. ежедневно!</b>\n\n"
    "Не нужно быть дизайнером — достаточно пройти наше обучение."
)

INFOGRAPHIC_PAYMENT_TEXT = (
    "<b>Курс «Инфографика»</b>\n\n"
    "✅ Бессрочный доступ\n"
    "✅ Чат помощи\n"
    "✅ Именной сертификат бесплатно\n\n"
    "⏰ <b>Только 24 часа:</b> <b>2 500 р.</b> <s>4 990 р.</s>\n\n"
    "💰 Окупите курс в первый месяц и выйдете на доход от 50 000 р.\n\n"
    "Ссылка на оплату: [добавьте ссылку]"
)

TASKS_TEXT = (
    "<b>Заработок на заданиях</b> — топ 2026 года!\n\n"
    "Идеально без соцсетей и продаж.\n\n"
    "<b>Задания и оплата:</b>\n"
    "• Отзывы — от 100 р.\n"
    "• Скачивание приложений — до 300 р.\n"
    "• Звонки — от 100 р.\n"
    "• Опросы — от 50 р.\n"
    "• Презентации — от 1 000 р.\n"
    "• Тексты — от 500 р.\n\n"
    "<b>Кому подойдёт:</b> мамам в декрете, студентам, фрилансерам.\n\n"
    "<b>График:</b> гибкий, сами решаете когда работать.\n"
    "<b>Вывод:</b> на карты, кошельки, номер телефона."
)

TASKS_PAYMENT_TEXT = (
    "<b>Курс «Заработок на заданиях»</b>\n\n"
    "✅ Бессрочный доступ\n"
    "✅ Чат помощи постоянно\n"
    "✅ Именной сертификат\n"
    "✅ Старт заработка с первого дня\n\n"
    "⏰ <b>Только 24 часа:</b> <b>2 490 р.</b> <s>4 990 р.</s>\n\n"
    "💰 После обучения — доход от 15 000 р. в месяц.\n\n"
    "Ссылка на оплату: [добавьте ссылку]"
)

DONE_TEXT = (
    "Отлично! 🎉 Наш менеджер свяжется с тобой в ближайшее время.\n\n"
    "Если хочешь ускорить — напиши напрямую: @Gallu1990 😊"
)

def kb_start():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Узнать подробности", callback_data="subscribe")]])

def kb_subscribe():
    return InlineKeyboardMarkup([[InlineKeyboardButton("✅ Подписался(ась)", callback_data="directions")]])

def kb_directions():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👩‍💼 Куратор онлайн‑школы", callback_data="curator")],
        [InlineKeyboardButton("💻 Онлайн‑специалист", callback_data="specialist")],
        [InlineKeyboardButton("🎨 Инфографика для маркетплейсов", callback_data="infographic")],
        [InlineKeyboardButton("📋 Заработок на заданиях", callback_data="tasks")],
    ])

def kb_one(text, cb):
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, callback_data=cb)]])

def kb_payment():
    return InlineKeyboardMarkup([[InlineKeyboardButton("✅ Оплатил(а)", callback_data="done")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(WELCOME_TEXT, reply_markup=kb_start())

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "subscribe":
        await query.message.reply_html(SUBSCRIBE_TEXT, reply_markup=kb_subscribe())
    elif data == "directions":
        await query.message.reply_html(DIRECTIONS_TEXT, reply_markup=kb_directions())
    elif data == "curator":
        await query.message.reply_html(CURATOR_TEXT, reply_markup=kb_one("🚀 Стать куратором", "curator_tariff"))
    elif data == "curator_tariff":
        await query.message.reply_html(CURATOR_TARIFF_TEXT, reply_markup=kb_one("💳 Перейти к оплате", "curator_payment"))
    elif data == "curator_payment":
        await query.message.reply_html(PAYMENT_TEXT, reply_markup=kb_payment())
    elif data == "specialist":
        await query.message.reply_html(SPECIALIST_TEXT, reply_markup=kb_one("🚀 Стать онлайн‑специалистом", "specialist_tariff"))
    elif data == "specialist_tariff":
        await query.message.reply_html(SPECIALIST_TARIFF_TEXT


, reply_markup=kb_one("💳 Перейти к оплате", "specialist_payment"))
    elif data == "specialist_payment":
        await query.message.reply_html(PAYMENT_TEXT, reply_markup=kb_payment())
    elif data == "infographic":
        await query.message.reply_html(INFOGRAPHIC_TEXT, reply_markup=kb_one("✅ Готова оплатить", "infographic_payment"))
    elif data == "infographic_payment":
        await query.message.reply_html(INFOGRAPHIC_PAYMENT_TEXT, reply_markup=kb_payment())
    elif data == "tasks":
        await query.message.reply_html(TASKS_TEXT, reply_markup=kb_one("📋 Выполнять задания", "tasks_payment"))
    elif data == "tasks_payment":
        await query.message.reply_html(TASKS_PAYMENT_TEXT, reply_markup=kb_one("🚀 Начнем!", "done"))
    elif data == "done":
        await query.message.reply_html(DONE_TEXT)

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("Переменная окружения BOT_TOKEN не задана!")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
