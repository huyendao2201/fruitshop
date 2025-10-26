from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # API Endpoints for Charts
    path('api/revenue-chart/', views.RevenueChartAPIView.as_view(), name='revenue_chart_api'),
    path('api/daily-revenue/', views.DailyRevenueAPIView.as_view(), name='daily_revenue_api'),
    path('api/product-stats/', views.ProductStatsAPIView.as_view(), name='product_stats_api'),
    path('api/order-status/', views.OrderStatusAPIView.as_view(), name='order_status_api'),
    path('api/quick-stats/', views.QuickStatsAPIView.as_view(), name='quick_stats_api'),
    
    # Export Reports
    path('export/', views.ExportReportView.as_view(), name='export_report'),
    
    # Product Management
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    
    # Order Management
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/update-status/', views.OrderUpdateStatusView.as_view(), name='order_update_status'),
    
    # Customer Management
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    
    # Category Management
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # Review Management
    path('reviews/', views.ReviewListView.as_view(), name='review_list'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
    
    # Product Image Management
    path('products/<int:product_id>/images/', views.ProductImageManageView.as_view(), name='product_images'),
    path('product-images/<int:image_id>/delete/', views.ProductImageDeleteView.as_view(), name='product_image_delete'),
    path('product-images/<int:image_id>/set-primary/', views.ProductImageSetPrimaryView.as_view(), name='product_image_set_primary'),
    
    # Advanced Analytics
    path('analytics/advanced/', views.AdvancedAnalyticsView.as_view(), name='advanced_analytics'),
    
    # Delivery Management
    path('deliveries/', views.DeliveryListView.as_view(), name='delivery_list'),
    path('deliveries/<int:pk>/', views.DeliveryDetailView.as_view(), name='delivery_detail'),
    path('deliveries/<int:pk>/assign/', views.DeliveryAssignView.as_view(), name='delivery_assign'),
    path('deliveries/<int:pk>/update-status/', views.DeliveryUpdateStatusView.as_view(), name='delivery_update_status'),
    path('deliveries/<int:pk>/add-tracking/', views.DeliveryAddTrackingView.as_view(), name='delivery_add_tracking'),
    
    # Delivery Person Management
    path('delivery-persons/', views.DeliveryPersonListView.as_view(), name='delivery_person_list'),
    path('delivery-persons/<int:pk>/', views.DeliveryPersonDetailView.as_view(), name='delivery_person_detail'),
    
    # User Management (All Roles)
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/add/', views.UserCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('users/<int:pk>/toggle-active/', views.UserToggleActiveView.as_view(), name='user_toggle_active'),
    path('users/<int:pk>/reset-password/', views.UserResetPasswordView.as_view(), name='user_reset_password'),
    
    # Discount Management
    path('discounts/', views.DiscountListView.as_view(), name='discount_list'),
    path('discounts/<int:pk>/', views.DiscountDetailView.as_view(), name='discount_detail'),
    path('discounts/add/', views.DiscountCreateView.as_view(), name='discount_add'),
    path('discounts/<int:pk>/edit/', views.DiscountUpdateView.as_view(), name='discount_edit'),
    path('discounts/<int:pk>/delete/', views.DiscountDeleteView.as_view(), name='discount_delete'),
    path('discounts/<int:pk>/toggle-active/', views.DiscountToggleActiveView.as_view(), name='discount_toggle_active'),
    
    # Shop Review Management
    path('shop-reviews/', views.ShopReviewListView.as_view(), name='shop_review_list'),
    path('shop-reviews/<int:pk>/', views.ShopReviewDetailView.as_view(), name='shop_review_detail'),
    path('shop-reviews/<int:pk>/delete/', views.ShopReviewDeleteView.as_view(), name='shop_review_delete'),
    path('shop-reviews/<int:pk>/toggle-approval/', views.ShopReviewToggleApprovalView.as_view(), name='shop_review_toggle_approval'),
    path('shop-reviews/<int:pk>/toggle-featured/', views.ShopReviewToggleFeaturedView.as_view(), name='shop_review_toggle_featured'),
    path('shop-reviews/<int:pk>/toggle-verified/', views.ShopReviewToggleVerifiedView.as_view(), name='shop_review_toggle_verified'),
    
    # Newsletter Management
    path('newsletters/', views.NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletters/<int:pk>/', views.NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('newsletters/<int:pk>/toggle-active/', views.NewsletterToggleActiveView.as_view(), name='newsletter_toggle_active'),
    path('newsletters/<int:pk>/delete/', views.NewsletterDeleteView.as_view(), name='newsletter_delete'),
]