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

# ──────────────────────────────────────────────
# ТЕКСТЫ
# ──────────────────────────────────────────────

WELCOME_TEXT = (
    "👋 Привет! Меня зовут <b>Галия</b>.\n\n"
    "Всего 3 года назад я была в отчаянии — по уши в долгах, денег не хватало даже на продукты. "
    "Мы буквально выживали: жили от зарплаты до зарплаты и считали каждую копейку 😔\n\n"
    "Но я нашла выход — и моя жизнь кардинально изменилась! "
    "Подробности — на моей странице в Instagram 👇\n"
    "📸 https://www.instagram.com/gallyu_abdullina\n\n"
    "💰 За последние 2,5 года я заработала более <b>10 миллионов рублей</b>, используя только телефон.\n"
    "Сейчас у меня свыше <b>30 учениц</b> — они каждый день радуют меня своими успехами 🙌\n\n"
    "🚀 Хочешь узнать, как начать зарабатывать онлайн <b>без опыта</b>? Жми скорее!"
)

SUBSCRIBE_TEXT = (
    "💛 Прежде чем я раскрою все секреты заработка, сделай один небольшой шаг — "
    "<b>подпишись на мой Telegram-канал</b>!\n\n"
    "Там ты найдёшь:\n"
    "✨ Реальные истории учениц и их успехи\n"
    "⭐️ Честные отзывы\n"
    "🎯 Мои достижения и немного закулисья жизни\n\n"
    "Так ты убедишься, что я — живой человек, а не просто картинка из рекламы 😊\n\n"
    "👉 <b>Ссылка на канал:</b> https://t.me/+p53UUtIURY9hY2Fi\n\n"
    "После подписки возвращайся сюда и жми кнопку 👇"
)

DIRECTIONS_TEXT = (
    "🎉 Отлично, ты подписался(ась)!\n\n"
    "Давай тезисно расскажу, какие варианты заработка есть:\n\n"
    "👩‍💼 <b>Куратор онлайн‑школы</b>\n"
    "Средний доход — от 200 000 руб./мес. Работа только с входящими заявками!\n\n"
    "💻 <b>Онлайн‑специалист</b>\n"
    "Более 25 востребованных профессий. Стартовый доход — от 70 000 руб.\n\n"
    "🎨 <b>Инфографика для маркетплейсов</b>\n"
    "Простая и востребованная профессия. Доход — от 50 000 руб./мес.\n\n"
    "📋 <b>Заработок на заданиях</b>\n"
    "Лайки, отзывы, скачивания. От 15 000 руб./мес., первый заработок — уже сегодня!\n\n"
    "👇 <b>Что тебе ближе?</b>"
)

CURATOR_TEXT = (
    "👩‍💼 <b>Куратор онлайн‑школы INSTART</b>\n\n"
    "Это специалист по сопровождению учеников проекта. "
    "Ты предоставляешь доступ новым участникам и помогаешь им на всех этапах обучения.\n\n"
    "🔑 <b>Главное преимущество:</b> работа только с <b>входящими заявками</b> — "
    "никакого активного поиска клиентов!\n\n"
    "🎁 <b>Ты получишь:</b>\n"
    "✅ Пошаговое обучение с нуля\n"
    "✅ Готовые инструменты: посты, макеты, презентации\n"
    "✅ Полный доступ к проекту INSTART\n"
    "✅ Чаты помощи с администраторами 24/7\n"
    "✅ Планёрки и прямые эфиры от основателей\n\n"
    "💰 Доход поступает <b>напрямую на твою карту</b>, без ограничений по сумме!\n"
    "📈 Средний доход кураторов — <b>от 100 000 р./мес.</b>\n"
    "🏆 Лучшие выходят на <b>3 000 000+ р./мес.</b>\n\n"
    "👇 Смотри тарифы и выбирай свой!"
)

CURATOR_TARIFF_TEXT = (
    "💼 <b>Выбери свой тариф и стань куратором INSTART!</b>\n\n"
    "📦 <b>ВСЁ ВКЛЮЧЕНО</b> — <b>4 990 р.</b>\n"
    "Более 20 курсов по востребованным онлайн-профессиям\n\n"
    "⭐️ <b>ПРЕМИУМ</b> — <b>12 990 р.</b>\n"
    "Хит продаж! Расширенный пакет курсов + рабочие инструменты\n\n"
    "👑 <b>VIP</b> — <b>19 990 р.</b>\n"
    "Легендарные программы основателей INSTART + курсы для масштабирования\n\n"
    "🎯 <b>Все тарифы включают:</b>\n"
    "• Обучение для кураторов\n"
    "• Регулярные обновления курсов\n"
    "• Бессрочный доступ + право перепродажи\n"
    "• Чаты помощи с администраторами\n"
    "• Готовые макеты и презентации\n"
    "• Фирменная символика INSTART\n\n"
    "👇 Выбери тариф для оплаты:"
)

PAYMENT_VSE_TEXT = (
    "📦 <b>Тариф «ВСЁ ВКЛЮЧЕНО»</b>\n\n"
    "💰 <b>4 990 р.</b>\n\n"
    "📚 Содержит <b>более 20 курсов:</b>\n"
    "• Куратор INSTART (партнёр проекта)\n"
    "• Дизайнер инфографики для WB/OZON\n"
    "• Монтажёр креативных видеороликов\n"
    "• SMM-менеджер, Копирайтер\n"
    "• Специалист по чат-ботам\n"
    "• Продвижение в TG и Instagram\n"
    "• И многое другое!\n\n"
    "📈 Ожидаемый доход: от 50 000 р./мес.\n\n"
    "💳 Для оплаты и получения доступа напиши напрямую: <b>@Gallu1990</b>\n\n"
    "⏰ <i>Цена действует ограниченное время!</i>"
)

PAYMENT_PREMIUM_TEXT = (
    "⭐️ <b>Тариф «ПРЕМИУМ»</b> — 🔥 Хит продаж!\n\n"
    "💰 <b>12 990 р.</b>\n\n"
    "📚 Включает <b>все курсы тарифа «Всё включено»</b> +\n"
    "• Специалист по нейросетям\n"
    "• Менеджер Wildberries и OZON\n"
    "• WB. Путь предпринимателя\n"
    "• Закупки из Китая\n"
    "• Дизайнер фото и видео в нейросетях\n"
    "• И другие расширенные курсы!\n\n"
    "📈 Ожидаемый доход: от 200 000 р./мес.\n\n"
    "💳 Для оплаты и получения доступа напиши напрямую: <b>@Gallu1990</b>\n\n"
    "⏰ <i>Цена действует ограниченное время!</i>"
)

PAYMENT_VIP_TEXT = (
    "👑 <b>Тариф «VIP»</b> — для масштабирования результатов!\n\n"
    "💰 <b>19 990 р.</b>\n\n"
    "📚 Включает <b>всё из «Премиум»</b> + легендарные программы основателей:\n"
    "🎬 «Время Reels» — продвижение без выгорания\n"
    "💼 «Практика продаж» — продавай без stories 24/7\n"
    "⏰ «25й час» — найди время на семью и хобби\n"
    "🧠 «Магия стратегии» — план развития блога/бизнеса\n"
    "🎭 «Сценарист прогревов» — продажи через stories\n"
    "🎤 «Заговори легко, чётко и уверенно»\n"
    "⚖️ «Юридическая грамотность» для фрилансеров\n"
    "📱 «Подписчики с Reels» — 1000–5000 подписчиков/мес.\n"
    "🗓 «Успеть всё!» — идеальный график жизни\n\n"
    "📈 Ожидаемый доход: от 300 000 р./мес.\n\n"
    "💳 Для оплаты и получения доступа напиши напрямую: <b>@Gallu1990</b>\n\n"
    "⏰ <i>Цена действует ограниченное время!</i>"
)

SPECIALIST_TEXT = (
    "💻 <b>Онлайн‑специалист INSTART</b>\n\n"
    "Освойте удалённую профессию и начните зарабатывать из любой точки мира!\n\n"
    "📊 В нашей школе — более <b>30 востребованных направлений</b>.\n\n"
    "📋 <b>Как проходит обучение:</b>\n"
    "1️⃣ Выбираешь направление\n"
    "2️⃣ Проходишь курс в удобном темпе\n"
    "3️⃣ Сдаёшь итоговый тест\n"
    "4️⃣ Получаешь именной сертификат 🎓\n"
    "5️⃣ Формируешь портфолио\n"
    "6️⃣ Начинаешь работать с реальными заказами 💼\n\n"
    "🎁 <b>Ты получаешь:</b>\n"
    "✅ Бессрочный доступ ко всем материалам\n"
    "✅ Бесплатные обновления курсов\n"
    "✅ Блок по поиску клиентов и заключению сделок\n"
    "✅ Знания от практикующих профессионалов\n"
    "✅ Чат помощи 24/7\n\n"
    "💰 Уже в первый месяц — доход <b>от 50 000 р.</b>, с ростом опыта — больше!"
)

INFOGRAPHIC_TEXT = (
    "🎨 <b>Специалист по инфографике для маркетплейсов</b>\n\n"
    "Одна из самых простых и востребованных онлайн-профессий прямо сейчас! 🔥\n\n"
    "💵 <b>Сколько можно заработать?</b>\n"
    "• 1 картинка — в среднем 500 р. (~20 минут работы)\n"
    "• В карточке товара — 5–10 изображений\n"
    "• 1 заказ = от 2 500 до 5 000 р. (~2 часа работы)\n\n"
    "📈 Уже в первые дни — доход <b>от 1 500 р. ежедневно!</b>\n\n"
    "✏️ Не нужно быть профессиональным дизайнером — "
    "достаточно пройти наше обучение и начать практиковаться.\n\n"
    "🚀 Освой новый навык и превратите его в стабильный источник дохода!"
)

INFOGRAPHIC_PAYMENT_TEXT = (
    "🎨 <b>Курс «Инфографика для маркетплейсов»</b>\n\n"
    "✅ Бессрочный доступ к материалам\n"
    "✅ Чат помощи — поддержка постоянно\n"
    "✅ Именной сертификат — бесплатно\n"
    "✅ Максимальное наполнение по минимальной цене\n\n"
    "⏰ <b>Специальная цена только 24 часа:</b>\n"
    "💰 <b>2 500 р.</b>\n\n"
    "📈 Окупишь курс уже в первый месяц и выйдешь на доход от 50 000 р.!\n\n"
    "💳 Для оплаты и получения доступа напиши напрямую: <b>@Gallu1990</b>"
)

TASKS_TEXT = (
    "📋 <b>Заработок на заданиях</b> — топовое направление 2026 года! 🔥\n\n"
    "Идеально для тех, кто не хочет вести соцсети и заниматься продажами.\n\n"
    "💼 <b>Какие задания и сколько платят:</b>\n"
    "⭐️ Отзывы — от 100 р.\n"
    "📱 Скачивание приложений — до 300 р.\n"
    "📞 Звонки — от 100 р.\n"
    "📝 Опросы — от 50 р.\n"
    "📊 Презентации — от 1 000 р.\n"
    "✍️ Написание текстов — от 500 р.\n"
    "👍 Подписки, лайки и др.\n\n"
    "👥 <b>Кому подойдёт:</b>\n"
    "👶 Мамам в декрете\n"
    "🎓 Студентам\n"
    "💼 Фрилансерам\n"
    "👔 Работающим по найму (доп. доход)\n\n"
    "🕐 <b>График:</b> гибкий — сами решаете когда и сколько работать.\n"
    "💳 <b>Вывод денег:</b> на карты, кошельки, номер телефона."
)

TASKS_PAYMENT_TEXT = (
    "📋 <b>Курс «Заработок на заданиях»</b>\n\n"
    "✅ Бессрочный доступ к материалам\n"
    "✅ Постоянный чат помощи\n"
    "✅ Именной сертификат после обучения\n"
    "✅ Всё необходимое для старта уже в первый день!\n\n"
    "⏰ <b>Специальная цена только 24 часа:</b>\n"
    "💰 <b>2 490 р.</b>\n\n"
    "📈 После обучения — доход от 15 000 р. в месяц.\n\n"
    "💳 Для оплаты и получения доступа напиши напрямую: <b>@Gallu1990</b>"
)

DONE_TEXT = (
    "🎉 <b>Отлично! Добро пожаловать в команду!</b>\n\n"
    "Наш менеджер свяжется с тобой в ближайшее время и отправит доступ.\n\n"
    "💬 Напиши напрямую: <b>@Gallu1990</b> 😊\n\n"
    "📸 Instagram: https://www.instagram.com/gallyu_abdullina\n"
    "📢 Telegram-канал: https://t.me/+p53UUtIURY9hY2Fi"
)

# ──────────────────────────────────────────────
# КЛАВИАТУРЫ
# ──────────────────────────────────────────────

def kb_home():
    return [InlineKeyboardButton("🏠 Вернуться на главную", callback_data="home")]

def kb_start():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔥 Узнать подробности", callback_data="subscribe")]])

def kb_subscribe():
    return InlineKeyboardMarkup([[InlineKeyboardButton("✅ Подписался(ась)", callback_data="directions")]])

def kb_directions():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👩‍💼 Куратор онлайн‑школы", callback_data="curator")],
        [InlineKeyboardButton("💻 Онлайн‑специалист", callback_data="specialist")],
        [InlineKeyboardButton("🎨 Инфографика для маркетплейсов", callback_data="infographic")],
        [InlineKeyboardButton("📋 Заработок на заданиях", callback_data="tasks")],
    ])

def kb_curator():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💼 Смотреть тарифы", callback_data="curator_tariff")],
        kb_home(),
    ])

def kb_curator_tariff():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 ВСЁ ВКЛЮЧЕНО — 4 990 р.", callback_data="pay_vse")],
        [InlineKeyboardButton("⭐️ ПРЕМИУМ — 12 990 р.", callback_data="pay_premium")],
        [InlineKeyboardButton("👑 VIP — 19 990 р.", callback_data="pay_vip")],
        kb_home(),
    ])

def kb_payment():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Оплатил(а)", callback_data="done")],
        kb_home(),
    ])

def kb_one_with_home(text, cb):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text, callback_data=cb)],
        kb_home(),
    ])

def kb_done():
    return InlineKeyboardMarkup([kb_home()])

# ──────────────────────────────────────────────
# ХЭНДЛЕРЫ
# ──────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(WELCOME_TEXT, reply_markup=kb_start())

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "home":
        await query.message.reply_html(WELCOME_TEXT, reply_markup=kb_start())

    elif data == "subscribe":
        await query.message.reply_html(SUBSCRIBE_TEXT, reply_markup=kb_subscribe())

    elif data == "directions":
        await query.message.reply_html(DIRECTIONS_TEXT, reply_markup=kb_directions())

    # ── Куратор ──
    elif data == "curator":
        await query.message.reply_html(CURATOR_TEXT, reply_markup=kb_curator())

    elif data == "curator_tariff":
        await query.message.reply_html(CURATOR_TARIFF_TEXT, reply_markup=kb_curator_tariff())

    elif data == "pay_vse":
        await query.message.reply_html(PAYMENT_VSE_TEXT, reply_markup=kb_payment())

    elif data == "pay_premium":
        await query.message.reply_html(PAYMENT_PREMIUM_TEXT, reply_markup=kb_payment())

    elif data == "pay_vip":
        await query.message.reply_html(PAYMENT_VIP_TEXT, reply_markup=kb_payment())

    # ── Специалист ──
    elif data == "specialist":
        await query.message.reply_html(SPECIALIST_TEXT, reply_markup=kb_one_with_home("🚀 Стать онлайн‑специалистом", "specialist_tariff"))

    elif data == "specialist_tariff":
        await query.message.reply_html(CURATOR_TARIFF_TEXT, reply_markup=kb_curator_tariff())

    # ── Инфографика ──
    elif data == "infographic":
        await query.message.reply_html(INFOGRAPHIC_TEXT, reply_markup=kb_one_with_home("✅ Хочу оплатить!", "infographic_payment"))

    elif data == "infographic_payment":
        await query.message.reply_html(INFOGRAPHIC_PAYMENT_TEXT, reply_markup=kb_payment())

    # ── Задания ──
    elif data == "tasks":
        await query.message.reply_html(TASKS_TEXT, reply_markup=kb_one_with_home("📋 Хочу выполнять задания!", "tasks_payment"))

    elif data == "tasks_payment":
        await query.message.reply_html(TASKS_PAYMENT_TEXT, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Начнём!", callback_data="done")],
            kb_home(),
        ]))

    elif data == "done":
        await query.message.reply_html(DONE_TEXT, reply_markup=kb_done())

# ──────────────────────────────────────────────
# ЗАПУСК
# ──────────────────────────────────────────────

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
