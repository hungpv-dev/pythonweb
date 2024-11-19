from django.shortcuts import render
from django.http import JsonResponse
import subprocess
import psutil
from .models import Post
import json

# Biến toàn cục để lưu trữ tiến trình
current_process = None

def index(request):
    process_running = False
    if is_process_running('crawl.py'):
        process_running = True
    return render(request, 'pages/home.html', {
        'process_running': process_running
    })

def post(request):
    return render(request, 'pages/posts.html')

def run_crawl(request):
    global current_process
    is_running = False
    if current_process and current_process.poll() is None: 
        current_process.terminate()
        current_process = None
        return JsonResponse({"message": "Tiến trình đã dừng.","is_running": is_running})
    try:
        current_process = subprocess.Popen(['python', 'crawl.py']) 
        is_running = True
        return JsonResponse({"message": "Crawl đã được thực hiện thành công!","is_running": is_running})
    except Exception as e:
        return JsonResponse({"message": "Có lỗi xảy ra khi chạy crawl.","is_running": is_running, "error": str(e)}, status=500)

def is_process_running(process_name):
    for proc in psutil.process_iter(['cmdline']):
        cmdline = proc.info['cmdline']
        if cmdline is not None and process_name in cmdline:
            return True
    return False

def api_posts(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        start = (page - 1) * per_page
        end = start + per_page
        total_posts = Post.objects.count()
        posts = Post.objects.all().values()[start:end]
        return JsonResponse({
            'total': total_posts,
            'page': page,
            'per_page': per_page,
            'posts': list(posts)
        }, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        post = Post.objects.create(**data)
        return JsonResponse({'id': post.id}, status=201)