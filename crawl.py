from selenium import webdriver
import json
import os
import django
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep
from tools.crawl import Crawl
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebPython.settings')
django.setup()

from home.models import Page

chrome_options = Options()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox") 
# chrome_options.add_argument("--disable-dev-shm-usage")

service = Service('chromedriver.exe') 
browser = webdriver.Chrome(service=service,options=chrome_options)

browser.get("https://facebook.com")

# Đọc cookie từ file
with open('cookie.json','r') as file:
    cookies = json.load(file)

# Thêm từng cookie vào trình duyệt
for cookie in cookies:
    browser.add_cookie(cookie)

sleep(2)
browser.get('https://facebook.com')

def crawlPage():
    pages = Page.objects.all().filter(type_page=1).order_by('updated_at')[:100]
    for page in pages:
        link = page.link
        browser.get(link)
        crawl = Crawl(browser,page)
        crawl.get()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        page.updated_at = current_time
        page.save()
        sleep(1)
    crawlPage()
    
try:
    crawlPage()
except Exception as e:
    with open('error.log','a', encoding='utf-8') as file:
        file.write(f'Lỗi khi lấy {e}!')

browser.close() # Đóng
