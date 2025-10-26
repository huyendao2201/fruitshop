from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    # Admin/Staff URLs
    path('dashboard/', views.delivery_dashboard, name='dashboard'),
    path('list/', views.delivery_list, name='list'),
    path('<int:delivery_id>/', views.delivery_detail, name='detail'),
    path('<int:delivery_id>/assign/', views.delivery_assign, name='assign'),
    path('statistics/', views.delivery_statistics, name='statistics'),
    
    # Delivery Person URLs
    path('my-deliveries/', views.my_deliveries, name='my_deliveries'),
    path('<int:delivery_id>/update-status/', views.delivery_update_status, name='update_status'),
    path('<int:delivery_id>/mark-delivered/', views.delivery_mark_delivered, name='mark_delivered'),
    
    # Customer URLs
    path('track/<int:order_id>/', views.customer_track_delivery, name='customer_track'),
    path('<int:delivery_id>/rate/', views.customer_rate_delivery, name='rate'),
    
    # API URLs
    path('api/<int:delivery_id>/status/', views.api_delivery_status, name='api_status'),
    path('api/<int:delivery_id>/update-location/', views.api_update_location, name='api_update_location'),
]
















