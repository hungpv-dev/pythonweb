from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from ...models import Page, User
from django.http import JsonResponse
from ..serializers import PageSerializer
from ...utils import is_process_running, paginate

class PaegViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    @action(detail=False, methods=['get'])
    def all(self, request):
        find = None
        model = self.queryset.order_by('-id')
        if 'page_id' in request.GET:
            find = self.queryset.filter(id=request.GET.get('page_id')).first()
            
        if 'type_page' in request.GET:
            model = model.filter(type_page=request.GET.get('type_page'))
            
        if 'name' in request.GET:
            search_value = request.GET.get('name')
            model = model.filter(link__icontains=search_value) | model.filter(type__icontains=search_value)
        
        if 'user_id' in request.GET:
            model = model.exclude(user_id=request.GET.get('user_id'))
            
        response = paginate(request, model)
        if find:
            response['data'].insert(0, self.serializer_class(find).data)
        
        for item in response['data']:
            user = User.objects.filter(id=item['user_id']).first()
            if user:
                item['user'] = {
                    'id': user.id,
                    'username': user.name,
                    'link': user.link,
                    'code': user.code,
                }
            else:
                item['user'] = None
        
        return JsonResponse(response, safe=True)
    
    @action(detail=True, methods=['get'])
    def show(self, request, pk=None):
        try:
            post = Page.objects.get(pk=pk)
            serializer = PageSerializer(post)
            return Response(serializer.data)
        except Page.DoesNotExist:
            return JsonResponse({'error': 'Bài viết không tồn tại.'}, status=404)
        
    @action(detail=False, methods=['post'])
    def add(self, request):
        link = request.data.get('link')
        if Page.objects.filter(link=link).exists():
            return Response({'link': ['Đường dẫn đã tồn tại.']}, status=422)
        
        serializer = PageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Thêm page mới thành công!',
                'data': serializer.data
            }, status=201)
        return Response(serializer.errors, status=400)
    
    @action(detail=False, methods=['put'])
    def edit(self, request):
        page_id = request.data.get('id')
        page = Page.objects.filter(id=page_id).first()
        if not page:
            return JsonResponse({'error': 'Bài viết không tồn tại.'}, status=404)
        
        link = request.data.get('link')
        if Page.objects.filter(link=link).exclude(id=page_id).exists():
            return Response({'link': ['Đường dẫn đã tồn tại.']}, status=422)
        
        serializer = PageSerializer(page, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Cập nhật page thành công!',
                'data': serializer.data
            }, status=200)
        return Response(serializer.errors, status=400)
