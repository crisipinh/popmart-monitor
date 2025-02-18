import requests
from bs4 import BeautifulSoup
import smtplib
import time
import os
from email.message import EmailMessage
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 配置邮箱和密码
EMAIL_USER = "Crisipinh888@gmail.com"  # 替换为你的Gmail地址
EMAIL_PASSWORD = "ahjd mqyn vkba uahb"  # 替换为生成的应用专用密码
TARGET_URL = "https://au.popmart.com/products/pop-mart-the-monsters-zimomo-i-found-you-vinyl-plush-doll?srsltid=AfmBOoojPaxaE419PCpQ5GinxnXNFOCJWVZaIeu8h4JKwewQeAJBzid4"
CHECK_INTERVAL = 120  # 120秒 = 2分钟
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

def check_stock():
    headers = {'User-Agent': USER_AGENT}
    try:
        response = requests.get(TARGET_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找库存状态（需要根据实际页面结构调整选择器）
        add_to_cart_button = soup.find('button', {'name': 'add'})
        if add_to_cart_button and 'disabled' not in add_to_cart_button.attrs:
            return True
        return False
    except Exception as e:
        logging.error(f"检查库存时出错: {str(e)}")
        return False

def send_notification():
    msg = EmailMessage()
    msg['Subject'] = "POP MART ZIMOMO 补货通知！"
    msg['From'] = EMAIL_USER
    msg['To'] = ['crisipinh888@gmail.com', 'dannie9966ll@gmail.com']
    msg.set_content(f"立即购买：{TARGET_URL}")

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        logging.info("通知邮件已发送")
    except Exception as e:
        logging.error(f"发送邮件失败: {str(e)}")

def main():
    logging.info("启动库存监控...")
    while True:
        try:
            if check_stock():
                logging.info("检测到补货！")
                send_notification()
                # 发送成功后暂停1小时避免重复通知
                time.sleep(3600)
            else:
                logging.info("当前无库存")
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            logging.info("监控已停止")
            break
        except Exception as e:
            logging.error(f"运行异常: {str(e)}")
            time.sleep(60)

if __name__ == "__main__":
    main()