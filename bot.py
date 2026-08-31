import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TOKEN = "8680499622:AAHTpgQXyGKyFATDolT6tmBH4USgct1HU4A"

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
    # پشکێن تایبەت یێن هاککرنا کەناڵان، گرووپا و هێرشێن سایبەر
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

# پڕکرنا لستێ ب شێوەیەکێ خودکار و زیرەک ژ (21 هەتا 5000) دگەل هەموو سەرپێچی و تشتێن هاککرنا کەناڵان
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
  username = f"@{user.username}" if user.username else "نەدیار"
  name = user.first_name
  balance = 0

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
    await query.edit_message_text(
        text=profile_text, parse_mode="Markdown", reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()
  data = query.data

  if data == "back_to_start":
    user = update.effective_user
    username = f"@{user.username}" if user.username else "نەدیار"
    balance = 0
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
        "بۆت نوکە پڕبوویە ژ تەواویا **5000** جۆرێن سەرپێچییێن جیهانی و ئامرازێن هاککرنا کەناڵ و گرووپان!\n"
        "• 1 کلیل = 5 ڕاپۆرت\n"
        "• 5 کلیل = 50 ڕاپۆرت\n"
        "• 10 کلیل = 100 ڕاپۆرت\n"
        "• 150 کلیل = 1000 ڕاپۆرت (بۆ بندکرنا کەناڵان ب ڕاستی)\n\n"
        "👇 پشکەکا نموونەیی ژ لستا 5000 دانەیی بژێرە:"
    )
    report_keyboard = [
        [InlineKeyboardButton("📂 نیشاندانا پشکا 1 (نموونا 10 سەرەکی)", callback_data="rep_page_1")],
        [InlineKeyboardButton("🛒 بۆ کڕینێ سەرەدانا چاتێ بکە", url="https://t.me/YUSEEF_SURCHI")],
        [InlineKeyboardButton("🔙 پاشڤە (Back)", callback_data="back_to_start")],
    ]
    await query.edit_message_text(
        text=report_menu, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(report_keyboard)
    )

  elif data == "rep_page_1":
    items = list(MASSIVE_REPORT_TYPES.items())[:10]
    rep_keyboard = []
    for key_code, (title, emoji) in items:
      rep_keyboard.append(
          [InlineKeyboardButton(f"{emoji} {title}", callback_data=f"execute_{key_code}")]
      )
    rep_keyboard.append([InlineKeyboardButton("🔙 پاشڤە بۆ مێنۆیا سەرەکی", callback_data="menu_reports")])
    await query.edit_message_text(
        text="📌 **لستا نموونەیی (ژ کۆما 5000 تشتێن خراب و هاککرنا کەناڵان):**",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(rep_keyboard),
    )

  elif data.startswith("execute_"):
    rep_key = data.replace("execute_", "")
    report_name, emoji = MASSIVE_REPORT_TYPES.get(rep_key, ("تشتێ خراب", "⚠️"))
    await query.answer(
        f"{emoji} سەرکەفتن! داخوازییا هاککرن و ڕاپۆرتێ بۆ ({report_name}) هاتە هنارتن.",
        show_alert=True,
    )

  elif data == "claim_gift":
    await query.answer(
        "🎁 پیرۆزە براتە عزیز! 5 کلیلان بۆ باڵانسا تە هاتە زێدەکرن.", show_alert=True
    )

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
