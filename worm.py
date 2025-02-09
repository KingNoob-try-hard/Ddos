from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext
from telegram import Update
from transformers import pipeline  
import requests  

# Sử dụng mô hình AI 
ai_model = pipeline("text-generation", model="EleutherAI/gpt2-medium")  

# Danh sách người dùng được phép sử dụng bot  
ALLOWED_USERS = {6031289574}  

def generate_response(user_input):  
    response = ai_model(user_input, max_length=900, do_sample=True)[0]['generated_text']  
    return response  

async def chat(update: Update, context: CallbackContext):  
    user_id = update.message.from_user.id  
    if user_id not in ALLOWED_USERS:  
        return  # Không phản hồi nếu không có quyền  

    user_input = update.message.text  
    response = generate_response(user_input)  
    await update.message.reply_text(response)  

def evade_detection(text):  
    blocked_words = []  
    for word in blocked_words:  
        text = text.replace(word, word[0] + "*" * (len(word) - 1))  
    return text  

# Danh sách proxy
proxies_list = [
    "http://67.43.228.250:8277",
    "http://218.31.88.90:11889",
    "http://52.73.224.54:3128",
    "http://51.20.19.159:3128",
    "http://13.36.104.85:80",
    "http://41.59.90.171:80",
    "http://8.211.49.86:10000",
    "http://162.223.90.130:80",
    "http://202.63.172.18:9128",
    "http://103.124.137.150:20",
    "http://47.91.29.151:9080",
    "http://18.228.149.161:80",
    "http://52.16.232.164:3128",
    "http://80.249.112.162:80",
    "http://44.219.175.186:80",
    "http://58.243.224.244:8085",
    "http://15.156.24.206:3128",
    "http://54.179.39.14:3128",
    "http://3.97.176.251:3128",
    "http://184.73.68.87:11",
    "http://51.16.199.206:3128",
    "http://106.38.26.22:2080",
    "http://218.13.39.150:9091",
    "http://103.49.202.252:80",
    "http://180.184.79.187:12798",
    "http://177.93.49.203:999",
    "http://119.3.113.152:9094",
    "http://13.37.59.99:3128",
    "http://139.215.92.20:10005",
    "http://13.56.192.187:80",
    "http://111.34.79.216:10219",
    "http://13.246.209.48:1080",
    "http://54.152.3.36:80",
    "http://8.215.3.250:90",
    "http://183.215.23.242:9091",
    "http://58.23.152.29:7080",
    "http://218.1.197.106:2324",
    "http://38.54.116.9:4000",
    "http://51.20.50.149:3128",
    "http://185.105.102.189:80",
    "http://13.208.56.180:80",
    "http://8.208.85.34:6969",
    "http://67.43.228.253:13087",
    "http://43.200.77.128:3128",
    "http://27.189.130.203:8089",
    "http://135.181.154.225:80",
    "http://194.190.70.200:3128",
    "http://204.236.137.68:80",
    "http://87.248.129.32:80",
    "http://67.43.228.250:29003",
    "http://67.43.236.21:14883",
    "http://183.234.215.11:8443",
    "http://47.123.4.107:9100",
    "http://72.10.160.174:1971",
    "http://8.211.49.86:8443"
]

def check_proxy(proxy):
    proxies = {"http": proxy, "https": proxy}
    try:
        response = requests.get("http://checkip.amazonaws.com/", proxies=proxies, timeout=5)
        if response.status_code == 200:
            return f"✅ Proxy {proxy} hoạt động - IP: {response.text.strip()}"
    except requests.RequestException:
        return f"❌ Proxy {proxy} không hoạt động"
    return f"❌ Proxy {proxy} không phản hồi"

# Kiểm tra từng proxy
for proxy in proxies_list:
    print(check_proxy(proxy)) 

# Khởi tạo bot Telegram  
app = ApplicationBuilder().token("7809751417:AAGu6DQJA1-oqSxcKUf0bI9GNlJe9plAyz8").build()  
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))  

print("🤖 Bot Telegram đang chạy...")  
app.run_polling()