from django.shortcuts import render
from .utils import is_process_running
from .models import Post
from .utils import compact

from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

def index(request):
    process_running = False
    if is_process_running('crawl.py'):
        process_running = True
    return render(request, 'pages/home.html', {
        'process_running': process_running
    })

def post(request):
    return render(request, 'pages/posts/index.html',compact('up','crawl'))

def list_accounts(request):
    return render(request, 'pages/users/list_accounts.html')

def start_virtual_browser(request):
    try:
        # Path to your ChromeDriver
        chrome_driver_path = os.path.join(os.path.dirname(__file__), '../../chromedriver.exe')

        # Setup Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Optional: Run in headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Start the browser
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
        driver.get('https://www.facebook.com/login')

        # Perform login actions here if needed

        return JsonResponse({'status': 'success', 'message': 'Virtual browser started'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
