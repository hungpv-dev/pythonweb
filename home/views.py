from django.shortcuts import render
from .utils import is_process_running

def index(request):
    process_running = False
    if is_process_running('crawl.py'):
        process_running = True
    return render(request, 'pages/home.html', {
        'process_running': process_running
    })

def post(request):
    return render(request, 'pages/posts/index.html')
