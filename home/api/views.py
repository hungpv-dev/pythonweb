from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Post
from django.http import JsonResponse
from .serializers import PostSerializer
import math
import subprocess

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=False, methods=['post'])
    def crawl(self, request):
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

    @action(detail=False, methods=['get'])
    def all(self, request):
        limit = 10
        page = int(request.GET.get('page', 1))
        offset = (page - 1) * limit
        counts = Post.objects.count()
        to = offset + limit
        to = min(to, counts)
        posts = Post.objects.all().order_by('-id').values()[offset:to]
        return JsonResponse({
            'limit': limit,
            'from': offset + 1,
            'to': to,
            'total': counts,
            'totalPages': math.ceil(counts / limit),
            'currentPage': page,
            'url': request.build_absolute_uri().split('?')[0],
            'currentUrl': request.build_absolute_uri(),
            'params': '?' + request.META['QUERY_STRING'],
            'all': bool(request.GET.get('show_all')),
            'data': list(posts),
        }, safe=False)