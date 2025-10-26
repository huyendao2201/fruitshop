"""
URL configuration for fruitshop project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products.views import HomeView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('reports/', include('reports.urls')),
    path('delivery/', include('delivery.urls')),
]

# Custom error handlers
handler404 = 'fruitshop.views.custom_404'
handler500 = 'fruitshop.views.custom_500'

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    
    # Add test routes for error pages (only in DEBUG mode)
    urlpatterns += [
        path('test-404/', TemplateView.as_view(template_name='404.html'), name='test_404'),
        path('test-500/', TemplateView.as_view(template_name='500.html'), name='test_500'),
    ]