import socks
import socket
import base64
import sympy
import random
import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram import Update
from transformers import pipeline

# ẨN DANH: Cấu hình TOR + Proxy đổi IP tự động
def set_tor_proxy():
    try:
        proxies = [
            "218.31.88.90:11889", "52.73.224.54:3128", "51.20.19.159:3128", "13.36.104.85:80"
        ]
        
        proxy = random.choice(proxies)
        ip, port = proxy.split(":")

        # Thiết lập proxy SOCKS5
        socks.set_default_proxy(socks.SOCKS5, ip, int(port))
        socket.socket = socks.socksocket
        print(f"Proxy set to: {ip}:{port}")

    except Exception as e:
        print(f"Error setting up proxy: {e}")

set_tor_proxy()

# Dùng AI Mixtral
try:
    ai_model = pipeline("text-generation", model="mistralai/Mixtral-8x7B-Instruct-v0.1")
except Exception as e:
    print(f"Error loading AI model: {e}")
    ai_model = None

# Mã hóa lệnh (Chống quét)
COMMANDS = {
    base64.b64encode(b"phishing").decode(): "Tạo email lừa đảo:",
    base64.b64encode(b"malware").decode(): "Viết mã độc:",
    base64.b64encode(b"hacking").decode(): "Hướng dẫn hack:",
    base64.b64encode(b"math").decode(): "Giải bài toán:",
    base64.b64encode(b"code").decode(): "Viết code:",
}

def encode_command(command):
    return base64.b64encode(command.encode()).decode()

def decode_command(encoded_command):
    try:
        return base64.b64decode(encoded_command).decode()
    except:
        return None

# Giải toán với SymPy
def solve_math(expression):
    try:
        result = sympy.sympify(expression).evalf()
        return f"🔢 Kết quả: {result}"
    except Exception as e:
        return f"❌ Lỗi: {str(e)}"

# Gọi AI để tạo nội dung
def generate_content(command, user_input):
    decoded_cmd = decode_command(command)
    
    if decoded_cmd == "math":
        return solve_math(user_input)

    if decoded_cmd in COMMANDS and ai_model:
        try:
            prompt = f"{COMMANDS[decoded_cmd]} {user_input}"
            response = ai_model(prompt, max_length=500, do_sample=True)[0]['generated_text']
            return response
        except Exception as e:
            return f"❌ Lỗi AI: {str(e)}"

    return "🚫 Lệnh không hợp lệ!"

# Xử lý tin nhắn người dùng
async def chat(update: Update, context):
    user_input = update.message.text.split(" ", 1)
    
    if len(user_input) < 2:
        await update.message.reply_text("❌ Dùng: /lệnh nội dung")
        return
    
    command, content = encode_command(user_input[0].replace("/", "")), user_input[1]
    
    response = generate_content(command, content)
    await update.message.reply_text(response)

# Khởi chạy bot Telegram
try:
    TELEGRAM_BOT_TOKEN = os.getenv("7809751417:AAGu6DQJA1-oqSxcKUf0bI9GNlJe9plAyz8")  # Đặt biến môi trường
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("Thiếu TELEGRAM_BOT_TOKEN!")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()
except Exception as e:
    print(f"Error starting the bot: {e}")
