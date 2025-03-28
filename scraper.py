import re
import requests
import os
import asyncio
from telegram import Bot

# Telegram 配置
BOT_TOKEN = "7799347711:AAEQDRavpSXKSNiaPMLBrVvSobnmwuMCL_Q"
CHAT_ID = "-4740029830"  # Nezzotizia 群组 ID

bot = Bot(token=BOT_TOKEN)
file_path = "ricevimento.txt"
url = "https://www.beniculturali.unipd.it/www/dipartimento/personale/personale-%20docente/profilo-docente/?IdDocDid=12695"

async def send_telegram_message(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
        print("📨 Telegram 通知已发送")
    except Exception as e:
        print("❌ Telegram 发送失败:", e)

def extract_ricevimento_text(html):
    match = re.search(r'id="hideslide0p2317".*?</div>', html, re.DOTALL)
    if not match:
        return ""
    block = match.group(0)
    lines = re.findall(r"<p.*?>(.*?)</p>", block, re.DOTALL)
    return "\n".join(
        re.sub(r"<.*?>", "", line).strip()
        for line in lines if re.sub(r"<.*?>", "", line).strip()
    )

def read_old_content():
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def write_new_content(content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

# 主流程
old_content = read_old_content()
print("📄 本地内容：")
print(old_content if old_content else "[空]")

html = requests.get(url).text
new_content = extract_ricevimento_text(html)
print("\n🌐 网络内容：")
print(new_content if new_content else "[未提取到内容]")

if new_content and new_content != old_content:
    write_new_content(new_content)
    print("\n✅ ricevimento.txt 内容已更新")
    asyncio.run(send_telegram_message(f"📢 [教授会面时间更新提醒]\n\n{new_content}"))
elif new_content == old_content:
    print("\n🔁 内容未变化，无需更新")
else:
    print("\n⚠️ 未能成功提取内容或内容为空")

