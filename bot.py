import json
import logging
import os
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN", "8680499622:AAHTpgQXyGKyFATDolT6tmBH4USgct1HU4A")
ADMIN_ID = "123456789"  # ID یا خۆ وەک ڕێڤەبەر لێرە دانە داکو پێزانین بۆ تە بێن

BALANCE_FILE = "balances.json"
COOLDOWN_FILE = "cooldowns.json"
HISTORY_FILE = "history.json"
USED_KEYS_FILE = "used_keys.json"

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_data(file_path, data):
    try:
        with open(file_path, "w") as f:
            json.dump(data, f)
    except Exception as e:
        logging.error(f"Error saving data to {file_path}: {e}")

# دروستکرنا لستا زەبەلاح و پێشکەفتی یا 1285 ڕاپۆرتێن بۆتی
MASSIVE_REPORT_TYPES = {
    "rep_1": ("🚨 سپام و بڵاڤکرنا ڤیدیۆکێن بێ مانا", "🚨"),
    "rep_2": ("🔞 ناڤەرۆکا نەشیاو و پۆلێن 18+", "🔞"),
    "rep_3": ("⚠️ توندوتیژی و پێشێلکاریێن دڕندانە", "⚠️"),
    "rep_4": ("🔪 گروپێن تێرۆرستی و چەکدار", "🔪"),
    "rep_5": ("💸 فێلبازی و سکامێن ئابووری", "💸"),
    "rep_6": ("🔗 لینکێن نەیاسایی و ڤایرۆسێن مەترسیدار", "🔗"),
    "rep_7": ("💊 فرۆتنا ماددەیێن هوشْبەر", "💊"),
    "rep_8": ("🔫 بازرگانیا چەکێن قەدەغەکری", "🔫"),
    "rep_9": ("🛑 پێشێلکرنا مافێن سەرەکی یێن مرۆڤی", "🛑"),
    "rep_10": ("🎭 خۆخاپاندن و دروستکرنا ناسنامەیێن درۆین", "🎭"),
    "rep_11": ("💻 هێرشا ڕاوەستاندنا خزمەتگوزاریێ (DDoS Sabotage)", "💻"),
    "rep_12": ("🔓 ئامرازێن هاککرن و دزینا کەناڵێن تەلەگرام", "🔓"),
    "rep_13": ("🛡 لادانا ئەدمنێن سەرەکی و کۆنترۆلا کەناڵێ", "🛡"),
    "rep_14": ("🕵️ دزینا تۆکن و کۆوکیێن سێرڤەری", "🕵️"),
    "rep_15": ("🦠 بەلاڤکرنا ڕانسۆموێر (Ransomware Attack)", "🦠"),
    "rep_16": ("📡 هێرشێن فیشینگا پێشکەفتی بۆ کۆنترۆلێ", "📡"),
    "rep_17": ("⚡ شکاندنا کلیل و سکیورتییا گرووپان", "⚡"),
    "rep_18": ("🌐 هێرشێن SQL Injection بۆ بانکێن داتایێ", "🌐"),
    "rep_19": ("⚙️ بەلاڤکرنا 0-Day Exploit بۆ شکستپێکرنێ", "⚙️"),
    "rep_20": ("📥 دانانا باکدۆر و ترۆجانێن کۆنترۆلا تەواو", "📥"),
}

for i in range(21, 1286):
    if i % 4 == 0:
        emoji = "⚡"
        title = f"هێرشا پله‌ بلند و کۆنترۆلا توند ژمارە {i}"
    elif i % 4 == 1:
        emoji = "🔥"
        title = f"سیستەمێ ئەکسپلویت و شکانترا سکیورتی ژمارە {i}"
    elif i % 4 == 2:
        emoji = "💎"
        title = f"ڕاپۆرتا تایبەت و هێرشا سایبەری ژمارە {i}"
    else:
        emoji = "🚀"
        title = f"ئامرازێ قەوی یێ ڕاپۆرت و سزای ژمارە {i}"
    MASSIVE_REPORT_TYPES[f"rep_{i}"] = (title, emoji)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    username = f"@{user.username}" if user.username else "نەدیار"
    name = user.first_name

    balances = load_data(BALANCE_FILE)
    if user_id not in balances:
        balances[user_id] = 5  # 5 کلیلێن دەستپێکی
        save_data(BALANCE_FILE, balances)

    balance = balances.get(user_id, 5)

    profile_text = (
        f"╔══════════════════════╗\n"
        f" 🛡 **سەنتەرێ پڕۆفیشناڵ یێ هاک و ڕاپۆرتان**\n"
        f"╚══════════════════════╝\n\n"
        f"👤 **پڕۆفایلێ بەکارهێنەری:**\n"
        f"• **ناڤ:** {name}\n"
        f"• **یوزەرنەیم:** `{username}`\n"
        f"• **باڵانسا نها:** `💎 {balance} کلیل`\n\n"
        f"🎁 **دیارییا دەمەکی (هر 5 دەمژمێران):**\n"
        f"⏱ دۆخ: `ڤەکری و بەرهەڤ بۆ وەرگرتنێ`"
    )

    keyboard = [
        [InlineKeyboardButton("🎁 وەرگرتنا 5 کلیلێن بەلاش", callback_data="claim_gift")],
        [
            InlineKeyboardButton("📊 سيستەمێ 1285 ڕاپۆرتان", callback_data="menu_reports"),
            InlineKeyboardButton("📜 سەنتەری ڕێپۆرتان (مێژوو)", callback_data="report_history"),
        ],
        [InlineKeyboardButton("🔄 نووژەنکرنا پڕۆفایلی (Refresh)", callback_data="refresh_profile")],
        [InlineKeyboardButton("🛒 کڕینا کلیلان (تەماس)", url="https://t.me/YUSEEF_SURCHI")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(profile_text, parse_mode="Markdown", reply_markup=reply_markup)
    elif update.callback_query:
        query = update.callback_query
        try:
            await query.answer()
            await query.edit_message_text(text=profile_text, parse_mode="Markdown", reply_markup=reply_markup)
        except Exception:
            pass


async def handle_secret_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user = update.effective_user
    user_id = str(user.id)
    
    # پشکنینا کلیلەکا نهێنی یا تایبەت
    if text == "rayan1324675554":
        used_keys = load_data(USED_KEYS_FILE)
        
        if user_id in used_keys.get("users", []):
            await update.message.reply_text("⚠️ تە بەری نوکە ئەڤ کلیلە بکار ئینایە و تنێ ١ جار دهێتە بکارئینان!")
            return

        if "global_used" in used_keys and used_keys["global_used"]:
            await update.message.reply_text("⚠️ ئەڤ کلیلە بەری نوکە هاتیە بکارئینان و اکسپایێر بوویە!")
            return

        # تۆمارکرنا کو کلیل هاتە بکارئینان
        if "users" not in used_keys:
            used_keys["users"] = []
        used_keys["users"].append(user_id)
        used_keys["global_used"] = True
        save_data(USED_KEYS_FILE, used_keys)

        # زێدەکرنا کلیلان بۆ باڵانسا بەکارهێنەری (بۆ نموونە 10 کلیلێن custom)
        balances = load_data(BALANCE_FILE)
        current_bal = balances.get(user_id, 5)
        added_amount = 10  # ژمارەیا کلیلێن زێدەبووی
        balances[user_id] = current_bal + added_amount
        save_data(BALANCE_FILE, balances)

        # پەیاما سەرکەفتنێ بۆ بەکارهێنەری
        await update.message.reply_text(
            f"🎉 پیرۆزە! کلیلا تایبەت ب سەرکەفتن هاتە فعالکرن.\n"
            f"💎 بڕێ `{added_amount} کلیل` بۆ باڵانسا تە هاتە زێدەکرن!\n"
            f"⚠️ ئەڤ کلیلە اکسپایێر بوو و کەسەک دی ناتوانێ بکار بینیت.",
            parse_mode="Markdown"
        )

        # هنارتنا پێزانینان بۆ ڕێڤەبەری (دگەل یوزەرناڤ، ئایدی و پڕۆفایلێ ب وێنە یاخود لینک)
        admin_msg = (
            f"🚨 **چالاكبوونا کلیلا نهێنی!**\n\n"
            f"👤 ناڤ: {user.first_name}\n"
            f"🆔 ئایدی: `{user.id}`\n"
            f"🔗 یوزەرنەیم: @{user.username if user.username else 'نەدیار'}\n"
            f"💎 کلیلێن بۆ هاتنە زێدەکرن: +{added_amount}\n"
            f"🔒 دۆخ: کلیل هاتە بکارئینان و اکسپایێر بوو."
        )
        
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_msg, parse_mode="Markdown")
        except Exception:
            pass
    else:
        # ئەگەر پیامەک ئاسایی بوو، بتۆڤێ دەستپێکێ بینە یان پەیاما ئاسایی بدە
        await start(update, context)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = str(query.from_user.id)

    try:
        await query.answer()
    except Exception:
        pass

    if data == "back_to_start" or data == "refresh_profile":
        await start(update, context)

    elif data == "menu_reports":
        report_menu = (
            "🌌 **ناڤەندا کۆنتڕۆلا 1285 ڕاپۆرتێن پێشکەفتی**\n\n"
            "• هەموو ئامرازێن هێرش و ڕاپۆرتان ب شێوەیەکێ قەوی و خودکار کار دکەن.\n"
            "• هەر 1 کلیل = 5 کردارێن سەرپێچییێ.\n\n"
            "👇 پەڕەیا خۆ بژێرە بۆ بینینا لستان:"
        )
        report_keyboard = [
            [InlineKeyboardButton("📄 دەستپێکرنا پەڕەیا 1", callback_data="page_0")],
            [InlineKeyboardButton("🛒 کڕینا باڵانسی (راستەوخۆ)", url="https://t.me/YUSEEF_SURCHI")],
            [InlineKeyboardButton("🔙 پاشڤە (دەستپێکێ)", callback_data="back_to_start")],
        ]
        try:
            await query.edit_message_text(text=report_menu, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(report_keyboard))
        except Exception:
            pass

    elif data.startswith("page_"):
        page_idx = int(data.replace("page_", ""))
        items_list = list(MASSIVE_REPORT_TYPES.items())
        per_page = 10
        total_pages = (len(items_list) + per_page - 1) // per_page
        
        start_idx = page_idx * per_page
        end_idx = start_idx + per_page
        current_items = items_list[start_idx:end_idx]
        
        rep_keyboard = []
        for key_code, (title, emoji) in current_items:
            rep_keyboard.append([InlineKeyboardButton(f"{emoji} {title}", callback_data=f"execute_{key_code}")])

        nav_buttons = []
        if page_idx > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ پێشتر", callback_data=f"page_{page_idx - 1}"))
        if end_idx < len(items_list):
            nav_buttons.append(InlineKeyboardButton("دواتر ➡️", callback_data=f"page_{page_idx + 1}"))

        if nav_buttons:
            rep_keyboard.append(nav_buttons)

        rep_keyboard.append([InlineKeyboardButton("🔙 پاشڤە بۆ مێنۆیا سەرەکی", callback_data="menu_reports")])

        try:
            await query.edit_message_text(
                text=f"⚡ **لستا فەرمیا ڕاپۆرتان (پەڕە {page_idx + 1} ژ {total_pages}):**\nبۆ دیتنا زێدەتر کلیکا دوگمەیێن خوارێ بکە:",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(rep_keyboard),
            )
        except Exception:
            pass

    elif data.startswith("execute_"):
        rep_key = data.replace("execute_", "")
        report_name, emoji = MASSIVE_REPORT_TYPES.get(rep_key, ("تشتێ خراب", "⚠️"))
        
        histories = load_data(HISTORY_FILE)
        if user_id not in histories:
            histories[user_id] = []
        
        current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        histories[user_id].insert(0, {
            "name": f"{emoji} {report_name}",
            "time": current_time_str
        })
        histories[user_id] = histories[user_id][:10]
        save_data(HISTORY_FILE, histories)

        try:
            await context.bot.answer_callback_query(
                callback_query_id=query.id,
                text=f"{emoji} سەرکەفتن! داخوازییا ڕاپۆرتێ بۆ ({report_name}) ب سەرکەفتن هاتە هنارتن.",
                show_alert=True
            )
        except Exception:
            pass

    elif data == "report_history":
        histories = load_data(HISTORY_FILE)
        user_history = histories.get(user_id, [])

        if not user_history:
            hist_text = "📜 **سەنتەرێ ڕێپۆرتان (مێژوو):**\n\nتە هێشتا هیچ ڕێپۆرتەک نەنارتیە!"
        else:
            hist_text = "📜 **دوماهیک ڕێپۆرتێن تە هنارتین دگەل دەمی:**\n\n"
            for idx, h in enumerate(user_history, 1):
                hist_text += f"{idx}. {h['name']}\n   ⏱ کات: `{h['time']}`\n\n"

        hist_keyboard = [
            [InlineKeyboardButton("🔙 پاشڤە (دەستپێکێ)", callback_data="back_to_start")]
        ]
        try:
            await query.edit_message_text(text=hist_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(hist_keyboard))
        except Exception:
            pass

    elif data == "claim_gift":
        cooldowns = load_data(COOLDOWN_FILE)
        current_time = time.time()
        last_claim = cooldowns.get(user_id, 0)
        
        cooldown_time = 5 * 3600
        
        if current_time - last_claim < cooldown_time:
            remaining_sec = int(cooldown_time - (current_time - last_claim))
            rem_hours = remaining_sec // 3600
            rem_mins = (remaining_sec % 3600) // 60
            rem_secs = remaining_sec % 60
            try:
                await context.bot.answer_callback_query(
                    callback_query_id=query.id,
                    text=f"⚠️ هێشتا دەمێ وەرگرتنی نەهاتیە!\n⏳ ماوەیێ مایی: {rem_hours} دەمژمێر، {rem_mins} خولەک و {rem_secs} چرکە.",
                    show_alert=True
                )
            except Exception:
                pass
            return

        balances = load_data(BALANCE_FILE)
        current_bal = balances.get(user_id, 5)
        balances[user_id] = current_bal + 5
        save_data(BALANCE_FILE, balances)

        cooldowns[user_id] = current_time
        save_data(COOLDOWN_FILE, cooldowns)

        try:
            await context.bot.answer_callback_query(
                callback_query_id=query.id,
                text="🎁 پیرۆزە! 5 کلیلێن بەلاش ب سەرکەفتن هاتنە زێدەکرن بۆ پڕۆفایلا تە.",
                show_alert=True
            )
        except Exception:
            pass
        await start(update, context)


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    # هاندەرێ پەیامان بۆ پشکنینا کلیلێن نهێنی و ڤەشارتى
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_secret_key))

    print("بۆتێ 1285 ڕاپۆرتان و سیستەمێ کلیلێن نهێنی ب سەرکەفتن د کار دکەت...")
    app.run_polling()

if __name__ == "__main__":
    main()
