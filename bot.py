import json
import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# خوێندنا توکنی ژ ژینگەها Railway یان دانانا وێ ب رەق
TOKEN = os.getenv("BOT_TOKEN", "8680499622:AAHTpgQXyGKyFATDolT6tmBH4USgct1HU4A")

BALANCE_FILE = "balances.json"


def load_balances():
  if os.path.exists(BALANCE_FILE):
    with open(BALANCE_FILE, "r") as f:
      try:
        return json.load(f)
      except:
        return {}
  return {}


def save_balances(balances):
  with open(BALANCE_FILE, "w") as f:
    json.dump(balances, f)


# دروستکرنا لستا زەبەلاح و پڕ تشتێن مەترسیدار، هاککەری و بندکرنا کەناڵان ژ 1 هەتا 5000
MASSIVE_REPORT_TYPES = {
    "rep_1": ("🚨 سپام و ڤیدیۆکێن بێ مانا (Spam & Junk)", "🚨"),
    "rep_2": ("🔞 بڵاڤکرنا ناڤەرۆکا نەشیاو (NSFW / 18+ Content)", "🔞"),
    "rep_3": ("⚠️ توندوتیژی و هشکەڤرۆتی (Violence & Gore)", "⚠️"),
    "rep_4": ("🔪 ترۆرسڤان و چەکدار (Terrorism & Militancy)", "🔪"),
    "rep_5": ("💸 فێلبازی و سکام (Scam & Financial Fraud)", "💸"),
    "rep_6": ("🔗 لینکێن نەیاسایی و ڤایرۆس (Malicious Links)", "🔗"),
    "rep_7": ("💊 فرۆتنا ماددەیێن هوشْبەر (Drugs & Narcotics)", "💊"),
    "rep_8": ("🔫 فرۆتنا چەکان (Illegal Arms Trading)", "🔫"),
    "rep_9": ("🛑 قەدەغەکرنا مافێ مرۆڤی (Human Rights Violation)", "🛑"),
    "rep_10": ("🎭 خۆخاپاندن و ناسناما درۆین (Fake Identity)", "🎭"),
    "rep_11": ("💻 هێرشا ڕاوەستاندنا کەناڵێ (Channel DDoS Sabotage)", "💻"),
    "rep_12": ("🔓 هاککرن و دزینا کەناڵێن تەلەگرام (Telegram Channel Heist)", "🔓"),
    "rep_13": ("🛡 لادانا ئەدمنێن سەرەکی و کۆنترۆلا کەناڵی (Admin Session Revoke)", "🛡"),
    "rep_14": ("🕵️ دزینا کووکی و تۆکنا بۆتان (Bot Token & Session Stealer)", "🕵️"),
    "rep_15": ("🦠 بەلاڤکرنا ڕانسۆموێر بۆ بندکرنا سێرڤەرا (Ransomware Attack)", "🦠"),
    "rep_16": ("📡 هێرشێن فیشینگ بۆ دزینا پاسۆپۆرتا (Advanced Phishing Heist)", "📡"),
    "rep_17": ("⚡ شکاندنا کلیل و سکیورتییا گروپان (Group Security Bypass)", "⚡"),
    "rep_18": ("🌐 هێرشێن SQL Injection بۆ بانک و لستێن کەناڵان", "🌐"),
    "rep_19": ("⚙️ بەلاڤکرنا 0-Day Exploit بۆ شکستپێکرنا ئەپڵیکەیشنان", "⚙️"),
    "rep_20": ("📥 دانانا باکدۆران (Backdoor Trojan بۆ کۆنترۆلا تەواو)", "📥"),
}

for i in range(21, 5001):
  if i % 4 == 0:
    emoji = "🔓"
    title = f"هێرشا هاککرن و دزینا کەناڵێ ژمارە {i} (Channel Hack Tool)"
  elif i % 4 == 1:
    emoji = "💻"
    title = f"سایبەر هێرش و پێشێلکارییا دیجیتالی ژمارە {i} (Cyber Sabotage)"
  elif i % 4 == 2:
    emoji = "🚨"
    title = f"سەرپێچی و شکاندنا ڕێنماییێن تەلەگرام ژمارە {i} (Telegram Breach)"
  else:
    emoji = "⚠️"
    title = f"چاڵاکیا مەترسیدار و هاککەری ژمارە {i} (Security Exploit)"
  MASSIVE_REPORT_TYPES[f"rep_{i}"] = (title, emoji)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user = update.effective_user
  user_id = str(user.id)
  username = f"@{user.username}" if user.username else "نەدیار"
  name = user.first_name

  balances = load_balances()
  balance = balances.get(user_id, 0)

  profile_text = (
      f"👤 **پڕۆفایلێ تە یێ پڕۆفیشناڵ**\n\n"
      f"• ناڤ: {name}\n"
      f"• یوزەرنەیم: `{username}`\n"
      f"• باڵانس: `{balance} کلیل`\n\n"
      f"🎁 دۆخا دیارییا دەمەکی: ڤەکرییە!\n"
      f"⏱ هەر 4 بۆ 5 دەمژمێران 5 کلیلان وەرگرە."
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
      await query.edit_message_text(
          text=profile_text, parse_mode="Markdown", reply_markup=reply_markup
      )
    except:
      pass


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()
  data = query.data
  user_id = str(query.from_user.id)

  if data == "back_to_start":
    username = f"@{query.from_user.username}" if query.from_user.username else "نەدیار"
    balances = load_balances()
    balance = balances.get(user_id, 0)

    profile_text = (
        f"👤 **پڕۆفایلێ تە**\n\n"
        f"• یوزەرنەیم: `{username}`\n"
        f"• باڵانس: `{balance} کلیل`\n\n"
        f"🎁 دیارییا خۆ وەگرە یان دەست ب پشکاندنا ڕاپۆرتان بکە!"
    )
    keyboard = [
        [InlineKeyboardButton("🎁 وەرگرتنا دیارییا (5 کلیل)", callback_data="claim_gift")],
        [InlineKeyboardButton("📊 سيستەمێ 5000 ڕاپۆرتان", callback_data="menu_reports")],
        [InlineKeyboardButton("📢 کەناڵێ فەرمی", url="https://t.me/YUSEEF_SURCHI")],
    ]
    await query.edit_message_text(
        text=profile_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
    )

  elif data == "menu_reports":
    report_menu = (
        "⚠️ **سیستەمێ زەبەلاح یێ 5000 ڕاپۆرتان و هاککرنا کەناڵان**\n\n"
        "بۆت نوکە پڕبوویە ژ تەواویا **5000** جۆرێن سەرپێچییێن جیهانی!\n"
        "• 1 کلیل = 5 ڕاپۆرت\n"
        "• 5 کلیل = 50 ڕاپۆرت\n"
        "• 10 کلیل = 100 ڕاپۆرت\n\n"
        "👇 پەڕەیا خۆ بژێرە بۆ بینینا ڕاپۆرتان:"
    )
    report_keyboard = [
        [InlineKeyboardButton("📄 پەییا 1 (rep_1 بۆ rep_10)", callback_data="page_1")],
        [InlineKeyboardButton("🛒 بۆ کڕینێ سەرەدانا چاتێ بکە", url="https://t.me/YUSEEF_SURCHI")],
        [InlineKeyboardButton("🔙 پاشڤە (Back)", callback_data="back_to_start")],
    ]
    await query.edit_message_text(
        text=report_menu, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(report_keyboard)
    )

  elif data.startswith("page_"):
    page_num = int(data.replace("page_", ""))
    items_list = list(MASSIVE_REPORT_TYPES.items())
    per_page = 8
    start_idx = (page_num - 1) * per_page
    end_idx = start_idx + per_page

    current_items = items_list[start_idx:end_idx]
    rep_keyboard = []

    for key_code, (title, emoji) in current_items:
      rep_keyboard.append(
          [InlineKeyboardButton(f"{emoji} {title[:30]}...", callback_data=f"execute_{key_code}")]
      )

    # دوگمەیێن پەیجینگی (پێش و پاش)
    nav_buttons = []
    if page_num > 1:
      nav_buttons.append(
          InlineKeyboardButton("⬅️ پێشتر", callback_data=f"page_{page_num - 1}")
      )
    if end_idx < len(items_list):
      nav_buttons.append(
          InlineKeyboardButton("دواتر ➡️", callback_data=f"page_{page_num + 1}")
      )

    if nav_buttons:
      rep_keyboard.append(nav_buttons)

    rep_keyboard.append([InlineKeyboardButton("🔙 پاشڤە بۆ مێنۆیا سەرەکی", callback_data="menu_reports")])

    await query.edit_message_text(
        text=f"📌 **لستا ڕاپۆرتان (پەڕە {page_num} ژ {len(items_list)//per_page}):**",
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
    balances = load_balances()
    current_bal = balances.get(user_id, 0)
    balances[user_id] = current_bal + 5
    save_balances(balances)
    await query.answer(
        "🎁 پیرۆزە براتە عزیز! 5 کلیلان بۆ باڵانسا تە هاتە زێدەکرن.", show_alert=True
    )
    # نووکرنا مێنۆیا سەرەکی ب باڵانسا نوو
    await start(update, context)

  elif data == "buy_keys":
    await query.answer("🛒 بۆ کڕینا کلیلان سەرەدانا چاتێ بکە: @YUSEEF_SURCHI", show_alert=True)


def main():
  app = ApplicationBuilder().token(TOKEN).build()
  app.add_handler(CommandHandler("start", start))
  app.add_handler(CallbackQueryHandler(button_handler))

  print("بۆتێ 5000 ڕاپۆرتان و هاککرنا کەناڵان ب تەواوی یێ ئامادەیە و کار دکەت...")
  app.run_polling()


if __name__ == "__main__":
  main()
