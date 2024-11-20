from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ...models import Post
from django.http import JsonResponse
from ..serializers import PostSerializer
import math
import psutil
from ...utils import is_process_running, paginate
import subprocess

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=False, methods=['post'])
    def crawl(self, request):
        is_running = False
        if is_process_running('crawl.py'):
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                if "python" in proc.info['name'] and "crawl.py" in proc.info['cmdline']:
                    proc.kill()
            return JsonResponse({"message": "Tiến trình đã dừng.", "is_running": is_running})
        else:
            try:
                subprocess.Popen(['python', 'crawl.py'])
                is_running = True
                return JsonResponse({"message": "Crawl đã được thực hiện thành công!", "is_running": is_running})
            except Exception as e:
                return JsonResponse({"message": "Có lỗi xảy ra khi chạy crawl.", "is_running": is_running, "error": str(e)}, status=500)

    @action(detail=False, methods=['get'])
    
    def all(self, request):
        model = Post.objects.order_by('-id')
        return paginate(request, model)
    
    @action(detail=True, methods=['get'])
    def show(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Bài viết không tồn tại.'}, status=404)
        
        