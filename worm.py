import socks
import socket
import base64
import sympy
import random
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram import Update
from transformers import pipeline

# ẨN DANH: Cấu hình TOR + Proxy đổi IP tự động

def set_tor_proxy():
    try:
        # List of proxies
        proxies = [
            "218.31.88.90:11889", "52.73.224.54:3128", "51.20.19.159:3128", "13.36.104.85:80",
            "41.59.90.171:80", "8.211.49.86:10000", "162.223.90.130:80", "202.63.172.18:9128",
            "103.124.137.150:20", "47.91.29.151:9080", "18.228.149.161:80", "52.16.232.164:3128",
            "80.249.112.162:80", "44.219.175.186:80", "58.243.224.244:8085", "15.156.24.206:3128",
            "54.179.39.14:3128", "3.97.176.251:3128", "184.73.68.87:11", "51.16.199.206:3128",
            "106.38.26.22:2080", "218.13.39.150:9091", "103.49.202.252:80", "180.184.79.187:12798",
            "177.93.49.203:999", "119.3.113.152:9094", "13.37.59.99:3128", "139.215.92.20:10005",
            "13.56.192.187:80", "111.34.79.216:10219", "13.246.209.48:1080", "54.152.3.36:80",
            "8.215.3.250:90", "183.215.23.242:9091", "58.23.152.29:7080", "218.1.197.106:2324",
            "38.54.116.9:4000", "51.20.50.149:3128", "185.105.102.189:80", "13.208.56.180:80",
            "8.208.85.34:6969", "67.43.228.253:13087", "43.200.77.128:3128", "27.189.130.203:8089",
            "135.181.154.225:80", "194.190.70.200:3128", "204.236.137.68:80", "87.248.129.32:80",
            "67.43.228.250:29003", "67.43.236.21:14883", "183.234.215.11:8443", "47.123.4.107:9100",
            "72.10.160.174:1971", "8.211.49.86:8443", "3.139.242.184:80", "43.201.121.81:80",
            "58.144.141.26:12798", "5.135.103.166:80", "51.89.255.67:80", "38.54.116.9:3128",
            "47.89.184.18:3128", "43.202.154.212:80", "15.236.203.245:3128", "72.10.160.170:16285",
            "116.228.73.230:650", "189.240.60.162:9090", "27.189.131.179:8089", "37.187.25.85:80",
            "196.1.95.124:80", "152.231.88.213:999", "52.26.114.229:1080", "13.59.156.167:3128",
            "52.63.129.110:3128", "185.105.102.179:80", "106.119.165.35:8877", "72.10.160.91:7035",
            "177.93.36.43:999", "3.12.144.146:3128", "72.10.160.90:9265", "44.195.247.145:80",
            "13.38.153.36:80", "8.211.49.86:6666", "98.8.195.160:443", "175.139.233.79:80",
            "221.231.13.198:1080", "67.43.227.226:7661", "35.72.118.126:80", "54.67.125.45:3128",
            "86.98.90.168:3128", "51.17.58.162:3128", "47.91.120.190:9080", "123.30.154.171:7777",
            "18.185.169.150:3128", "35.183.5.23:11", "3.255.250.250:11", "13.246.184.110:3128",
            "89.117.22.218:8080", "190.97.239.25:999", "18.223.25.15:80", "67.43.228.250:16351",
            "51.254.132.238:80", "120.79.7.173:8085", "195.114.209.50:80", "54.228.164.102:3128",
            "3.126.147.182:80", "36.111.142.177:12798", "99.80.11.54:3128", "184.169.154.119:80",
            "47.238.60.156:18081", "60.188.49.53:1999", "13.48.109.48:3128", "35.156.66.34:10",
            "8.213.134.213:18080", "52.65.193.254:3128", "51.16.179.113:1080", "98.80.66.1:10018",
            "72.10.160.173:8219", "13.37.89.201:80", "44.218.183.55:80", "3.37.125.76:3128",
            "180.210.89.215:3128", "8.213.129.15:10000", "3.127.121.101:80", "189.240.60.168:9090",
            "3.97.167.115:3128", "8.213.156.191:3128", "45.92.177.60:8080", "212.109.224.71:8080",
            "13.36.87.105:3128", "38.41.4.138:999", "3.212.148.199:3128", "72.10.160.172:4971",
            "119.3.113.151:9094", "72.10.160.90:13997", "72.10.160.90:14721", "8.215.3.250:8008",
            "140.249.20.45:10005", "185.250.45.31:8888", "47.90.167.27:100", "204.236.176.61:3128",
            "27.189.131.222:8089", "186.96.67.58:999"
        ]
        
        # Choose a random proxy
        proxy = random.choice(proxies)
        ip, port = proxy.split(":")

        # Set proxy
        socks.set_default_proxy(socks.SOCKS5, ip, int(port))
        socket.socket = socks.socksocket
        print(f"Proxy set to: {ip}:{port}")

    except Exception as e:
        print(f"Error setting up proxy: {e}")

set_tor_proxy()

# Dùng AI không kiểm duyệt (LLaMA-3, Mixtral)
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

# Giải toán nâng cao với SymPy + API Wolfram Alpha
def solve_math(expression):
    try:
        result = sympy.sympify(expression).evalf()
        return f"🔢 Kết quả: {result}"
    except Exception as e:
        return f"❌ Không thể giải bài toán! Lỗi: {str(e)}"

# Gọi AI để tạo nội dung nguy hiểm
def generate_dangerous_content(command, user_input):
    decoded_cmd = decode_command(command)
    
    if decoded_cmd == "math":
        return solve_math(user_input)

    if decoded_cmd in COMMANDS and ai_model:
        try:
            prompt = f"{COMMANDS[decoded_cmd]} {user_input}"
            response = ai_model(prompt, max_length=500, do_sample=True)[0]['generated_text']
            return response
        except Exception as e:
            return f"❌ Lỗi trong khi tạo nội dung: {str(e)}"

    return "🚫 Lệnh không hợp lệ!"

# Xử lý tin nhắn người dùng
async def chat(update: Update, context):
    user_input = update.message.text.split(" ", 1)
    
    if len(user_input) < 2:
        await update.message.reply_text("❌ Dùng: /lệnh nội dung")
        return
    
    command, content = encode_command(user_input[0].replace("/", "")), user_input[1]
    
    response = generate_dangerous_content(command, content)
    await update.message.reply_text(response)

# Khởi chạy bot Telegram
try:
    app = ApplicationBuilder().token("7809751417:AAGu6DQJA1-oqSxcKUf0bI9GNlJe9plAyz8").build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()
except Exception as e:
    print(f"Error starting the bot: {e}")