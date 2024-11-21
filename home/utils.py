import psutil
from django.http import JsonResponse
import math

def is_process_running(process_name):
    for proc in psutil.process_iter(['cmdline']):
        cmdline = proc.info['cmdline']
        if cmdline is not None and process_name in cmdline:
            return True
    return False

def paginate(request,model):
    limit = int(request.GET.get('limit',10))
    page = int(request.GET.get('page', 1))
    offset = (page - 1) * limit
    counts = model.count()
    to = offset + limit
    to = min(to, counts)
    data = list(model.all().values()[offset:to])
    return {
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
        'data': data,
    }

def compact(*args):
    return {item: globals().get(item) for item in args}