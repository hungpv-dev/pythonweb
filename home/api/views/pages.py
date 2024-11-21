from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from ...models import Page
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
            model = model.filter(link__icontains=request.GET.get('name'))
            
        response = paginate(request, model)
        if find:
            response['data'].insert(0, self.serializer_class(find).data)
        return JsonResponse(response, safe=True)
    
    @action(detail=True, methods=['get'])
    def show(self, request, pk=None):
        try:
            post = Page.objects.get(pk=pk)
            serializer = PageSerializer(post)
            return Response(serializer.data)
        except Page.DoesNotExist:
            return JsonResponse({'error': 'Bài viết không tồn tại.'}, status=404)
        
        