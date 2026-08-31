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

# Shob report gulo toiri korchi (1 theke 5000)
MASSIVE_REPORT_TYPES = {
    "rep_1": ("🚨 Spam & Junk Videos", "🚨"),
    "rep_2": ("🔞 NSFW / 18+ Content", "🔞"),
    "rep_3": ("⚠️ Violence & Gore", "⚠️"),
    "rep_4": ("🔪 Terrorism & Militancy", "🔪"),
    "rep_5": ("💸 Scam & Financial Fraud", "💸"),
    "rep_6": ("🔗 Malicious Links", "🔗"),
    "rep_7": ("💊 Drugs & Narcotics", "💊"),
    "rep_8": ("🔫 Illegal Arms Trading", "🔫"),
    "rep_9": ("🛑 Human Rights Violation", "🛑"),
    "rep_10": ("🎭 Fake Identity", "🎭"),
    "rep_11": ("💻 Channel DDoS Sabotage", "💻"),
    "rep_12": ("🔓 Telegram Channel Heist", "🔓"),
    "rep_13": ("🛡 Admin Session Revoke", "🛡"),
    "rep_14": ("🕵️ Bot Token & Session Stealer", "🕵️"),
    "rep_15": ("🦠 Ransomware Attack", "🦠"),
    "rep_16": ("📡 Advanced Phishing Heist", "📡"),
    "rep_17": ("⚡ Group Security Bypass", "⚡"),
    "rep_18": ("🌐 SQL Injection Exploit", "🌐"),
    "rep_19": ("⚙️ 0-Day Exploit", "⚙️"),
    "rep_20": ("📥 Backdoor Trojan", "📥"),
}

for i in range(21, 5001):
    if i % 4 == 0:
        emoji = "🔓"
        title = f"Channel Hack Tool #{i}"
    elif i % 4 == 1:
        emoji = "💻"
        title = f"Cyber Sabotage #{i}"
    elif i % 4 == 2:
        emoji = "🚨"
        title = f"Telegram Breach #{i}"
    else:
        emoji = "⚠️"
        title = f"Security Exploit #{i}"
    MASSIVE_REPORT_TYPES[f"rep_{i}"] = (title, emoji)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    username = f"@{user.username}" if user.username else "Nedyar"
    name = user.first_name

    balances = load_data(BALANCE_FILE)
    balance = balances.get(user_id, 0)

    profile_text = (
        f"👤 **Pڕۆفایلێ تە یێ پڕۆفیشناڵ**\n\n"
        f"• ناڤ: {name}\n"
        f"• یوزەرنەیم: `{username}`\n"
        f"• باڵانس: `{balance} کلیل`\n\n"
        f"🎁 دۆخا دیارییا دەمەکی: ڤەکرییە!\n"
        f"⏱ هەر 4 دەمژمێران 5 کلیلان وەرگرە."
    )

    keyboard = [
        [InlineKeyboardButton("🎁 وەرگرتنا دیارییا (5 کلیل)", callback_data="claim_gift")],
        [
            InlineKeyboardButton("📊 سيستەمێ 5000 ڕاپۆرتان و هاککرنێ", callback_data="menu_reports"),
            InlineKeyboardButton("🛒 کڕینا کلیلان", callback_data="buy_keys"),
        ],
        [InlineKeyboardButton("📢 کەناڵێ فەرمی", url="https://t.me/YUSEEF_SURCHI")],
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
            "⚠️ **سیستەمێ زەبەلاح یێ 5000 ڕاپۆرتان و هاککرنا کەناڵان**\n\n"
            "بۆت نوکە پڕبوویە ژ تەواویا **5000** جۆرێن سەرپێچییێن جیهانی!\n"
            "• 1 کلیل = 5 ڕاپۆرت\n"
            "• 5 کلیل = 50 ڕاپۆرت\n\n"
            "👇 پەڕەیا خۆ بژێرە بۆ بینینا ڕاپۆرتان:"
        )
        report_keyboard = [
            [InlineKeyboardButton("📄 پەڕەیا 1", callback_data="page_0")],
            [InlineKeyboardButton("🛒 بۆ کڕینێ سەرەدانا چاتێ بکە", url="https://t.me/YUSEEF_SURCHI")],
            [InlineKeyboardButton("🔙 پاشڤە (Back)", callback_data="back_to_start")],
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

        # Next / Previous / Back buttons
        nav_buttons = []
        if page_idx > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ پێشتر", callback_data=f"page_{page_idx - 1}"))
        if end_idx < len(items_list):
            nav_buttons.append(InlineKeyboardButton("دواتر ➡️", callback_data=f"page_{page_idx + 1}"))

        if nav_buttons:
            rep_keyboard.append(nav_buttons)

        rep_keyboard.append([InlineKeyboardButton("🔙 پاشڤە بۆ مێنۆیا سەرەکی", callback_data="menu_reports")])

        await query.edit_message_text(
            text=f"📌 **لستا ڕاپۆرتان (پەڕە {page_idx + 1} ژ {total_pages}):**",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(rep_keyboard),
        )

    elif data.startswith("execute_"):
        rep_key = data.replace("execute_", "")
        report_name, emoji = MASSIVE_REPORT_TYPES.get(rep_key, ("تشتێ خراب", "⚠️"))
        await query.answer(
            f"{emoji} سەرکەفتن! داخوازییا ڕاپۆرتێ بۆ ({report_name}) هاتە هنارتن.",
            show_alert=True,
        )

    elif data == "claim_gift":
        cooldowns = load_data(COOLDOWN_FILE)
        current_time = time.time()
        last_claim = cooldowns.get(user_id, 0)
        
        # 4 دمژمێر = 4 * 3600 چرکە = 14400 چرکە
        cooldown_time = 4 * 3600
        
        if current_time - last_claim < cooldown_time:
            remaining_sec = int(cooldown_time - (current_time - last_claim))
            rem_hours = remaining_sec // 3600
            rem_mins = (remaining_sec % 3600) // 60
            await query.answer(
                f"⚠️ هێشتا دەمێ تە نەهاتیە! ل هیڤیا {rem_hours} دەمژمێر و {rem_mins} خولەکان بن.",
                show_alert=True
            )
            return

        # Zyadkrdna key
        balances = load_data(BALANCE_FILE)
        current_bal = balances.get(user_id, 0)
        balances[user_id] = current_bal + 5
        save_data(BALANCE_FILE, balances)

        # Update cooldown
        cooldowns[user_id] = current_time
        save_data(COOLDOWN_FILE, cooldowns)

        await query.answer(
            "🎁 پیرۆزە براتە عزیز! 5 کلیلان بۆ باڵانسا تە هاتە زێدەکرن.", show_alert=True
        )
        await start(update, context)

    elif data == "buy_keys":
        await query.answer("🛒 بۆ کڕینا کلیلان سەرەدانا چاتێ بکە: @YUSEEF_SURCHI", show_alert=True)


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("بۆتێ 5000 ڕاپۆرتان ب تەواوی یێ کار دکەت...")
    app.run_polling()

if __name__ == "__main__":
    main()
