from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Avg, F, Q, Max, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth, TruncDate
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import models
from datetime import datetime, timedelta
from decimal import Decimal
from orders.models import Order, OrderItem
from products.models import Product, Review, Category, ProductImage, Discount, ShopReview
from accounts.models import User
from delivery.models import Delivery, DeliveryPerson, DeliveryTracking


class AdminRequiredMixin(LoginRequiredMixin):
    """Mixin để yêu cầu user phải là admin"""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        return super().dispatch(request, *args, **kwargs)

"""tongquan"""
class DashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'admin_dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get date ranges
        today = timezone.now().date()
        this_month = today.replace(day=1)
        last_month = (this_month - timedelta(days=1)).replace(day=1)
        this_year = today.replace(month=1, day=1)
        
        # ============ STATISTICS CARDS ============
        
        # Total Revenue (all completed orders)
        total_revenue = Order.objects.filter(
            payment_status='paid'
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
        
        # Monthly Revenue
        monthly_revenue = Order.objects.filter(
            created_at__gte=this_month,
            payment_status='paid'
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
        
        # Calculate monthly growth
        last_month_revenue = Order.objects.filter(
            created_at__gte=last_month,
            created_at__lt=this_month,
            payment_status='paid'
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
        
        if last_month_revenue > 0:
            monthly_growth = ((monthly_revenue - last_month_revenue) / last_month_revenue) * 100
        else:
            monthly_growth = 100 if monthly_revenue > 0 else 0
        
        # Total Orders
        total_orders = Order.objects.count()
        monthly_orders = Order.objects.filter(created_at__gte=this_month).count()
        
        # Pending Orders (need attention)
        pending_orders = Order.objects.filter(
            status__in=['pending', 'confirmed']
        ).count()
        
        # Total Customers
        total_customers = User.objects.filter(role='customer').count()
        new_customers_this_month = User.objects.filter(
            role='customer',
            date_joined__gte=this_month
        ).count()
        
        # Total Products
        total_products = Product.objects.count()
        active_products = Product.objects.filter(is_active=True).count()
        
        context.update({
            'total_revenue': total_revenue,
            'monthly_revenue': monthly_revenue,
            'monthly_growth': round(monthly_growth, 1),
            'total_orders': total_orders,
            'monthly_orders': monthly_orders,
            'pending_orders': pending_orders,
            'total_customers': total_customers,
            'new_customers': new_customers_this_month,
            'total_products': total_products,
            'active_products': active_products,
        })
        
        # ============ ORDER STATUS DISTRIBUTION ============
        order_status_stats = Order.objects.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        status_labels = []
        status_data = []
        status_colors = {
            'pending': '#ffc107',
            'confirmed': '#17a2b8',
            'processing': '#007bff',
            'shipped': '#6f42c1',
            'delivered': '#20c997',
            'completed': '#28a745',
            'canceled': '#dc3545',
        }
        
        for stat in order_status_stats:
            status_labels.append(dict(Order.STATUS_CHOICES).get(stat['status'], stat['status']))
            status_data.append(stat['count'])
        
        context.update({
            'order_status_labels': status_labels,
            'order_status_data': status_data,
            'order_status_colors': [status_colors.get(s['status'], '#6c757d') for s in order_status_stats],
        })
        
        # ============ RECENT ORDERS ============
        context['recent_orders'] = Order.objects.select_related('user').prefetch_related('items__product').order_by('-created_at')[:10]
        
        # ============ RECENT ORDER ITEMS (CHI TIẾT SẢN PHẨM ĐÃ BÁN) ============
        recent_order_items = OrderItem.objects.select_related(
            'order', 'order__user', 'product'
        ).order_by('-order__created_at')[:20]
        context['recent_order_items'] = recent_order_items
        
        # ============ BEST SELLING PRODUCTS ============
        best_selling = Product.objects.annotate(
            total_sold=Sum('orderitem__quantity'),
            total_revenue=Sum(F('orderitem__quantity') * F('orderitem__price'), output_field=DecimalField())
        ).filter(
            total_sold__isnull=False
        ).order_by('-total_sold')[:5]
        
        context['best_selling_products'] = best_selling
        
        # ============ LOW STOCK PRODUCTS ============
        low_stock = Product.objects.filter(
            stock__lte=F('stock') * 0.2,  # 20% or less of stock
            stock__gt=0
        ).order_by('stock')[:5]
        
        context['low_stock_products'] = low_stock
        
        # ============ RECENT REVIEWS ============
        context['recent_reviews'] = Review.objects.select_related(
            'user', 'product'
        ).order_by('-created_at')[:5]
        
        # ============ AVERAGE RATING ============
        avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0
        context['average_rating'] = round(avg_rating, 1)
        
        # ============ SHOP REVIEWS STATISTICS ============
        total_shop_reviews = ShopReview.objects.count()
        context['total_shop_reviews'] = total_shop_reviews
        
        # Recent shop reviews
        context['recent_shop_reviews'] = ShopReview.objects.select_related(
            'user'
        ).order_by('-created_at')[:5]
        
        # Shop average rating
        shop_avg_rating = ShopReview.objects.aggregate(avg=Avg('rating'))['avg'] or 0
        context['shop_average_rating'] = round(shop_avg_rating, 1)
        
        # Approved vs pending count
        approved_shop_reviews = ShopReview.objects.filter(is_approved=True).count()
        pending_shop_reviews = ShopReview.objects.filter(is_approved=False).count()
        context['approved_shop_reviews'] = approved_shop_reviews
        context['pending_shop_reviews'] = pending_shop_reviews
        
        # Featured reviews
        featured_shop_reviews = ShopReview.objects.filter(is_featured=True).count()
        context['featured_shop_reviews'] = featured_shop_reviews
        
        # ============ DELIVERY STATISTICS ============
        
        # Total deliveries
        total_deliveries = Delivery.objects.count()
        context['total_deliveries'] = total_deliveries
        
        # Delivery status breakdown
        delivery_status_counts = {}
        for status, label in Delivery.STATUS_CHOICES:
            count = Delivery.objects.filter(status=status).count()
            delivery_status_counts[status] = {
                'count': count,
                'label': label,
                'percentage': (count / total_deliveries * 100) if total_deliveries > 0 else 0
            }
        context['delivery_status_counts'] = delivery_status_counts
        
        # Pending deliveries (need assignment)
        pending_deliveries = Delivery.objects.filter(status='pending').count()
        context['pending_deliveries'] = pending_deliveries
        
        # Active deliveries (in progress)
        active_deliveries = Delivery.objects.filter(
            status__in=['assigned', 'picked_up', 'in_transit']
        ).count()
        context['active_deliveries'] = active_deliveries
        
        # Today's deliveries
        today_deliveries = Delivery.objects.filter(
            created_at__date=today
        ).count()
        context['today_deliveries'] = today_deliveries
        
        # Completed today
        completed_today = Delivery.objects.filter(
            status='delivered',
            delivered_at__date=today
        ).count()
        context['completed_today'] = completed_today
        
        # Delayed deliveries
        delayed_deliveries = Delivery.objects.filter(
            estimated_delivery_time__lt=timezone.now(),
            status__in=['assigned', 'picked_up', 'in_transit']
        ).count()
        context['delayed_deliveries'] = delayed_deliveries
        
        # ============ DELIVERY PERSON STATISTICS ============
        
        # Total active delivery persons
        active_delivery_persons = DeliveryPerson.objects.filter(is_active=True).count()
        context['active_delivery_persons'] = active_delivery_persons
        
        # Top delivery persons (by successful deliveries)
        top_delivery_persons = DeliveryPerson.objects.filter(
            is_active=True
        ).annotate(
            success_rate_calc=models.Case(
                models.When(total_deliveries=0, then=0),
                default=(F('successful_deliveries') * 100.0 / F('total_deliveries')),
                output_field=models.FloatField()
            )
        ).order_by('-successful_deliveries')[:5]
        context['top_delivery_persons'] = top_delivery_persons
        
        # ============ RECENT DELIVERIES ============
        
        # Recent deliveries (last 20)
        recent_deliveries = Delivery.objects.select_related(
            'order', 
            'order__user',
            'delivery_person',
            'delivery_person__user'
        ).prefetch_related(
            'order__items',
            'order__items__product'
        ).order_by('-created_at')[:20]
        context['recent_deliveries'] = recent_deliveries
        
        # Deliveries needing attention
        deliveries_need_attention = Delivery.objects.select_related(
            'order',
            'order__user',
            'delivery_person'
        ).filter(
            Q(status='pending') |  # Need assignment
            Q(status='failed') |   # Failed deliveries
            Q(estimated_delivery_time__lt=timezone.now(), status__in=['assigned', 'picked_up', 'in_transit'])  # Delayed
        ).order_by('estimated_delivery_time')[:10]
        context['deliveries_need_attention'] = deliveries_need_attention
        
        return context


class RevenueChartAPIView(AdminRequiredMixin, View):
    """API endpoint cho biểu đồ doanh thu 12 tháng"""
    
    def get(self, request):
        # Get last 12 months data
        today = timezone.now().date()
        twelve_months_ago = today - timedelta(days=365)
        
        # Query revenue by month
        monthly_data = Order.objects.filter(
            created_at__gte=twelve_months_ago,
            payment_status='paid'
        ).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            revenue=Sum('total_amount'),
            orders=Count('id')
        ).order_by('month')
        
        # Prepare data for Chart.js
        labels = []
        revenue_data = []
        orders_data = []
        
        for data in monthly_data:
            month_str = data['month'].strftime('%m/%Y')
            labels.append(month_str)
            revenue_data.append(float(data['revenue'] or 0))
            orders_data.append(data['orders'])
        
        return JsonResponse({
            'labels': labels,
            'revenue': revenue_data,
            'orders': orders_data
        })


class DailyRevenueAPIView(AdminRequiredMixin, View):
    """API endpoint cho biểu đồ doanh thu theo ngày (30 ngày gần nhất)"""
    
    def get(self, request):
        # Get last 30 days
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)
        
        daily_data = Order.objects.filter(
            created_at__gte=thirty_days_ago,
            payment_status='paid'
        ).annotate(
            day=TruncDate('created_at')
        ).values('day').annotate(
            revenue=Sum('total_amount'),
            orders=Count('id')
        ).order_by('day')
        
        labels = []
        revenue_data = []
        orders_data = []
        
        for data in daily_data:
            day_str = data['day'].strftime('%d/%m')
            labels.append(day_str)
            revenue_data.append(float(data['revenue'] or 0))
            orders_data.append(data['orders'])
        
        return JsonResponse({
            'labels': labels,
            'revenue': revenue_data,
            'orders': orders_data
        })


class ProductStatsAPIView(AdminRequiredMixin, View):
    """API endpoint cho thống kê sản phẩm"""
    
    def get(self, request):
        # Top 10 best selling products
        top_products = Product.objects.annotate(
            total_sold=Sum('orderitem__quantity'),
            total_revenue=Sum(F('orderitem__quantity') * F('orderitem__price'), output_field=DecimalField())
        ).filter(
            total_sold__isnull=False
        ).order_by('-total_sold')[:10]
        
        labels = []
        sold_data = []
        revenue_data = []
        
        for product in top_products:
            labels.append(product.name[:20])  # Truncate long names
            sold_data.append(product.total_sold or 0)
            revenue_data.append(float(product.total_revenue or 0))
        
        return JsonResponse({
            'labels': labels,
            'sold': sold_data,
            'revenue': revenue_data
        })


class OrderStatusAPIView(AdminRequiredMixin, View):
    """API endpoint cho phân bố trạng thái đơn hàng"""
    
    def get(self, request):
        status_stats = Order.objects.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        labels = []
        data = []
        colors = {
            'pending': '#ffc107',
            'confirmed': '#17a2b8',
            'processing': '#007bff',
            'shipped': '#6f42c1',
            'delivered': '#20c997',
            'completed': '#28a745',
            'canceled': '#dc3545',
        }
        background_colors = []
        
        for stat in status_stats:
            status_display = dict(Order.STATUS_CHOICES).get(stat['status'], stat['status'])
            labels.append(status_display)
            data.append(stat['count'])
            background_colors.append(colors.get(stat['status'], '#6c757d'))
        
        return JsonResponse({
            'labels': labels,
            'data': data,
            'colors': background_colors
        })


class ExportReportView(AdminRequiredMixin, View):
    """Export báo cáo dưới dạng CSV"""
    
    def get(self, request):
        import csv
        from django.http import HttpResponse
        from datetime import datetime
        
        report_type = request.GET.get('type', 'orders')
        
        # Create the HttpResponse object with CSV header
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="report_{report_type}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        # Add BOM for Excel UTF-8 support
        response.write('\ufeff')
        
        writer = csv.writer(response)
        
        if report_type == 'orders':
            # Export orders report
            writer.writerow(['Mã Đơn', 'Khách Hàng', 'Email', 'Ngày Đặt', 'Trạng Thái', 'Thanh Toán', 'Tổng Tiền'])
            
            orders = Order.objects.select_related('user').order_by('-created_at')
            for order in orders:
                writer.writerow([
                    order.order_number,
                    order.user.get_full_name() or order.user.username,
                    order.user.email,
                    order.created_at.strftime('%d/%m/%Y %H:%M'),
                    order.get_status_display(),
                    order.get_payment_status_display(),
                    f"{order.total_amount:,.0f}đ"
                ])
                
        elif report_type == 'products':
            # Export products report
            writer.writerow(['Tên Sản Phẩm', 'Danh Mục', 'Giá', 'Tồn Kho', 'Đã Bán', 'Doanh Thu', 'Trạng Thái'])
            
            products = Product.objects.annotate(
                total_sold=Sum('orderitem__quantity'),
                total_revenue=Sum(F('orderitem__quantity') * F('orderitem__price'), output_field=DecimalField())
            ).select_related('category').order_by('-total_sold')
            
            for product in products:
                writer.writerow([
                    product.name,
                    product.category.name if product.category else 'N/A',
                    f"{product.price:,.0f}đ",
                    product.stock,
                    product.total_sold or 0,
                    f"{product.total_revenue or 0:,.0f}đ",
                    'Hoạt động' if product.is_active else 'Không hoạt động'
                ])
                
        elif report_type == 'customers':
            # Export customers report
            writer.writerow(['Họ Tên', 'Username', 'Email', 'Số Điện Thoại', 'Ngày Đăng Ký', 'Tổng Đơn', 'Tổng Chi Tiêu'])
            
            customers = User.objects.filter(role='customer').annotate(
                total_orders=Count('order'),
                total_spent=Sum('order__total_amount', filter=Q(order__payment_status='paid'))
            ).order_by('-total_spent')
            
            for customer in customers:
                writer.writerow([
                    customer.get_full_name() or 'N/A',
                    customer.username,
                    customer.email,
                    customer.phone or 'N/A',
                    customer.date_joined.strftime('%d/%m/%Y'),
                    customer.total_orders,
                    f"{customer.total_spent or 0:,.0f}đ"
                ])
                
        elif report_type == 'revenue':
            # Export revenue report
            writer.writerow(['Tháng', 'Số Đơn Hàng', 'Doanh Thu', 'Trung Bình/Đơn'])
            
            today = timezone.now().date()
            twelve_months_ago = today - timedelta(days=365)
            
            monthly_data = Order.objects.filter(
                created_at__gte=twelve_months_ago,
                payment_status='paid'
            ).annotate(
                month=TruncMonth('created_at')
            ).values('month').annotate(
                revenue=Sum('total_amount'),
                orders=Count('id'),
                avg_order=Avg('total_amount')
            ).order_by('month')
            
            for data in monthly_data:
                writer.writerow([
                    data['month'].strftime('%m/%Y'),
                    data['orders'],
                    f"{data['revenue']:,.0f}đ",
                    f"{data['avg_order']:,.0f}đ"
                ])
        
        return response


class QuickStatsAPIView(AdminRequiredMixin, View):
    """API endpoint cho quick stats (real-time updates)"""
    
    def get(self, request):
        today = timezone.now().date()
        this_month = today.replace(day=1)
        
        # Today's stats
        today_orders = Order.objects.filter(
            created_at__date=today
        ).count()
        
        today_revenue = Order.objects.filter(
            created_at__date=today,
            payment_status='paid'
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
        
        # Pending orders needing attention
        pending_count = Order.objects.filter(
            status='pending'
        ).count()
        
        # Low stock count
        low_stock_count = Product.objects.filter(
            stock__lte=10,
            stock__gt=0,
            is_active=True
        ).count()
        
        return JsonResponse({
            'today_orders': today_orders,
            'today_revenue': float(today_revenue),
            'pending_orders': pending_count,
            'low_stock_count': low_stock_count,
        })


# ============================================
# PRODUCT MANAGEMENT VIEWS
# ============================================

class ProductListView(AdminRequiredMixin, ListView):
    """Danh sách tất cả sản phẩm"""
    model = Product
    template_name = 'admin_dashboard/products/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Product.objects.select_related('category').prefetch_related('images')
        
        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search)
            )
        
        # Filter by category
        category_id = self.request.GET.get('category', '')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by status
        status = self.request.GET.get('status', '')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        elif status == 'low_stock':
            queryset = queryset.filter(stock__lte=10, stock__gt=0)
        elif status == 'out_of_stock':
            queryset = queryset.filter(stock=0)
        
        # Ordering
        order_by = self.request.GET.get('order_by', '-created_at')
        queryset = queryset.order_by(order_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search'] = self.request.GET.get('search', '')
        context['category_id'] = self.request.GET.get('category', '')
        context['status'] = self.request.GET.get('status', '')
        context['order_by'] = self.request.GET.get('order_by', '-created_at')
        
        # Statistics
        context['total_products'] = Product.objects.count()
        context['active_products'] = Product.objects.filter(is_active=True).count()
        context['low_stock_count'] = Product.objects.filter(stock__lte=10, stock__gt=0).count()
        context['out_of_stock_count'] = Product.objects.filter(stock=0).count()
        
        return context


class ProductDetailView(AdminRequiredMixin, DetailView):
    """Chi tiết sản phẩm"""
    model = Product
    template_name = 'admin_dashboard/products/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        
        # Get reviews
        context['reviews'] = product.reviews.select_related('user').order_by('-created_at')[:10]
        
        # Get order items (sales history)
        context['order_items'] = OrderItem.objects.filter(
            product=product
        ).select_related('order').order_by('-order__created_at')[:10]
        
        # Statistics
        context['total_sold'] = OrderItem.objects.filter(
            product=product,
            order__payment_status='paid'
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        context['total_revenue'] = OrderItem.objects.filter(
            product=product,
            order__payment_status='paid'
        ).aggregate(total=Sum(F('quantity') * F('price'), output_field=DecimalField()))['total'] or Decimal('0')
        
        return context


class ProductCreateView(AdminRequiredMixin, CreateView):
    """Thêm sản phẩm mới"""
    model = Product
    template_name = 'admin_dashboard/products/product_form.html'
    fields = ['name', 'description', 'short_description', 'category', 'price', 'discount_price', 'stock', 'unit', 'origin', 'nutrition_info', 'image', 'is_active', 'is_featured', 'is_new', 'is_bestseller', 'is_hot', 'meta_keywords', 'meta_description']
    success_url = reverse_lazy('reports:product_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Đã thêm sản phẩm "{form.instance.name}" thành công!')
        return super().form_valid(form)


class ProductUpdateView(AdminRequiredMixin, UpdateView):
    """Cập nhật sản phẩm"""
    model = Product
    template_name = 'admin_dashboard/products/product_form.html'
    fields = ['name', 'description', 'short_description', 'category', 'price', 'discount_price', 'stock', 'unit', 'origin', 'nutrition_info', 'image', 'is_active', 'is_featured', 'is_new', 'is_bestseller', 'is_hot', 'meta_keywords', 'meta_description']
    success_url = reverse_lazy('reports:product_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Đã cập nhật sản phẩm "{form.instance.name}" thành công!')
        return super().form_valid(form)


class ProductDeleteView(AdminRequiredMixin, DeleteView):
    """Xóa sản phẩm"""
    model = Product
    template_name = 'admin_dashboard/products/product_confirm_delete.html'
    success_url = reverse_lazy('reports:product_list')
    
    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        messages.success(request, f'Đã xóa sản phẩm "{product.name}" thành công!')
        return super().delete(request, *args, **kwargs)


# ============================================
# ORDER MANAGEMENT VIEWS
# ============================================

class OrderListView(AdminRequiredMixin, ListView):
    """Danh sách đơn hàng"""
    model = Order
    template_name = 'admin_dashboard/orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Order.objects.select_related('user').prefetch_related('items__product')
        
        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(order_number__icontains=search) |
                Q(user__email__icontains=search) |
                Q(user__username__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(phone__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by payment status
        payment_status = self.request.GET.get('payment_status', '')
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)
        
        # Filter by date range
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)
        
        # Ordering
        order_by = self.request.GET.get('order_by', '-created_at')
        queryset = queryset.order_by(order_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        context['payment_status'] = self.request.GET.get('payment_status', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')
        context['order_by'] = self.request.GET.get('order_by', '-created_at')
        
        # Statistics
        context['total_orders'] = Order.objects.count()
        context['pending_orders'] = Order.objects.filter(status='pending').count()
        context['processing_orders'] = Order.objects.filter(status='processing').count()
        context['shipped_orders'] = Order.objects.filter(status='shipped').count()
        context['delivered_orders'] = Order.objects.filter(status='delivered').count()
        context['cancelled_orders'] = Order.objects.filter(status='cancelled').count()
        
        return context


class OrderDetailView(AdminRequiredMixin, DetailView):
    """Chi tiết đơn hàng"""
    model = Order
    template_name = 'admin_dashboard/orders/order_detail.html'
    context_object_name = 'order'
    
    def get_queryset(self):
        return Order.objects.select_related('user').prefetch_related('items__product')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        
        # Get delivery info if exists
        try:
            delivery = Delivery.objects.select_related(
                'delivery_person',
                'delivery_person__user'
            ).prefetch_related(
                'tracking_logs',
                'tracking_logs__created_by'
            ).get(order=order)
            context['delivery'] = delivery
            context['tracking_logs'] = delivery.tracking_logs.all().order_by('-created_at')
        except Delivery.DoesNotExist:
            context['delivery'] = None
            context['tracking_logs'] = []
        
        # Get available delivery persons for assignment
        context['available_delivery_persons'] = DeliveryPerson.objects.filter(
            is_active=True
        ).select_related('user').annotate(
            current_deliveries_count=Count(
                'deliveries',
                filter=Q(deliveries__status__in=['assigned', 'picked_up', 'in_transit'])
            )
        ).order_by('current_deliveries_count', '-rating')
        
        return context


class OrderUpdateStatusView(AdminRequiredMixin, View):
    """Cập nhật trạng thái đơn hàng"""
    
    def post(self, request, pk):
        from django.utils import timezone
        from orders.utils import send_order_status_update_email
        
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES):
            old_status_code = order.status
            old_status_display = order.get_status_display()
            
            # Update status
            order.status = new_status
            
            # Update timestamp fields based on status
            if new_status == 'confirmed' and not order.confirmed_at:
                order.confirmed_at = timezone.now()
            elif new_status == 'shipped' and not order.shipped_at:
                order.shipped_at = timezone.now()
            elif new_status == 'delivered' and not order.delivered_at:
                order.delivered_at = timezone.now()
            
            order.save()
            
            # Send email notification if status actually changed
            if old_status_code != new_status:
                try:
                    send_order_status_update_email(order, old_status_code, new_status)
                    messages.success(
                        request, 
                        f'Đã cập nhật trạng thái đơn hàng #{order.order_number} từ "{old_status_display}" sang "{order.get_status_display()}" và gửi email thông báo đến khách hàng.'
                    )
                except Exception as e:
                    messages.warning(
                        request,
                        f'Đã cập nhật trạng thái đơn hàng #{order.order_number} nhưng không thể gửi email: {str(e)}'
                    )
            else:
                messages.info(request, 'Trạng thái không thay đổi.')
        else:
            messages.error(request, 'Trạng thái không hợp lệ!')
        
        return redirect('reports:order_detail', pk=pk)


# ============================================
# CUSTOMER MANAGEMENT VIEWS
# ============================================

class CustomerListView(AdminRequiredMixin, ListView):
    """Danh sách khách hàng"""
    model = User
    template_name = 'admin_dashboard/customers/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = User.objects.filter(role='customer')
        
        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status', '')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        # Ordering
        order_by = self.request.GET.get('order_by', '-date_joined')
        queryset = queryset.order_by(order_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        context['order_by'] = self.request.GET.get('order_by', '-date_joined')
        
        # Statistics
        context['total_customers'] = User.objects.filter(role='customer').count()
        context['active_customers'] = User.objects.filter(role='customer', is_active=True).count()
        context['inactive_customers'] = User.objects.filter(role='customer', is_active=False).count()
        
        return context


class CustomerDetailView(AdminRequiredMixin, DetailView):
    """Chi tiết khách hàng"""
    model = User
    template_name = 'admin_dashboard/customers/customer_detail.html'
    context_object_name = 'customer'
    
    def get_queryset(self):
        return User.objects.filter(role='customer')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.object
        
        # Get orders
        context['orders'] = Order.objects.filter(
            user=customer
        ).order_by('-created_at')[:10]
        
        # Get reviews
        context['reviews'] = Review.objects.filter(
            user=customer
        ).select_related('product').order_by('-created_at')[:10]
        
        # Statistics
        context['total_orders'] = Order.objects.filter(user=customer).count()
        context['total_spent'] = Order.objects.filter(
            user=customer,
            payment_status='paid'
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
        
        context['total_reviews'] = Review.objects.filter(user=customer).count()
        context['avg_rating'] = Review.objects.filter(user=customer).aggregate(
            avg=Avg('rating')
        )['avg'] or 0
        
        return context


# ============================================
# CATEGORY MANAGEMENT VIEWS
# ============================================

class CategoryListView(AdminRequiredMixin, ListView):
    """Danh sách danh mục"""
    model = Category
    template_name = 'admin_dashboard/categories/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20
    
    def get_queryset(self):
        # Annotate with product count for ordering
        queryset = Category.objects.annotate(
            total_products=Count('products')
        )
        
        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Filter by status
        status = self.request.GET.get('status', '')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        # Ordering - map product_count to total_products
        order_by = self.request.GET.get('order_by', 'name')
        if order_by == 'product_count':
            order_by = 'total_products'
        elif order_by == '-product_count':
            order_by = '-total_products'
        queryset = queryset.order_by(order_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        context['order_by'] = self.request.GET.get('order_by', 'name')
        
        # Statistics
        context['total_categories'] = Category.objects.count()
        context['active_categories'] = Category.objects.filter(is_active=True).count()
        context['inactive_categories'] = Category.objects.filter(is_active=False).count()
        
        return context


class CategoryDetailView(AdminRequiredMixin, DetailView):
    """Chi tiết danh mục"""
    model = Category
    template_name = 'admin_dashboard/categories/category_detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        
        # Get products in this category
        context['products'] = Product.objects.filter(
            category=category
        ).order_by('-created_at')[:20]
        
        # Statistics
        context['total_products'] = Product.objects.filter(category=category).count()
        context['active_products'] = Product.objects.filter(category=category, is_active=True).count()
        context['total_revenue'] = OrderItem.objects.filter(
            product__category=category,
            order__payment_status='paid'
        ).aggregate(
            total=Sum(F('quantity') * F('price'), output_field=DecimalField())
        )['total'] or Decimal('0')
        
        return context


class CategoryCreateView(AdminRequiredMixin, CreateView):
    """Thêm danh mục mới"""
    model = Category
    template_name = 'admin_dashboard/categories/category_form.html'
    fields = ['name', 'description', 'image', 'is_active']
    success_url = reverse_lazy('reports:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Đã thêm danh mục mới thành công!')
        return super().form_valid(form)


class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    """Cập nhật danh mục"""
    model = Category
    template_name = 'admin_dashboard/categories/category_form.html'
    fields = ['name', 'description', 'image', 'is_active']
    success_url = reverse_lazy('reports:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Đã cập nhật danh mục thành công!')
        return super().form_valid(form)


class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    """Xóa danh mục"""
    model = Category
    template_name = 'admin_dashboard/categories/category_confirm_delete.html'
    success_url = reverse_lazy('reports:category_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Đã xóa danh mục thành công!')
        return super().delete(request, *args, **kwargs)


# ============================================
# REVIEW MANAGEMENT VIEWS
# ============================================

class ReviewListView(AdminRequiredMixin, ListView):
    """Danh sách đánh giá"""
    model = Review
    template_name = 'admin_dashboard/reviews/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Review.objects.select_related('user', 'product').order_by('-created_at')
        
        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(user__username__icontains=search) |
                Q(product__name__icontains=search) |
                Q(comment__icontains=search)
            )
        
        # Filter by rating
        rating = self.request.GET.get('rating', '')
        if rating:
            queryset = queryset.filter(rating=rating)
        
        # Filter by product
        product_id = self.request.GET.get('product', '')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['rating'] = self.request.GET.get('rating', '')
        context['product'] = self.request.GET.get('product', '')
        
        # Statistics
        context['total_reviews'] = Review.objects.count()
        context['avg_rating'] = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0
        
        return context


class ReviewDetailView(AdminRequiredMixin, DetailView):
    """Chi tiết đánh giá"""
    model = Review
    template_name = 'admin_dashboard/reviews/review_detail.html'
    context_object_name = 'review'


class ReviewDeleteView(AdminRequiredMixin, DeleteView):
    """Xóa đánh giá"""
    model = Review
    template_name = 'admin_dashboard/reviews/review_confirm_delete.html'
    success_url = reverse_lazy('reports:review_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Đã xóa đánh giá thành công!')
        return super().delete(request, *args, **kwargs)


# ============================================
# PRODUCT IMAGE MANAGEMENT VIEWS
# ============================================

class ProductImageManageView(AdminRequiredMixin, View):
    """Quản lý ảnh sản phẩm"""
    
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        images = ProductImage.objects.filter(product=product).order_by('order')
        
        context = {
            'product': product,
            'images': images,
        }
        return render(request, 'admin_dashboard/products/product_images.html', context)
    
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        
        # Handle multiple file uploads
        image_files = request.FILES.getlist('images')
        
        if image_files:
            is_primary = request.POST.get('is_primary', False)
            
            # If this is primary, unset other primary images
            if is_primary:
                ProductImage.objects.filter(product=product, is_primary=True).update(is_primary=False)
            
            # Get the next order number
            max_order = ProductImage.objects.filter(product=product).aggregate(
                max_order=models.Max('order')
            )['max_order'] or 0
            
            # Create images
            uploaded_count = 0
            for idx, image_file in enumerate(image_files):
                # Only set first image as primary if checkbox is checked
                is_this_primary = is_primary and idx == 0
                
                ProductImage.objects.create(
                    product=product,
                    image=image_file,
                    is_primary=is_this_primary,
                    order=max_order + idx + 1
                )
                uploaded_count += 1
            
            if uploaded_count == 1:
                messages.success(request, 'Đã thêm 1 ảnh thành công!')
            else:
                messages.success(request, f'Đã thêm {uploaded_count} ảnh thành công!')
        else:
            messages.error(request, 'Vui lòng chọn ít nhất một ảnh!')
        
        return redirect('reports:product_images', product_id=product_id)


class ProductImageDeleteView(AdminRequiredMixin, View):
    """Xóa ảnh sản phẩm"""
    
    def post(self, request, image_id):
        image = get_object_or_404(ProductImage, id=image_id)
        product_id = image.product.id
        
        # Delete the image file
        if image.image:
            image.image.delete()
        
        # Delete the database record
        image.delete()
        
        messages.success(request, 'Đã xóa ảnh thành công!')
        return redirect('reports:product_images', product_id=product_id)


class ProductImageSetPrimaryView(AdminRequiredMixin, View):
    """Đặt ảnh làm ảnh chính"""
    
    def post(self, request, image_id):
        image = get_object_or_404(ProductImage, id=image_id)
        product = image.product
        
        # Unset all primary images for this product
        ProductImage.objects.filter(product=product).update(is_primary=False)
        
        # Set this image as primary
        image.is_primary = True
        image.save()
        
        messages.success(request, 'Đã đặt làm ảnh chính!')
        return redirect('reports:product_images', product_id=product.id)


# ============================================
# ADVANCED ANALYTICS VIEWS
# ============================================

class AdvancedAnalyticsView(AdminRequiredMixin, TemplateView):
    """Trang thống kê nâng cao"""
    template_name = 'admin_dashboard/analytics/advanced.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get date range from request or default to last 30 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        if date_from:
            start_date = datetime.strptime(date_from, '%Y-%m-%d').date()
        if date_to:
            end_date = datetime.strptime(date_to, '%Y-%m-%d').date()
        
        context['date_from'] = start_date
        context['date_to'] = end_date
        
        # ============ REVENUE ANALYTICS ============
        
        # Daily revenue trend
        daily_revenue = Order.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
            payment_status='paid'
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            revenue=Sum('total_amount'),
            orders=Count('id')
        ).order_by('date')
        
        revenue_dates = [stat['date'].strftime('%Y-%m-%d') for stat in daily_revenue]
        revenue_amounts = [float(stat['revenue']) for stat in daily_revenue]
        revenue_orders = [stat['orders'] for stat in daily_revenue]
        
        context.update({
            'revenue_dates': revenue_dates,
            'revenue_amounts': revenue_amounts,
            'revenue_orders': revenue_orders,
        })
        
        # ============ PRODUCT PERFORMANCE ============
        
        # Top selling products
        top_products = OrderItem.objects.filter(
            order__created_at__date__gte=start_date,
            order__created_at__date__lte=end_date,
            order__payment_status='paid'
        ).values(
            'product__name'
        ).annotate(
            revenue=Sum(F('quantity') * F('price'), output_field=DecimalField()),
            quantity=Sum('quantity')
        ).order_by('-revenue')[:10]
        
        top_product_names = [p['product__name'] for p in top_products]
        top_product_revenue = [float(p['revenue']) for p in top_products]
        top_product_quantity = [p['quantity'] for p in top_products]
        
        context.update({
            'top_product_names': top_product_names,
            'top_product_revenue': top_product_revenue,
            'top_product_quantity': top_product_quantity,
        })
        
        # ============ CATEGORY PERFORMANCE ============
        
        category_stats = OrderItem.objects.filter(
            order__created_at__date__gte=start_date,
            order__created_at__date__lte=end_date,
            order__payment_status='paid'
        ).values(
            'product__category__name'
        ).annotate(
            revenue=Sum(F('quantity') * F('price'), output_field=DecimalField()),
            total_quantity=Sum('quantity')
        ).order_by('-revenue')
        
        category_names = [c['product__category__name'] or 'Chưa phân loại' for c in category_stats]
        category_revenue = [float(c['revenue']) for c in category_stats]
        
        context.update({
            'category_names': category_names,
            'category_revenue': category_revenue,
        })
        
        # ============ CUSTOMER ANALYTICS ============
        
        # Top customers by spending
        top_customers = Order.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
            payment_status='paid'
        ).values(
            'user__username',
            'user__email'
        ).annotate(
            total_spent=Sum('total_amount'),
            order_count=Count('id')
        ).order_by('-total_spent')[:10]
        
        context['top_customers'] = top_customers
        
        # Customer acquisition
        new_customers_trend = User.objects.filter(
            role='customer',
            date_joined__date__gte=start_date,
            date_joined__date__lte=end_date
        ).annotate(
            date=TruncDate('date_joined')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        customer_dates = [c['date'].strftime('%Y-%m-%d') for c in new_customers_trend]
        customer_counts = [c['count'] for c in new_customers_trend]
        
        context.update({
            'customer_dates': customer_dates,
            'customer_counts': customer_counts,
        })
        
        # ============ ORDER ANALYTICS ============
        
        # Average order value
        avg_order_value = Order.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
            payment_status='paid'
        ).aggregate(avg=Avg('total_amount'))['avg'] or 0
        
        # Order status distribution
        order_status_dist = Order.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        ).values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        status_labels = [dict(Order.STATUS_CHOICES).get(s['status'], s['status']) for s in order_status_dist]
        status_counts = [s['count'] for s in order_status_dist]
        
        context.update({
            'avg_order_value': avg_order_value,
            'status_labels': status_labels,
            'status_counts': status_counts,
        })
        
        # ============ PAYMENT METHOD ANALYTICS ============
        
        payment_stats = Order.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
            payment_status='paid'
        ).values('payment_method').annotate(
            count=Count('id'),
            revenue=Sum('total_amount')
        ).order_by('-revenue')
        
        payment_methods = [dict(Order.PAYMENT_METHOD_CHOICES).get(p['payment_method'], p['payment_method']) for p in payment_stats]
        payment_counts = [p['count'] for p in payment_stats]
        payment_revenue = [float(p['revenue']) for p in payment_stats]
        
        context.update({
            'payment_methods': payment_methods,
            'payment_counts': payment_counts,
            'payment_revenue': payment_revenue,
        })
        
        # ============ SUMMARY STATS ============
        
        total_revenue = sum(revenue_amounts) if revenue_amounts else 0
        total_orders = Order.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        ).count()
        total_customers_in_period = Order.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        ).values('user').distinct().count()
        
        context.update({
            'period_total_revenue': total_revenue,
            'period_total_orders': total_orders,
            'period_total_customers': total_customers_in_period,
            'period_avg_order_value': avg_order_value,
        })
        
        return context


# ============================================================
# DELIVERY MANAGEMENT VIEWS
# ============================================================

class DeliveryListView(AdminRequiredMixin, ListView):
    """Danh sách giao hàng"""
    model = Delivery
    template_name = 'reports/delivery_list.html'
    context_object_name = 'deliveries'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = Delivery.objects.select_related(
            'order',
            'order__user',
            'delivery_person',
            'delivery_person__user'
        ).order_by('-created_at')
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by delivery person
        delivery_person_id = self.request.GET.get('delivery_person')
        if delivery_person_id:
            queryset = queryset.filter(delivery_person_id=delivery_person_id)
        
        # Filter by date range
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        # Search by order number or customer name
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(order__order_number__icontains=search) |
                Q(order__user__username__icontains=search) |
                Q(order__user__email__icontains=search) |
                Q(recipient_name__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add status choices for filter
        context['status_choices'] = Delivery.STATUS_CHOICES
        
        # Add delivery persons for filter
        context['delivery_persons'] = DeliveryPerson.objects.filter(
            is_active=True
        ).select_related('user')
        
        # Add statistics
        queryset = self.get_queryset()
        context['total_count'] = queryset.count()
        context['pending_count'] = queryset.filter(status='pending').count()
        context['active_count'] = queryset.filter(
            status__in=['assigned', 'picked_up', 'in_transit']
        ).count()
        context['completed_count'] = queryset.filter(status='delivered').count()
        context['failed_count'] = queryset.filter(status='failed').count()
        
        return context


class DeliveryDetailView(AdminRequiredMixin, DetailView):
    """Chi tiết giao hàng"""
    model = Delivery
    template_name = 'reports/delivery_detail.html'
    context_object_name = 'delivery'
    
    def get_queryset(self):
        return Delivery.objects.select_related(
            'order',
            'order__user',
            'delivery_person',
            'delivery_person__user'
        ).prefetch_related(
            'order__items',
            'order__items__product',
            'tracking_logs',
            'tracking_logs__created_by'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get tracking logs
        context['tracking_logs'] = self.object.tracking_logs.all().order_by('-created_at')
        
        # Get available delivery persons for assignment
        context['available_delivery_persons'] = DeliveryPerson.objects.filter(
            is_active=True
        ).select_related('user')
        
        return context


class DeliveryAssignView(AdminRequiredMixin, View):
    """Phân công giao hàng cho nhân viên"""
    
    def post(self, request, pk):
        delivery = get_object_or_404(Delivery, pk=pk)
        delivery_person_id = request.POST.get('delivery_person_id')
        
        # Determine redirect URL based on referer
        referer = request.META.get('HTTP_REFERER', '')
        if 'orders' in referer:
            redirect_url_name = 'reports:order_detail'
            redirect_pk = delivery.order.pk
        else:
            redirect_url_name = 'reports:delivery_detail'
            redirect_pk = pk
        
        if not delivery_person_id:
            messages.error(request, 'Vui lòng chọn nhân viên giao hàng!')
            return redirect(redirect_url_name, pk=redirect_pk)
        
        delivery_person = get_object_or_404(DeliveryPerson, pk=delivery_person_id)
        
        # Assign delivery (this will also send email)
        delivery.assign_to_person(delivery_person)
        
        # Check if delivery person has email
        if delivery_person.user.email:
            messages.success(
                request,
                f'Đã phân công đơn hàng #{delivery.order.order_number} cho {delivery_person.user.get_full_name()} và gửi email thông báo!'
            )
        else:
            messages.success(
                request,
                f'Đã phân công đơn hàng #{delivery.order.order_number} cho {delivery_person.user.get_full_name()}!'
            )
            messages.warning(
                request,
                f'Không thể gửi email vì {delivery_person.user.get_full_name()} chưa có địa chỉ email.'
            )
        
        return redirect(redirect_url_name, pk=redirect_pk)


class DeliveryUpdateStatusView(AdminRequiredMixin, View):
    """Cập nhật trạng thái giao hàng"""
    
    def post(self, request, pk):
        delivery = get_object_or_404(Delivery, pk=pk)
        new_status = request.POST.get('status')
        
        # Determine redirect URL based on referer
        referer = request.META.get('HTTP_REFERER', '')
        if 'orders' in referer:
            redirect_url_name = 'reports:order_detail'
            redirect_pk = delivery.order.pk
        else:
            redirect_url_name = 'reports:delivery_detail'
            redirect_pk = pk
        
        if not new_status:
            messages.error(request, 'Vui lòng chọn trạng thái!')
            return redirect(redirect_url_name, pk=redirect_pk)
        
        # Update status based on new_status
        if new_status == 'picked_up':
            delivery.mark_picked_up(user=request.user)
            messages.success(request, 'Đã cập nhật: Đã lấy hàng')
        
        elif new_status == 'in_transit':
            delivery.mark_in_transit(user=request.user)
            messages.success(request, 'Đã cập nhật: Đang giao hàng')
        
        elif new_status == 'delivered':
            delivery.mark_delivered(user=request.user)
            messages.success(request, 'Đã cập nhật: Giao hàng thành công!')
        
        elif new_status == 'failed':
            failure_reason = request.POST.get('failure_reason', 'Không rõ lý do')
            delivery.mark_failed(reason=failure_reason, user=request.user)
            messages.warning(request, f'Đã đánh dấu giao hàng thất bại: {failure_reason}')
        
        else:
            # Direct status update for other cases
            delivery.status = new_status
            delivery.save()
            messages.success(request, f'Đã cập nhật trạng thái: {delivery.get_status_display()}')
        
        return redirect(redirect_url_name, pk=redirect_pk)


class DeliveryAddTrackingView(AdminRequiredMixin, View):
    """Thêm tracking log cho delivery"""
    
    def post(self, request, pk):
        delivery = get_object_or_404(Delivery, pk=pk)
        
        message = request.POST.get('message')
        location_name = request.POST.get('location_name', '')
        
        if not message:
            messages.error(request, 'Vui lòng nhập nội dung tracking!')
            return redirect('reports:delivery_detail', pk=pk)
        
        # Create tracking log
        DeliveryTracking.objects.create(
            delivery=delivery,
            status=delivery.status,
            message=message,
            location_name=location_name,
            created_by=request.user
        )
        
        messages.success(request, 'Đã thêm thông tin theo dõi!')
        return redirect('reports:delivery_detail', pk=pk)


class DeliveryPersonListView(AdminRequiredMixin, ListView):
    """Danh sách nhân viên giao hàng"""
    model = DeliveryPerson
    template_name = 'admin_dashboard/delivery_person_list.html'
    context_object_name = 'delivery_persons'
    paginate_by = 30
    
    def get_queryset(self):
        queryset = DeliveryPerson.objects.select_related('user').annotate(
            current_deliveries_count=Count(
                'deliveries',
                filter=Q(deliveries__status__in=['assigned', 'picked_up', 'in_transit'])
            ),
            success_rate_calc=models.Case(
                models.When(total_deliveries=0, then=0),
                default=(F('successful_deliveries') * 100.0 / F('total_deliveries')),
                output_field=models.FloatField()
            )
        ).order_by('-is_active', '-rating')
        
        # Filter by active status
        is_active = self.request.GET.get('is_active')
        if is_active == 'true':
            queryset = queryset.filter(is_active=True)
        elif is_active == 'false':
            queryset = queryset.filter(is_active=False)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(user__username__icontains=search) |
                Q(user__email__icontains=search) |
                Q(phone__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        queryset = self.get_queryset()
        context['total_count'] = queryset.count()
        context['active_count'] = queryset.filter(is_active=True).count()
        context['inactive_count'] = queryset.filter(is_active=False).count()
        
        return context


class DeliveryPersonDetailView(AdminRequiredMixin, DetailView):
    """Chi tiết nhân viên giao hàng"""
    model = DeliveryPerson
    template_name = 'admin_dashboard/delivery_person_detail.html'
    context_object_name = 'delivery_person'
    
    def get_queryset(self):
        return DeliveryPerson.objects.select_related('user').prefetch_related(
            'deliveries',
            'deliveries__order',
            'deliveries__order__user'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get recent deliveries
        context['recent_deliveries'] = self.object.deliveries.select_related(
            'order', 'order__user'
        ).order_by('-created_at')[:20]
        
        # Get current deliveries (in progress)
        context['current_deliveries'] = self.object.deliveries.filter(
            status__in=['assigned', 'picked_up', 'in_transit']
        ).select_related('order', 'order__user')
        
        # Statistics by month
        today = timezone.now().date()
        this_month = today.replace(day=1)
        
        context['deliveries_this_month'] = self.object.deliveries.filter(
            created_at__gte=this_month
        ).count()
        
        context['successful_this_month'] = self.object.deliveries.filter(
            created_at__gte=this_month,
            status='delivered'
        ).count()
        
        # Calculate success rate
        if self.object.total_deliveries > 0:
            context['success_rate'] = (self.object.successful_deliveries / self.object.total_deliveries) * 100
        else:
            context['success_rate'] = 0
        
        return context


# ============================================
# USER MANAGEMENT VIEWS (ALL ROLES)
# ============================================

class UserListView(AdminRequiredMixin, ListView):
    """Danh sách tất cả users (admin, staff, shipper, customer)"""
    model = User
    template_name = 'admin_dashboard/users/user_list.html'
    context_object_name = 'users'
    paginate_by = 30
    
    def get_queryset(self):
        from django.contrib.auth.models import Group
        
        queryset = User.objects.all().prefetch_related('groups')
        
        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone__icontains=search)
            )
        
        # Filter by role
        role = self.request.GET.get('role', '')
        if role == 'admin':
            queryset = queryset.filter(is_superuser=True)
        elif role == 'staff':
            queryset = queryset.filter(groups__name='Staff')
        elif role == 'shipper':
            queryset = queryset.filter(groups__name='Shipper')
        elif role == 'customer':
            queryset = queryset.filter(groups__name='Customer')
        
        # Filter by status
        status = self.request.GET.get('status', '')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        # Ordering
        order_by = self.request.GET.get('order_by', '-date_joined')
        queryset = queryset.order_by(order_by)
        
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.contrib.auth.models import Group
        
        context['search'] = self.request.GET.get('search', '')
        context['role'] = self.request.GET.get('role', '')
        context['status'] = self.request.GET.get('status', '')
        context['order_by'] = self.request.GET.get('order_by', '-date_joined')
        
        # Statistics
        context['total_users'] = User.objects.count()
        context['admin_count'] = User.objects.filter(is_superuser=True).count()
        context['staff_count'] = User.objects.filter(groups__name='Staff').distinct().count()
        context['shipper_count'] = User.objects.filter(groups__name='Shipper').distinct().count()
        context['customer_count'] = User.objects.filter(groups__name='Customer').distinct().count()
        context['active_users'] = User.objects.filter(is_active=True).count()
        context['inactive_users'] = User.objects.filter(is_active=False).count()
        
        return context


class UserDetailView(AdminRequiredMixin, DetailView):
    """Chi tiết user"""
    model = User
    template_name = 'admin_dashboard/users/user_detail.html'
    context_object_name = 'user_detail'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        
        # Get user's groups
        context['user_groups'] = user.groups.all()
        
        # Get orders if customer
        if user.groups.filter(name='Customer').exists():
            context['orders'] = Order.objects.filter(
                user=user
            ).order_by('-created_at')[:10]
            
            context['total_orders'] = Order.objects.filter(user=user).count()
            context['total_spent'] = Order.objects.filter(
                user=user,
                payment_status='paid'
            ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
        
        # Get delivery person info if shipper
        if user.groups.filter(name='Shipper').exists():
            try:
                context['delivery_person'] = DeliveryPerson.objects.get(user=user)
                context['deliveries'] = Delivery.objects.filter(
                    delivery_person=context['delivery_person']
                ).select_related('order').order_by('-created_at')[:10]
            except DeliveryPerson.DoesNotExist:
                context['delivery_person'] = None
        
        # Get reviews
        context['reviews'] = Review.objects.filter(
            user=user
        ).select_related('product').order_by('-created_at')[:10]
        
        return context


class UserCreateView(AdminRequiredMixin, CreateView):
    """Thêm user mới"""
    model = User
    template_name = 'admin_dashboard/users/user_form.html'
    fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'address', 'is_active', 'is_staff', 'is_superuser']
    success_url = reverse_lazy('reports:user_list')
    
    def get_context_data(self, **kwargs):
        from django.contrib.auth.models import Group
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['is_create'] = True
        return context
    
    def form_valid(self, form):
        from django.contrib.auth.models import Group
        
        # Set a default password (user should change it later)
        user = form.save(commit=False)
        default_password = self.request.POST.get('password', 'password123')
        user.set_password(default_password)
        user.save()
        
        # Assign groups
        selected_groups = self.request.POST.getlist('groups')
        for group_id in selected_groups:
            try:
                group = Group.objects.get(id=group_id)
                user.groups.add(group)
            except Group.DoesNotExist:
                pass
        
        messages.success(
            self.request, 
            f'Đã thêm user "{user.username}" thành công! Mật khẩu mặc định: {default_password}'
        )
        return super().form_valid(form)


class UserUpdateView(AdminRequiredMixin, UpdateView):
    """Cập nhật user"""
    model = User
    template_name = 'admin_dashboard/users/user_form.html'
    fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'address', 'is_active', 'is_staff', 'is_superuser']
    success_url = reverse_lazy('reports:user_list')
    
    def get_context_data(self, **kwargs):
        from django.contrib.auth.models import Group
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['user_groups'] = self.object.groups.all()
        context['is_create'] = False
        return context
    
    def form_valid(self, form):
        from django.contrib.auth.models import Group
        
        user = form.save()
        
        # Update groups
        user.groups.clear()
        selected_groups = self.request.POST.getlist('groups')
        for group_id in selected_groups:
            try:
                group = Group.objects.get(id=group_id)
                user.groups.add(group)
            except Group.DoesNotExist:
                pass
        
        # Update password if provided
        new_password = self.request.POST.get('new_password', '').strip()
        if new_password:
            user.set_password(new_password)
            user.save()
            messages.success(self.request, f'Đã cập nhật user "{user.username}" và đổi mật khẩu thành công!')
        else:
            messages.success(self.request, f'Đã cập nhật user "{user.username}" thành công!')
        
        return super().form_valid(form)


class UserDeleteView(AdminRequiredMixin, DeleteView):
    """Xóa user"""
    model = User
    template_name = 'admin_dashboard/users/user_confirm_delete.html'
    success_url = reverse_lazy('reports:user_list')
    context_object_name = 'user_detail'
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        username = user.username
        
        # Prevent deleting yourself
        if user == request.user:
            messages.error(request, 'Bạn không thể xóa chính mình!')
            return redirect('reports:user_list')
        
        messages.success(request, f'Đã xóa user "{username}" thành công!')
        return super().delete(request, *args, **kwargs)


class UserToggleActiveView(AdminRequiredMixin, View):
    """Bật/tắt trạng thái active của user"""
    
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        
        # Prevent disabling yourself
        if user == request.user:
            messages.error(request, 'Bạn không thể vô hiệu hóa chính mình!')
            return redirect('reports:user_detail', pk=pk)
        
        user.is_active = not user.is_active
        user.save()
        
        if user.is_active:
            messages.success(request, f'Đã kích hoạt user "{user.username}"!')
        else:
            messages.warning(request, f'Đã vô hiệu hóa user "{user.username}"!')
        
        return redirect('reports:user_detail', pk=pk)


class UserResetPasswordView(AdminRequiredMixin, View):
    """Reset mật khẩu user"""
    
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        new_password = request.POST.get('new_password', 'password123')
        
        user.set_password(new_password)
        user.save()
        
        messages.success(
            request, 
            f'Đã reset mật khẩu cho user "{user.username}" thành: {new_password}'
        )
        return redirect('reports:user_detail', pk=pk)


# ==================== DISCOUNT MANAGEMENT ====================

class DiscountListView(AdminRequiredMixin, ListView):
    """Danh sách mã giảm giá"""
    model = Discount
    template_name = 'admin_dashboard/discounts/discount_list.html'
    context_object_name = 'discounts'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Discount.objects.all().order_by('-created_at')
        
        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) | 
                Q(description__icontains=search)
            )
        
        # Filter by status
        status_filter = self.request.GET.get('status', '')
        if status_filter == 'active':
            queryset = queryset.filter(is_active=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(is_active=False)
        elif status_filter == 'valid':
            now = timezone.now()
            queryset = queryset.filter(
                is_active=True,
                valid_from__lte=now,
                valid_to__gte=now
            )
        elif status_filter == 'expired':
            now = timezone.now()
            queryset = queryset.filter(valid_to__lt=now)
        
        # Filter by type
        type_filter = self.request.GET.get('type', '')
        if type_filter:
            queryset = queryset.filter(discount_type=type_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['type_filter'] = self.request.GET.get('type', '')
        
        # Statistics
        total_discounts = Discount.objects.count()
        active_discounts = Discount.objects.filter(is_active=True).count()
        now = timezone.now()
        valid_discounts = Discount.objects.filter(
            is_active=True,
            valid_from__lte=now,
            valid_to__gte=now
        ).count()
        expired_discounts = Discount.objects.filter(valid_to__lt=now).count()
        
        context.update({
            'total_discounts': total_discounts,
            'active_discounts': active_discounts,
            'valid_discounts': valid_discounts,
            'expired_discounts': expired_discounts,
        })
        
        return context


class DiscountDetailView(AdminRequiredMixin, DetailView):
    """Chi tiết mã giảm giá"""
    model = Discount
    template_name = 'admin_dashboard/discounts/discount_detail.html'
    context_object_name = 'discount'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get orders that used this discount
        discount = self.object
        orders_used = Order.objects.filter(discount=discount).order_by('-created_at')
        
        # Calculate statistics
        total_revenue = orders_used.filter(payment_status='paid').aggregate(
            total=Sum('total_amount')
        )['total'] or Decimal('0')
        
        total_discount_amount = orders_used.filter(payment_status='paid').aggregate(
            total=Sum('discount_amount')
        )['total'] or Decimal('0')
        
        context.update({
            'orders_used': orders_used[:10],  # Show recent 10 orders
            'total_orders': orders_used.count(),
            'total_revenue': total_revenue,
            'total_discount_amount': total_discount_amount,
        })
        
        return context


class DiscountCreateView(AdminRequiredMixin, CreateView):
    """Tạo mã giảm giá mới"""
    model = Discount
    template_name = 'admin_dashboard/discounts/discount_form.html'
    fields = [
        'code', 'description', 'discount_type', 'value', 
        'min_purchase', 'max_uses', 
        'valid_from', 'valid_to', 'is_active'
    ]
    success_url = reverse_lazy('reports:discount_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = True
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Đã tạo mã giảm giá "{form.instance.code}" thành công!')
        return super().form_valid(form)


class DiscountUpdateView(AdminRequiredMixin, UpdateView):
    """Cập nhật mã giảm giá"""
    model = Discount
    template_name = 'admin_dashboard/discounts/discount_form.html'
    fields = [
        'code', 'description', 'discount_type', 'value', 
        'min_purchase', 'max_uses', 
        'valid_from', 'valid_to', 'is_active'
    ]
    success_url = reverse_lazy('reports:discount_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = False
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Đã cập nhật mã giảm giá "{form.instance.code}" thành công!')
        return super().form_valid(form)


class DiscountDeleteView(AdminRequiredMixin, DeleteView):
    """Xóa mã giảm giá"""
    model = Discount
    template_name = 'admin_dashboard/discounts/discount_confirm_delete.html'
    success_url = reverse_lazy('reports:discount_list')
    context_object_name = 'discount'
    
    def delete(self, request, *args, **kwargs):
        discount = self.get_object()
        code = discount.code
        messages.success(request, f'Đã xóa mã giảm giá "{code}" thành công!')
        return super().delete(request, *args, **kwargs)


class DiscountToggleActiveView(AdminRequiredMixin, View):
    """Bật/tắt trạng thái mã giảm giá"""
    
    def post(self, request, pk):
        discount = get_object_or_404(Discount, pk=pk)
        discount.is_active = not discount.is_active
        discount.save()
        
        if discount.is_active:
            messages.success(request, f'Đã kích hoạt mã giảm giá "{discount.code}"!')
        else:
            messages.warning(request, f'Đã vô hiệu hóa mã giảm giá "{discount.code}"!')
        
        return redirect('reports:discount_detail', pk=pk)


# ============================================
# SHOP REVIEW MANAGEMENT VIEWS
# ============================================

class ShopReviewListView(AdminRequiredMixin, ListView):
    """Danh sách đánh giá cửa hàng"""
    model = ShopReview
    template_name = 'admin_dashboard/shop_reviews/shop_review_list.html'
    context_object_name = 'shop_reviews'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ShopReview.objects.select_related('user').order_by('-created_at')
        
        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(user__username__icontains=search) |
                Q(user__email__icontains=search) |
                Q(title__icontains=search) |
                Q(comment__icontains=search)
            )
        
        # Filter by rating
        rating = self.request.GET.get('rating', '')
        if rating:
            queryset = queryset.filter(rating=rating)
        
        # Filter by approval status
        approval = self.request.GET.get('approval', '')
        if approval == 'approved':
            queryset = queryset.filter(is_approved=True)
        elif approval == 'pending':
            queryset = queryset.filter(is_approved=False)
        
        # Filter by featured status
        featured = self.request.GET.get('featured', '')
        if featured == 'yes':
            queryset = queryset.filter(is_featured=True)
        elif featured == 'no':
            queryset = queryset.filter(is_featured=False)
        
        # Filter by verified purchase
        verified = self.request.GET.get('verified', '')
        if verified == 'yes':
            queryset = queryset.filter(is_verified_purchase=True)
        elif verified == 'no':
            queryset = queryset.filter(is_verified_purchase=False)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['rating'] = self.request.GET.get('rating', '')
        context['approval'] = self.request.GET.get('approval', '')
        context['featured'] = self.request.GET.get('featured', '')
        context['verified'] = self.request.GET.get('verified', '')
        
        # Statistics
        context['total_reviews'] = ShopReview.objects.count()
        context['approved_reviews'] = ShopReview.objects.filter(is_approved=True).count()
        context['pending_reviews'] = ShopReview.objects.filter(is_approved=False).count()
        context['featured_reviews'] = ShopReview.objects.filter(is_featured=True).count()
        context['verified_reviews'] = ShopReview.objects.filter(is_verified_purchase=True).count()
        context['avg_rating'] = ShopReview.objects.aggregate(avg=Avg('rating'))['avg'] or 0
        
        # Rating distribution
        rating_dist = {}
        for i in range(1, 6):
            rating_dist[i] = ShopReview.objects.filter(rating=i).count()
        context['rating_distribution'] = rating_dist
        
        return context


class ShopReviewDetailView(AdminRequiredMixin, DetailView):
    """Chi tiết đánh giá cửa hàng"""
    model = ShopReview
    template_name = 'admin_dashboard/shop_reviews/shop_review_detail.html'
    context_object_name = 'shop_review'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = self.object
        
        # Get user's order history to verify purchase
        from orders.models import Order
        user_orders = Order.objects.filter(
            user=review.user,
            status__in=['delivered', 'completed']
        ).order_by('-created_at')[:5]
        context['user_orders'] = user_orders
        
        # Check if user has actually purchased
        has_purchased = user_orders.exists()
        context['has_purchased'] = has_purchased
        
        # Other reviews from this user
        other_reviews = ShopReview.objects.filter(user=review.user).exclude(pk=review.pk)[:5]
        context['other_reviews'] = other_reviews
        
        return context


class ShopReviewDeleteView(AdminRequiredMixin, DeleteView):
    """Xóa đánh giá cửa hàng"""
    model = ShopReview
    template_name = 'admin_dashboard/shop_reviews/shop_review_confirm_delete.html'
    success_url = reverse_lazy('reports:shop_review_list')
    context_object_name = 'shop_review'
    
    def delete(self, request, *args, **kwargs):
        shop_review = self.get_object()
        username = shop_review.user.username
        messages.success(request, f'Đã xóa đánh giá của "{username}" thành công!')
        return super().delete(request, *args, **kwargs)


class ShopReviewToggleApprovalView(AdminRequiredMixin, View):
    """Bật/tắt trạng thái duyệt đánh giá"""
    
    def post(self, request, pk):
        shop_review = get_object_or_404(ShopReview, pk=pk)
        shop_review.is_approved = not shop_review.is_approved
        shop_review.save()
        
        if shop_review.is_approved:
            messages.success(request, f'Đã duyệt đánh giá của "{shop_review.user.username}"!')
        else:
            messages.warning(request, f'Đã ẩn đánh giá của "{shop_review.user.username}"!')
        
        return redirect('reports:shop_review_detail', pk=pk)


class ShopReviewToggleFeaturedView(AdminRequiredMixin, View):
    """Bật/tắt trạng thái nổi bật"""
    
    def post(self, request, pk):
        shop_review = get_object_or_404(ShopReview, pk=pk)
        shop_review.is_featured = not shop_review.is_featured
        shop_review.save()
        
        if shop_review.is_featured:
            messages.success(request, f'Đã đặt đánh giá làm nổi bật!')
        else:
            messages.info(request, f'Đã bỏ trạng thái nổi bật!')
        
        return redirect('reports:shop_review_detail', pk=pk)


class ShopReviewToggleVerifiedView(AdminRequiredMixin, View):
    """Bật/tắt trạng thái đã mua hàng"""
    
    def post(self, request, pk):
        shop_review = get_object_or_404(ShopReview, pk=pk)
        shop_review.is_verified_purchase = not shop_review.is_verified_purchase
        shop_review.save()
        
        if shop_review.is_verified_purchase:
            messages.success(request, f'Đã xác nhận người dùng đã mua hàng!')
        else:
            messages.info(request, f'Đã bỏ xác nhận mua hàng!')
        
        return redirect('reports:shop_review_detail', pk=pk)


# ==================== NEWSLETTER MANAGEMENT ====================

class NewsletterListView(AdminRequiredMixin, ListView):
    """Danh sách đăng ký nhận tin"""
    from products.models import Newsletter
    model = Newsletter
    template_name = 'admin_dashboard/newsletter_list.html'
    context_object_name = 'newsletters'
    paginate_by = 50
    
    def get_queryset(self):
        from products.models import Newsletter
        queryset = Newsletter.objects.all().order_by('-subscribed_at')
        
        # Search
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(email__icontains=search_query)
            )
        
        # Filter by status
        status_filter = self.request.GET.get('status', '')
        if status_filter == 'active':
            queryset = queryset.filter(is_active=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        # Filter by date range
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        if date_from:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(subscribed_at__date__gte=date_from)
            except ValueError:
                pass
        
        if date_to:
            try:
                date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(subscribed_at__date__lte=date_to)
            except ValueError:
                pass
        
        return queryset
    
    def get_context_data(self, **kwargs):
        from products.models import Newsletter
        context = super().get_context_data(**kwargs)
        
        # Statistics
        context['total_subscribers'] = Newsletter.objects.count()
        context['active_subscribers'] = Newsletter.objects.filter(is_active=True).count()
        context['inactive_subscribers'] = Newsletter.objects.filter(is_active=False).count()
        
        # Recent subscriptions (last 7 days)
        seven_days_ago = timezone.now() - timedelta(days=7)
        context['recent_subscribers'] = Newsletter.objects.filter(
            subscribed_at__gte=seven_days_ago
        ).count()
        
        # Filter params for template
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')
        
        return context


class NewsletterDetailView(AdminRequiredMixin, DetailView):
    """Chi tiết đăng ký nhận tin"""
    from products.models import Newsletter
    model = Newsletter
    template_name = 'admin_dashboard/newsletter_detail.html'
    context_object_name = 'newsletter'
    
    def get_queryset(self):
        from products.models import Newsletter
        return Newsletter.objects.all()


class NewsletterToggleActiveView(AdminRequiredMixin, View):
    """Bật/tắt trạng thái đăng ký"""
    
    def post(self, request, pk):
        from products.models import Newsletter
        newsletter = get_object_or_404(Newsletter, pk=pk)
        
        if newsletter.is_active:
            # Deactivate
            newsletter.is_active = False
            newsletter.unsubscribed_at = timezone.now()
            newsletter.save()
            messages.warning(request, f'Đã vô hiệu hóa đăng ký của {newsletter.email}!')
        else:
            # Activate
            newsletter.is_active = True
            newsletter.unsubscribed_at = None
            newsletter.save()
            messages.success(request, f'Đã kích hoạt lại đăng ký của {newsletter.email}!')
        
        return redirect('reports:newsletter_list')


class NewsletterDeleteView(AdminRequiredMixin, DeleteView):
    """Xóa đăng ký nhận tin"""
    from products.models import Newsletter
    model = Newsletter
    success_url = reverse_lazy('reports:newsletter_list')
    
    def get_queryset(self):
        from products.models import Newsletter
        return Newsletter.objects.all()
    
    def delete(self, request, *args, **kwargs):
        newsletter = self.get_object()
        email = newsletter.email
        messages.success(request, f'Đã xóa đăng ký của {email}!')
        return super().delete(request, *args, **kwargs)
