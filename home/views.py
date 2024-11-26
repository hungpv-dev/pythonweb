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
    return render(request, 'pages/posts/index.html')

def page(request):
    return render(request, 'pages/fanpages/index.html')

def data(request):
    return render(request, 'pages/data.html')

def list_accounts(request):
    return render(request, 'pages/users/list_accounts.html')
