from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.files.storage import default_storage
from ...models import Post
import uuid
from django.http import JsonResponse
from ..serializers import PostSerializer
import psutil
import os
import json
from ...utils import is_process_running, paginate
import subprocess
from django.conf import settings

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
        if 'page_id' in request.GET:
            model = model.filter(page_id=request.GET.get('page_id'))
            
        if 'up' in request.GET:
            up_value = request.GET.get('up') 
            if up_value in ['true', '1', True]:
                up_value = True
            else:
                up_value = False 
            model = model.filter(up=up_value)
            
        return Response(paginate(request, model))
    
    @action(detail=True, methods=['get'])
    def show(self, request, pk=None):
        try:
            print("Show method called")
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Bài viết không tồn tại.'}, status=404)
        
    @action(detail=False, methods=['post'])
    def edit(self, request):
        try:
            id = request.data.get('post_id_web')
            post = Post.objects.get(id=id)
            hrefs = json.loads(request.data.get('hrefs', '[]'))
            files = request.FILES.getlist('media')
            
            images = []
            for img in hrefs:
                images.append(img)
            
            if files:
                for file in files:
                    fake_name = f"{uuid.uuid4().hex}_{file.name}"
                    save_path = os.path.join('uploads', 'media', fake_name)
                    file_name = default_storage.save(save_path, file)
                    full_url = request.build_absolute_uri(f"/media/{fake_name}")
                    images.append(full_url)
            else:
                print("No files were uploaded.")
                
            return Response({'images': images}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Bài viết không tồn tại.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Có lỗi xảy ra khi lưu tệp.'}, status=500)
        
        