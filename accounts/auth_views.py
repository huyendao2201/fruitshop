"""
Views xác thực tùy chỉnh với chuyển hướng dựa trên vai trò
"""
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import reverse


class CustomLoginView(auth_views.LoginView):
    """
    View đăng nhập tùy chỉnh, chuyển hướng dựa trên vai trò người dùng
    """
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        """
        Chuyển hướng dựa trên vai trò/nhóm người dùng:
        - Superuser/Admin -> Báo cáo dashboard
        - Staff -> Bảng điều khiển giao hàng
        - Shipper (trong nhóm Shipper) -> Đơn hàng của tôi
        - Người dùng thường -> Trang chủ
        """
        user = self.request.user
        
        # Kiểm tra nếu là superuser/admin
        if user.is_superuser:
            return reverse('reports:dashboard')
        
        # Kiểm tra nếu là staff (nhưng không phải shipper)
        if user.is_staff and not user.groups.filter(name='Shipper').exists():
            return reverse('delivery:dashboard')
        
        # Kiểm tra nếu là shipper
        if user.groups.filter(name='Shipper').exists():
            return reverse('delivery:my_deliveries')
        
        # Khách hàng thông thường
        return reverse('home')


class CustomLogoutView(auth_views.LogoutView):
    """
    View đăng xuất tùy chỉnh
    """
    next_page = 'home'




