from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ...models import User
from django.http import JsonResponse
from ..serializers import UserSerializer
from ...utils import paginate
import math

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def all(self, request):
        limit = 10
        page = int(request.GET.get('page', 1))
        offset = (page - 1) * limit
        counts = User.objects.count()
        to = offset + limit
        to = min(to, counts)
        users = User.objects.all().order_by('-id')
        return paginate(request, users)

    @action(detail=False, methods=['get'])
    def api_list_accounts(self, request):
        limit = 10
        page = int(request.GET.get('page', 1))
        offset = (page - 1) * limit
        counts = User.objects.count()
        to = offset + limit
        to = min(to, counts)
        accounts = User.objects.all().order_by('-id')[offset:to]
        account_data = list(accounts.values('id', 'name', 'link', 'cookie'))
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
            'data': account_data,
        }, safe=False)

    @action(detail=False, methods=['post'])
    def add_accounts(self, request):
        accounts_data = request.data.get('accounts', [])
        created_accounts = []
        for account_data in accounts_data:
            serializer = UserSerializer(data=account_data)
            if serializer.is_valid():
                serializer.save()
                created_accounts.append(serializer.data)
            else:
                return JsonResponse({'error': 'Dữ liệu không hợp lệ', 'details': serializer.errors}, status=400)
        return JsonResponse({'message': 'Thêm tài khoản thành công', 'data': created_accounts}, status=201, safe=False)
