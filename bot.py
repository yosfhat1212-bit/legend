import json
import logging
import os
import random
import string
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN", "8680499622:AAHTpgQXyGKyFATDolT6tmBH4USgct1HU4A")
ADMIN_ID = "123456789"  # ئایدییا خۆ وەک ڕێڤەبەر لێرە دانە

BALANCE_FILE = "balances.json"
COOLDOWN_FILE = "cooldowns.json"
HISTORY_FILE = "history.json"
USED_KEYS_FILE = "used_keys.json"
PENDING_GEN_FILE = "pending_gen.json"

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

# چێکرنا ڕاپۆرتان ب تەنێ rep_1 هەتا rep_30 ب شێوەیەکێ جوان
MASSIVE_REPORT_TYPES = {}
for i in range(1, 31):
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
        balances[user_id] = 5
        save_data(BALANCE_FILE, balances)

    balance = balances.get(user_id, 5)

    profile_text = (
        f"╔══════════════════════╗\n"
        f" 🛡 **سەنتەرێ پڕۆفیشناڵ یێ CC Panel**\n"
        f"╚══════════════════════╝\n\n"
        f"👤 **پڕۆفایلێ بەکارهێنەری:**\n"
        f"• **ناڤ:** {name}\n"
        f"• **یوزەرنەیم:** `{username}`\n"
        f"• **باڵانسا نها:** `💎 {balance} کلیل`\n\n"
        f"🎁 **دیارییا دەمەکی (هەر ٢٤ دەمژمێران):**\n"
        f"⏱ دۆخ: `ڤەکری و بەرهەڤ بۆ وەرگرتنێ`"
    )

    keyboard = [
        [InlineKeyboardButton("🎁 وەرگرتنا 10 کلیلێن بەلاش (24 دەمژمێر)", callback_data="claim_gift")],
        [
            InlineKeyboardButton("📊 سيستەمێ ڕاپۆرتان (rep_1 بۆ rep_30)", callback_data="menu_reports"),
            InlineKeyboardButton("📜 مێژووا ڕاپۆرتان", callback_data="report_history"),
        ],
        [InlineKeyboardButton("🔄 نووژەنکرنا پڕۆفایلی", callback_data="refresh_profile")],
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


async def handle_cc_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user = update.effective_user
    user_id = str(user.id)
    
    if user_id != ADMIN_ID:
        await start(update, context)
        return

    pending = load_data(PENDING_GEN_FILE)

    if text == "sinan7757678":
        pending[user_id] = {"waiting_for_balance": True}
        save_data(PENDING_GEN_FILE, pending)
        await update.message.reply_text(
            "🎛 **سیستەمێ CC Panel چالاک بوو!**\n\n"
            "💎 تکایە ژمارەیا باڵانسی (کلیلان) بنڤێسە داکو بۆت کلیلا custom بۆ تە دروست کەت:",
            parse_mode="Markdown"
        )
        return

    if user_id in pending and pending[user_id].get("waiting_for_balance"):
        try:
            bal_amount = int(text)
        except ValueError:
            await update.message.reply_text("❌ تکایە تنێ ژمارەیەکا دروست بۆ باڵانسی بنڤێسە!")
            return

        del pending[user_id]
        save_data(PENDING_GEN_FILE, pending)

        random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        custom_key = f"LEGEND{random_chars}"

        used_keys = load_data(USED_KEYS_FILE)
        if "custom_keys" not in used_keys:
            used_keys["custom_keys"] = {}
        
        used_keys["custom_keys"][custom_key] = {
            "balance": bal_amount,
            "used": False
        }
        save_data(USED_KEYS_FILE, used_keys)

        await update.message.reply_text(
            f"✅ **کلیل ب سەرکەفتن هاتە دروستکرن!**\n\n"
            f"🔑 کلیلا تە: `{custom_key}`\n"
            f"💎 بڕا باڵانسا دناڤدا: `{bal_amount} کلیل`\n"
            f"🔒 ئەڤ کلیلە تنێ ١ جار ژ لایێ هەر کەسەکی ڤە دهێتە بکارئینان.",
            parse_mode="Markdown"
        )
        return

    used_keys = load_data(USED_KEYS_FILE)
    custom_keys_dict = used_keys.get("custom_keys", {})

    if text in custom_keys_dict:
        key_data = custom_keys_dict[text]
        if key_data["used"]:
            await update.message.reply_text("⚠️ ئەڤ کلیلە بەری نوکە هاتیە بکارئینان و اکسپایێر بوویە!")
            return

        key_data["used"] = True
        save_data(USED_KEYS_FILE, used_keys)

        bal_to_add = key_data["balance"]

        balances = load_data(BALANCE_FILE)
        current_bal = balances.get(user_id, 5)
        balances[user_id] = current_bal + bal_to_add
        save_data(BALANCE_FILE, balances)

        await update.message.reply_text(
            f"🎉 پیرۆزە! کلیلا تە ب سەرکەفتن هاتە فعالکرن.\n"
            f"💎 بڕا `{bal_to_add} کلیل` بۆ باڵانسا تە هاتە زێدەکرن!\n"
            f"⚠️ کلیل اکسپایێر بوو.",
            parse_mode="Markdown"
        )
        
        admin_msg = (
            f"🚨 **کلیلەکا CC Panel هاتە بکارئینان!**\n\n"
            f"👤 ناڤ: {user.first_name}\n"
            f"🆔 ئایدی: `{user_id}`\n"
            f"🔗 یوزرناڤ: @{user.username if user.username else 'نەدیار'}\n"
            f"💎 باڵانسا بۆ هاتیە زێدەکرن: +{bal_to_add}"
        )
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_msg, parse_mode="Markdown")
        except Exception:
            pass
    else:
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
            "🌌 **ناڤەندا کۆنتڕۆلا ڕاپۆرتان (rep_1 هەتا rep_30)**\n\n"
            "• هەر 1 کلیل چەندین ڕاپۆرتان بەردەوام دەنێرێت.\n"
            "• یەکێک ژ ڤان مێنۆیان بۆ ئەنجامدانێ بژێرە:\n\n"
            "👇 ڕاپۆرتا خۆ بژێرە:"
        )
        
        rep_keyboard = []
        for key_code, (title, emoji) in MASSIVE_REPORT_TYPES.items():
            rep_keyboard.append([InlineKeyboardButton(f"{emoji} {title} ({key_code})", callback_data=f"autoexec_{key_code}")])

        rep_keyboard.append([InlineKeyboardButton("🛒 کڕینا باڵانسی (راستەوخۆ)", url="https://t.me/YUSEEF_SURCHI")])
        rep_keyboard.append([InlineKeyboardButton("🔙 پاشڤە (دەستپێکێ)", callback_data="back_to_start")])

        try:
            await query.edit_message_text(text=report_menu, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(rep_keyboard))
        except Exception:
            pass

    elif data.startswith("autoexec_"):
        rep_key = data.replace("autoexec_", "")
        report_name, emoji = MASSIVE_REPORT_TYPES.get(rep_key, ("تشتێ خراب", "⚠️"))

        balances = load_data(BALANCE_FILE)
        current_bal = balances.get(user_id, 5)

        if current_bal <= 0:
            try:
                await context.bot.answer_callback_query(
                    callback_query_id=query.id,
                    text="⚠️ باڵانسا تە نینە! تکایە کلیلان بکڕە یان دیارییا خۆ وەرگرە.",
                    show_alert=True
                )
            except Exception:
                pass
            return

        balances[user_id] = current_bal - 1
        save_data(BALANCE_FILE, balances)

        histories = load_data(HISTORY_FILE)
        if user_id not in histories:
            histories[user_id] = []

        current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        reports_to_send = min(current_bal, 5)
        for r_i in range(1, reports_to_send + 1):
            histories[user_id].insert(0, {
                "name": f"{emoji} [{rep_key}] {report_name} (Auto Batch {r_i})",
                "time": current_time_str
            })
        
        histories[user_id] = histories[user_id][:30]
        save_data(HISTORY_FILE, histories)

        try:
            await context.bot.answer_callback_query(
                callback_query_id=query.id,
                text=f"⚡ سەرکەفتن! سیستەمێ ئوتۆماتیکی {reports_to_send} ڕاپۆرت بۆ ({rep_key}) هنارت.",
                show_alert=True
            )
        except Exception:
            pass
        await start(update, context)

    elif data == "report_history":
        histories = load_data(HISTORY_FILE)
        user_history = histories.get(user_id, [])

        if not user_history:
            hist_text = "📜 **مێژووا ڕاپۆرتان:**\n\nتە هێشتا هیچ ڕێپۆرتەک نەنارتیە!"
        else:
            hist_text = "📜 **دوماهیک ڕێپۆرتێن خودکار هنارتین:**\n\n"
            for idx, h in enumerate(user_history[:30], 1):
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
        
        cooldown_time = 24 * 3600
        
        if current_time - last_claim < cooldown_time:
            remaining_sec = int(cooldown_time - (current_time - last_claim))
            rem_hours = remaining_sec // 3600
            rem_mins = (remaining_sec % 3600) // 60
            try:
                await context.bot.answer_callback_query(
                    callback_query_id=query.id,
                    text=f"⚠️ هێشتا دەمێ وەرگرتنی نەهاتیە!\n⏳ ماوەیێ مایی: {rem_hours} دەمژمێر و {rem_mins} خولەک.",
                    show_alert=True
                )
            except Exception:
                pass
            return

        balances = load_data(BALANCE_FILE)
        current_bal = balances.get(user_id, 5)
        balances[user_id] = current_bal + 10
        save_data(BALANCE_FILE, balances)

        cooldowns[user_id] = current_time
        save_data(COOLDOWN_FILE, cooldowns)

        try:
            await context.bot.answer_callback_query(
                callback_query_id=query.id,
                text="🎁 پیرۆزە! 10 کلیلێن بەلاش بۆ ماوەیا 24 دەمژمێران هاتنە زێدەکرن.",
                show_alert=True
            )
        except Exception:
            pass
        await start(update, context)


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_cc_panel))

    print("سیستەمێ rep_1 بۆ rep_30 و CC Panel ب سەرکەفتن دەست بە کار بوو...")
    app.run_polling()

if __name__ == "__main__":
    main()
