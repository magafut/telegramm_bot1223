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
    "Привет! Надоело, что деньги утекают сквозь пальцы, "
    "а на развитие вечно нет времени? 📉\n\n"
    "Я помогу тебе вырваться из этого цикла. "
    "Забирай <b>бесплатный план по выходу на новый уровень</b>, "
    "который сэкономит тебе минимум год жизни!"
)

PLAN_TEXT = (
    "<b>План: 5 шагов к росту 🚀</b>\n\n"
    "1. <b>Аудит финансов:</b> Выпиши 3 главные статьи трат.\n"
    "   💡 <i>Лайфхак:</i> Крупные покупки (от 3к) делай только через 24 часа.\n\n"
    "2. <b>Тайм-менеджмент:</b> Удали 3 лишних приложения-пожирателя времени.\n"
    "   📈 <i>Результат:</i> +40 минут в день на развитие.\n\n"
    "3. <b>Заначка:</b> Открой счёт и переведи туда 500–1000 ₽ прямо сейчас. Сначала плати себе.\n\n"
    "4. <b>Фокус дня:</b> С вечера пиши только ОДНУ главную задачу на завтра.\n\n"
    "5. <b>Инвестиции:</b> Помни, что обучение даёт самый высокий % доходности.\n\n"
    "<b>Хочешь внедрить это по шагам вместе со мной?</b>"
)

CONSEQUENCES_TEXT = (
    "<b>Что будет, если оставить всё как есть:</b>\n\n"
    "1. <b>Минус сотни тысяч:</b> Без аудита ты продолжишь сливать до 30% дохода в никуда.\n"
    "2. <b>Украденная жизнь:</b> Пожиратели времени заберут у тебя 10 суток чистого времени в год.\n"
    "3. <b>Жизнь в долг:</b> Любая поломка или штраф станут трагедией без финансовой подушки.\n"
    "4. <b>Бег на месте:</b> Без фокуса ты будешь пахать 24/7, но не сдвинешься ни на шаг.\n"
    "5. <b>Деградация:</b> Пока ты экономишь на обучении, другие забирают твои деньги и возможности.\n\n"
    "<b>Оставляем всё как есть или начнём менять ситуацию?</b>"
)

FUTURE_TEXT = (
    "<b>Твоя жизнь через 1 год:</b>\n\n"
    "🛡 <b>Финансовый щит:</b> У тебя есть подушка безопасности. Кредиты гасятся, а импульсивные траты исчезли.\n\n"
    "⏰ <b>Свободное время:</b> Ты вернул(а) себе 250 часов в год. Больше никакой прокрастинации и пустых соцсетей.\n\n"
    "💸 <b>Рост дохода:</b> Благодаря обучению твоя ценность выросла. Ты зарабатываешь на 30–50% больше.\n\n"
    "🎯 <b>Ясные цели:</b> За год ты закрыл(а) ~300 важных задач. Хаос сменился чётким планом.\n\n"
    "💪 <b>Уверенность:</b> Ты управляешь деньгами, а не они тобой. Появилось чувство контроля над будущим.\n\n"
    "Сделаем первый шаг к этому результату?"
)

DIRECTION_TEXT = (
    "В нашей школе более 10 направлений — от аналитики до творчества. "
    "Чтобы ты не тратил(а) время на «не своё», давай выберем то, что принесёт тебе деньги и удовольствие.\n\n"
    "<b>Что тебе ближе?</b>"
)

VISUAL_TEXT = (
    "Круто! В этой нише сейчас самый быстрый рост. Выбирай свой инструмент:"
)

ANALYTICS_TEXT = (
    "Аналитика — основа любого успешного бизнеса. Выбирай свой инструмент:"
)

SOCIAL_TEXT = (
    "Контент и общение — двигатель современного маркетинга. Выбирай свой инструмент:"
)

TECH_TEXT = (
    "Технари нужны везде! Выбирай свою специализацию:"
)

OFFER_MONTAGE = (
    "Видеоконтент сейчас — нефть 21 века. Компании стоят в очереди за хорошими монтажёрами.\n\n"
    "<b>Твой результат через 2 месяца:</b>\n"
    "1. Навыки профи в монтаже на смартфоне/ПК.\n"
    "2. Готовое портфолио из 10 работ.\n"
    "3. Первые заказы от 30 000 ₽ в месяц.\n\n"
    "Хочешь посмотреть <b>3 примера работ наших учеников</b>, которые они сделали уже на первой неделе?"
)

FINAL_TEXT = (
    "Кстати! К любому курсу ты получаешь наш <b>Бонус: Модуль по личной эффективности</b>.\n\n"
    "Мало просто научиться монтировать или вести СММ. "
    "Важно уметь планировать день, чтобы не выгорать и успевать жить. "
    "Мы научим и тому, и другому.\n\n"
    "<b>Готов(а) инвестировать в новую жизнь?</b>"
)

# ──────────────────────────────────────────────
# КЛАВИАТУРЫ
# ──────────────────────────────────────────────

def kb_start():
    return InlineKeyboardMarkup([[InlineKeyboardButton("📋 Получить план", callback_data="plan")]])

def kb_plan():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔥 Да, погнали!", callback_data="consequences")]])

def kb_consequences():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Выбраться из ямы", callback_data="future")]])

def kb_future():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Начать путь к цели", callback_data="direction")]])

def kb_directions():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Аналитика и порядок", callback_data="dir_analytics")],
        [InlineKeyboardButton("🎨 Творчество и визуал", callback_data="dir_visual")],
        [InlineKeyboardButton("📱 Общение и контент", callback_data="dir_social")],
        [InlineKeyboardButton("🛠 Техническая часть", callback_data="dir_tech")],
    ])

def kb_visual():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 Монтажёр видео", callback_data="offer_montage")],
        [InlineKeyboardButton("📸 Фотограф", callback_data="offer_photo")],
        [InlineKeyboardButton("🎨 Графический дизайн", callback_data="offer_design")],
    ])

def kb_analytics():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Менеджер маркетплейсов", callback_data="offer_marketplace")],
        [InlineKeyboardButton("🎯 Таргетолог", callback_data="offer_target")],
    ])

def kb_social():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📲 СММ-менеджер", callback_data="offer_smm")],
        [InlineKeyboardButton("✍️ Копирайтер", callback_data="offer_copy")],
        [InlineKeyboardButton("🌟 Сторисмейкер", callback_data="offer_stories")],
    ])

def kb_tech():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Создатель сайтов", callback_data="offer_web")],
        [InlineKeyboardButton("⚙️ Техспец", callback_data="offer_techspec")],
    ])

def kb_offer():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👀 Да, покажи!", callback_data="final")],
        [InlineKeyboardButton("💰 Узнать цену и забронировать место", callback_data="final")],
    ])

def kb_final():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Хочу курс + Бонус!", callback_data="done")],
        [InlineKeyboardButton("🎁 Записаться на бесплатный урок", callback_data="done")],
    ])

# ──────────────────────────────────────────────
# ХЭНДЛЕРЫ
# ──────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(WELCOME_TEXT, reply_markup=kb_start())


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ── Основной сценарий ──
    if data == "plan":
        await query.message.reply_html(PLAN_TEXT, reply_markup=kb_plan())

    elif data == "consequences":
        await query.message.reply_html(CONSEQUENCES_TEXT, reply_markup=kb_consequences())

    elif data == "future":
        await query.message.reply_html(FUTURE_TEXT, reply_markup=kb_future())

    elif data == "direction":
        await query.message.reply_html(DIRECTION_TEXT, reply_markup=kb_directions())

    # ── Выбор направления ──
    elif data == "dir_visual":
        await query.message.reply_html(VISUAL_TEXT, reply_markup=kb_visual())

    elif data == "dir_analytics":
        await query.message.reply_html(ANALYTICS_TEXT, reply_markup=kb_analytics())

    elif data == "dir_social":
        await query.message.reply_html(SOCIAL_TEXT, reply_markup=kb_social())

    elif data == "dir_tech":
        await query.message.reply_html(TECH_TEXT, reply_markup=kb_tech())

    # ── Офферы ──
    elif data == "offer_montage":
        await query.message.reply_html(OFFER_MONTAGE, reply_markup=kb_offer())

    elif data in (
        "offer_photo", "offer_design", "offer_marketplace",
        "offer_target", "offer_smm", "offer_copy",
        "offer_stories", "offer_web", "offer_techspec",
    ):
        # Универсальный оффер для остальных профессий
        profession_names = {
            "offer_photo": "Фотограф",
            "offer_design": "Графический дизайнер",
            "offer_marketplace": "Менеджер маркетплейсов",
            "offer_target": "Таргетолог",
            "offer_smm": "СММ-менеджер",
            "offer_copy": "Копирайтер",
            "offer_stories": "Сторисмейкер",
            "offer_web": "Создатель сайтов",
            "offer_techspec": "Техспец",
        }
        name = profession_names.get(data, "Специалист")
        text = (
            f"Отличный выбор! <b>{name}</b> — одна из самых востребованных профессий прямо сейчас.\n\n"
            "<b>Твой результат через 2 месяца:</b>\n"
            "1. Профессиональные навыки с нуля.\n"
            "2. Готовое портфолио из реальных проектов.\n"
            "3. Первые заказы от 25 000–40 000 ₽ в месяц.\n\n"
            "Хочешь посмотреть <b>примеры работ наших учеников</b>?"
        )
        await query.message.reply_html(text, reply_markup=kb_offer())

    # ── Финальный этап ──
    elif data == "final":
        await query.message.reply_html(FINAL_TEXT, reply_markup=kb_final())

    elif data == "done":
        text = (
            "Отлично! 🎉 Наш менеджер свяжется с тобой в ближайшее время "
            "и расскажет все детали.\n\n"
            "А пока — напиши нам в личку или оставь свой контакт, "
            "чтобы мы могли с тобой связаться. 😊"
        )
        await query.message.reply_html(text)


# ──────────────────────────────────────────────
# ЗАПУСК
# ──────────────────────────────────────────────

def main():
    import os
    TOKEN = os.environ.get("BOT_TOKEN") # ← Замени на токен от @BotFather

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
