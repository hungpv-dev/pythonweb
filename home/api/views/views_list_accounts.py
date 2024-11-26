from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ...models import User
from django.http import JsonResponse
from ..serializers import UserSerializer
from ...utils import paginate
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def all(self, request):
        """
        Endpoint trả về tất cả các user với phân trang
        """
        users = User.objects.all()
        type = request.GET.get('type')
        name = request.GET.get('name')
        if type is not None and type != '':
            users = users.filter(type=type)
        if name is not None and name != '':
            users = users.filter(name__icontains=name) | users.filter(link__icontains=name)

        # Trả dữ liệu phân trang
        return JsonResponse(paginate(request, users), safe=False)

    @action(detail=False, methods=['get'])
    def api_list_accounts(self, request):
        """
        Endpoint trả về danh sách tài khoản với thông tin chi tiết và phân trang
        """
        limit = 10
        page = int(request.GET.get('page', 1))
        offset = (page - 1) * limit
        counts = User.objects.count()
        accounts = User.objects.all().order_by('-id')[offset:offset + limit]

        account_data = list(accounts.values('id','code', 'name', 'type', 'link', 'cookie'))
        total_pages = math.ceil(counts / limit)
        all_accounts_returned = (offset + limit >= counts)

        # Trả kết quả
        return Response({
            'limit': limit,
            'from': offset + 1,
            'to': min(offset + limit, counts),
            'total': counts,
            'totalPages': total_pages,
            'currentPage': page,
            'url': request.build_absolute_uri().split('?')[0],
            'currentUrl': request.build_absolute_uri(),
            'params': '?' + request.META['QUERY_STRING'],
            'all': all_accounts_returned,
            'data': account_data,
        })

    # @method_decorator(csrf_exempt)
    # @action(detail=False, methods=['post'])
    # def add_accounts(self, request):
    #     """
    #     Endpoint để thêm tài khoản
    #     """
    #     accounts_data = request.data.get('accounts', [])
    #     if not accounts_data:
    #         return JsonResponse({'error': 'Danh sách tài khoản rỗng'}, status=400)

    #     created_accounts = []
    #     for account_data in accounts_data:
    #         # Hiển thị giao diện đăng nhập Facebook
    #         fb_name, fb_link, fb_cookie = self.show_facebook_login_interface(account_data)
            
    #         if not fb_name or not fb_link or not fb_cookie:
    #             return JsonResponse({'error': 'Không thể lấy thông tin từ Facebook'}, status=400)

    #         # Gắn thông tin trả về
            
    #         account_data['name'] = fb_name
    #         account_data['link'] = fb_link
    #         account_data['cookie'] = fb_cookie

    #         # Serialize và lưu
    #         serializer = UserSerializer(data=account_data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             created_accounts.append(serializer.data)
    #         else:
    #             return JsonResponse({'error': 'Dữ liệu không hợp lệ', 'details': serializer.errors}, status=400)

    #     # Trả kết quả
    #     return JsonResponse({'message': 'Thêm tài khoản thành công', 'data': created_accounts}, status=201, safe=False)

    # def show_facebook_login_interface(self, account_data):
    #     """
    #     Hiển thị giao diện đăng nhập Facebook và lấy thông tin tài khoản.
    #     """
    #     # Initialize the Selenium WebDriver
    #     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    #     try:
    #         # Open Facebook login page directly
    #         driver.get("https://www.facebook.com/login")

    #         # Find and fill the email and password fields
    #         email_field = driver.find_element(By.ID, "email")
    #         password_field = driver.find_element(By.ID, "pass")
    #         email_field.send_keys(account_data.get('email'))
    #         password_field.send_keys(account_data.get('password'))
    #         password_field.send_keys(Keys.RETURN)

    #         # Wait for login to complete
    #         time.sleep(5)  # Adjust the sleep time as necessary

    #         # Navigate to the user's profile page
    #         driver.get("https://www.facebook.com/me")

    #         # Wait for the profile page to load
    #         time.sleep(5)  # Adjust the sleep time as necessary

    #         # Retrieve the user's name from the profile page
    #         fb_name = driver.find_element(By.CSS_SELECTOR, "h1").text  # Adjust the selector as needed
    #         fb_link = driver.current_url

    #         # Retrieve cookies
    #         cookies = driver.get_cookies()
    #         fb_cookie = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

    #         return fb_name, fb_link, fb_cookie

    #     except Exception as e:
    #         print(f"Lỗi trong quá trình đăng nhập Facebook: {e}")
    #         return None, None, None

    #     finally:
    #         driver.quit()

    @action(detail=True, methods=['put'])
    def update_account(self, request, pk=None):
        """
        Endpoint để cập nhật thông tin tài khoản
        """
        try:
            account = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Tài khoản không tồn tại'}, status=404)

        serializer = UserSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Cập nhật tài khoản thành công', 'data': serializer.data}, status=200)
        else:
            return JsonResponse({'error': 'Dữ liệu không hợp lệ', 'details': serializer.errors}, status=400)

    # @method_decorator(csrf_exempt)
    # @action(detail=False, methods=['post'])
    # def add_facebook_account(self, request):
    #     """
    #     Endpoint to add a Facebook account by redirecting to Facebook login and retrieving details.
    #     """
    #     email = request.data.get('email')
    #     password = request.data.get('password')

    #     if not email or not password:
    #         return JsonResponse({'error': 'Email và mật khẩu không được để trống'}, status=400)

    #     # Redirect to Facebook login page
    #     fb_name, fb_link, fb_cookie = self.show_facebook_login_interface({'email': email, 'password': password})

    #     if not fb_name or not fb_link or not fb_cookie:
    #         return JsonResponse({'error': 'Không thể lấy thông tin từ Facebook'}, status=400)

    #     # Create a new user with the retrieved data
    #     user_data = {
    #         'code': fb_link.split('/')[-1],  # Assuming the ID is the last part of the URL
    #         'name': fb_name,
    #         'type': 1,  # Assuming a default type
    #         'link': fb_link,
    #         'cookie': fb_cookie
    #     }

    #     serializer = UserSerializer(data=user_data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse({'success': True, 'data': serializer.data}, status=201)
    #     else:
    #         return JsonResponse({'error': 'Dữ liệu không hợp lệ', 'details': serializer.errors}, status=400)
