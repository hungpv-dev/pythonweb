from django.shortcuts import render
from django.http import JsonResponse
from .models import Post
import math
import json

def index(request):
    return render(request, 'pages/home.html')

def post(request):
    return render(request, 'pages/posts/index.html')

def api_posts(request):
    if request.method == 'GET':
        # Logic để lấy danh sách bài viết
        pass
    elif request.method == 'POST':
        # Logic để tạo bài viết mới
        pass
    
# from django.shortcuts import render
# from django.http import JsonResponse
# import subprocess
# import psutil
# from .models import Post
# import math
# import json

# # Biến toàn cục để lưu trữ tiến trình
# current_process = None

# def index(request):
#     process_running = False
#     if is_process_running('crawl.py'):
#         process_running = True
#     return render(request, 'pages/home.html', {
#         'process_running': process_running
#     })

# def post(request):
#     return render(request, 'pages/posts/index.html')



# def run_crawl(request):
#     global current_process
#     is_running = False
#     if current_process and current_process.poll() is None: 
#         current_process.terminate()
#         current_process = None
#         return JsonResponse({"message": "Tiến trình đã dừng.","is_running": is_running})
#     try:
#         current_process = subprocess.Popen(['python', 'crawl.py']) 
#         is_running = True
#         return JsonResponse({"message": "Crawl đã được thực hiện thành công!","is_running": is_running})
#     except Exception as e:
#         return JsonResponse({"message": "Có lỗi xảy ra khi chạy crawl.","is_running": is_running, "error": str(e)}, status=500)

# def is_process_running(process_name):
#     for proc in psutil.process_iter(['cmdline']):
#         cmdline = proc.info['cmdline']
#         if cmdline is not None and process_name in cmdline:
#             return True
#     return False

# def api_posts(request):
#     if request.method == 'GET':
#         limit = 10
#         page = int(request.GET.get('page', 1))
#         offset = (page - 1) * limit
#         counts = Post.objects.count()
#         to = offset + limit
#         to = min(to, counts)
#         posts = Post.objects.all().order_by('-id').values()[offset:to]
#         return JsonResponse({
#             'limit': limit,
#             'from': offset + 1,
#             'to': to,
#             'total': counts,
#             'totalPages': math.ceil(counts / limit),
#             'currentPage': page,
#             'url': request.build_absolute_uri().split('?')[0],
#             'currentUrl': request.build_absolute_uri(),
#             'params': '?' + request.META['QUERY_STRING'],
#             'all': bool(request.GET.get('show_all')),
#             'data': list(posts),
#         }, safe=False)
#     elif request.method == 'POST':
#         data = json.loads(request.body)
#         post = Post.objects.create(**data)
#         return JsonResponse({'id': post.id}, status=201)
    
# def api_post_detail(request, id):
#     try:
#         post = Post.objects.get(id=id)
#         post_data = {
#             field.name: getattr(post, field.name) for field in Post._meta.fields
#         }
#         return JsonResponse(post_data, safe=False)
#     except Post.DoesNotExist:
#         return JsonResponse({'error': 'Bài viết không tồn tại.'}, status=404)