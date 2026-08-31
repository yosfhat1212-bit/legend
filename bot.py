import json
import logging
import os
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN", "8680499622:AAHTpgQXyGKyFATDolT6tmBH4USgct1HU4A")

BALANCE_FILE = "balances.json"
COOLDOWN_FILE = "cooldowns.json"

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f)

# دروستکرنا لستا زەبەلاح و پێشکەفتی یا 5000 ڕاپۆرتان
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

for i in range(21, 5001):
    if i % 4 == 0:
        emoji = "🔓"
        title = f"هێرشا هاککرن و دزینا کەناڵێ ژمارە {i}"
    elif i % 4 == 1:
        emoji = "💻"
        title = f"سایبەر هێرش و پێشێلکارییا دیجیتالی ژمارە {i}"
    elif i % 4 == 2:
        emoji = "🚨"
        title = f"شکاندنا ڕێنماییێن تەلەگرام ژمارە {i}"
    else:
        emoji = "⚠️"
        title = f"چاڵاکیا مەترسیدار و سکیورتی ژمارە {i}"
    MASSIVE_REPORT_TYPES[f"rep_{i}"] = (title, emoji)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    username = f"@{user.username}" if user.username else "نەدیار"
    name = user.first_name

    balances = load_data(BALANCE_FILE)
    balance = balances.get(user_id, 0)

    profile_text = (
        f"╔══════════════════════╗\n"
        f" 🛡 **سەنتەرێ پڕۆفیشناڵ یێ هاک و ڕاپۆرتان**\n"
        f"╚══════════════════════╝\n\n"
        f"👤 **پڕۆفایلێ بەکارهێنەری:**\n"
        f"• **ناڤ:** {name}\n"
        f"• **یوزەرنەیم:** `{username}`\n"
        f"• **باڵانسا نها:** `💎 {balance} کلیل`\n\n"
        f"🎁 **دیارییا دەمەکی (هر 4 دەمژمێران):**\n"
        f"⏱ دۆخ: `ڤەکری و بەرهەڤ بۆ وەرگرتنێ`"
    )

    keyboard = [
        [InlineKeyboardButton("🎁 وەرگرتنا 5 کلیلێن بەلاش", callback_data="claim_gift")],
        [
            InlineKeyboardButton("📊 سيستەمێ 5000 ڕاپۆرتان", callback_data="menu_reports"),
            InlineKeyboardButton("🛒 کڕینا کلیلان (تەماس)", url="https://t.me/YUSEEF_SURCHI"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(profile_text, parse_mode="Markdown", reply_markup=reply_markup)
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        try:
            await query.edit_message_text(text=profile_text, parse_mode="Markdown", reply_markup=reply_markup)
        except:
            pass


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = str(query.from_user.id)

    if data == "back_to_start":
        await start(update, context)

    elif data == "menu_reports":
        report_menu = (
            "🌌 **ناڤەندا کۆنتڕۆلا 5000 ڕاپۆرتێن جیهانی**\n\n"
            "• هەموو ئامرازێن هێرش و ڕاپۆرتان ب شێوەیەکێ خودکار کار دکەن.\n"
            "• هەر 1 کلیل = 5 کردارێن سەرپێچییێ.\n\n"
            "👇 پەڕەیا خۆ بژێرە بۆ بینینا لستان:"
        )
        report_keyboard = [
            [InlineKeyboardButton("📄 پەڕەیا 1 (دەستپێک)", callback_data="page_0")],
            [InlineKeyboardButton("🛒 کڕینا باڵانسی (راستەوخۆ)", url="https://t.me/YUSEEF_SURCHI")],
            [InlineKeyboardButton("🔙 پاشڤە (دەستپێکێ)", callback_data="back_to_start")],
        ]
        await query.edit_message_text(text=report_menu, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(report_keyboard))

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

        rep_keyboard.append([InlineKeyboardButton("🔙 پاشڤە (دەستپێکێ)", callback_data="back_to_start")])

        await query.edit_message_text(
            text=f"⚡ **لستا فەرمیا ڕاپۆرتان (پەڕە {page_idx + 1} ژ {total_pages}):**",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(rep_keyboard),
        )

    elif data.startswith("execute_"):
        rep_key = data.replace("execute_", "")
        report_name, emoji = MASSIVE_REPORT_TYPES.get(rep_key, ("تشتێ خراب", "⚠️"))
        await query.answer(
            f"{emoji} سەرکەفتن! داخوازییا ڕاپۆرتێ بۆ ({report_name}) ب سەرکەفتن هاتە هنارتن.",
            show_alert=True,
        )

    elif data == "claim_gift":
        cooldowns = load_data(COOLDOWN_FILE)
        current_time = time.time()
        last_claim = cooldowns.get(user_id, 0)
        
        cooldown_time = 4 * 3600 # 4 دەمژمێر
        
        if current_time - last_claim < cooldown_time:
            remaining_sec = int(cooldown_time - (current_time - last_claim))
            rem_hours = remaining_sec // 3600
            rem_mins = (remaining_sec % 3600) // 60
            await query.answer(
                f"⚠️ هێشتا دەمێ وەرگرتنا دیارییا تە نەهاتیە! ل هیڤیا {rem_hours} دەمژمێر و {rem_mins} خولەکان بن.",
                show_alert=True
            )
            return

        balances = load_data(BALANCE_FILE)
        current_bal = balances.get(user_id, 0)
        balances[user_id] = current_bal + 5
        save_data(BALANCE_FILE, balances)

        cooldowns[user_id] = current_time
        save_data(COOLDOWN_FILE, cooldowns)

        await query.answer(
            "🎁 پیرۆزە! 5 کلیلێن بەلاش ب سەرکەفتن هاتنە زێدەکرن بۆ پڕۆفایلا تە.", show_alert=True
        )
        await start(update, context)


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("بۆتێ 5000 ڕاپۆرتان ب دیزاینەکا خەیالی یێ ئامادەیە و کار دکەت...")
    app.run_polling()

if __name__ == "__main__":
    main()
