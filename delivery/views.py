from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Count, Avg, F
from django.views.decorators.http import require_POST
from datetime import timedelta

from .models import Delivery, DeliveryPerson, DeliveryTracking, DeliveryZone
from orders.models import Order
from .forms import (
    DeliveryAssignmentForm, DeliveryStatusUpdateForm, DeliveryProofForm,
    CustomerRatingForm, DeliverySearchForm
)


def is_staff_or_admin(user):
    """Kiểm tra user là staff hoặc admin"""
    return user.is_staff or user.is_superuser


def is_delivery_person(user):
    """Kiểm tra user là nhân viên giao hàng"""
    # Check both DeliveryPerson model and Shipper group
    return hasattr(user, 'delivery_person') or user.groups.filter(name='Shipper').exists()


# ==================== ADMIN/STAFF VIEWS ====================

@login_required
@user_passes_test(is_staff_or_admin)
def delivery_dashboard(request):
    """Dashboard quản lý giao hàng"""
    # Thống kê tổng quan
    today = timezone.now().date()
    
    stats = {
        'total_pending': Delivery.objects.filter(status='pending').count(),
        'total_assigned': Delivery.objects.filter(status='assigned').count(),
        'total_in_transit': Delivery.objects.filter(status__in=['picked_up', 'in_transit']).count(),
        'total_delivered_today': Delivery.objects.filter(
            status='delivered',
            delivered_at__date=today
        ).count(),
        'total_failed_today': Delivery.objects.filter(
            status='failed',
            updated_at__date=today
        ).count(),
    }
    
    # Đơn hàng cần phân công
    pending_deliveries = Delivery.objects.filter(status='pending').select_related(
        'order', 'order__user'
    )[:10]
    
    # Đơn hàng đang giao
    active_deliveries = Delivery.objects.filter(
        status__in=['assigned', 'picked_up', 'in_transit']
    ).select_related('order', 'delivery_person', 'delivery_person__user')[:10]
    
    # Nhân viên giao hàng
    delivery_persons = DeliveryPerson.objects.filter(is_active=True).annotate(
        active_deliveries=Count('deliveries', filter=Q(
            deliveries__status__in=['assigned', 'picked_up', 'in_transit']
        ))
    )
    
    # Đơn hàng bị trễ
    delayed_deliveries = Delivery.objects.filter(
        status__in=['assigned', 'picked_up', 'in_transit'],
        estimated_delivery_time__lt=timezone.now()
    ).select_related('order', 'delivery_person')
    
    context = {
        'stats': stats,
        'pending_deliveries': pending_deliveries,
        'active_deliveries': active_deliveries,
        'delivery_persons': delivery_persons,
        'delayed_deliveries': delayed_deliveries,
    }
    
    return render(request, 'delivery/dashboard.html', context)


@login_required
@user_passes_test(is_staff_or_admin)
def delivery_list(request):
    """Danh sách tất cả đơn giao hàng"""
    deliveries = Delivery.objects.select_related(
        'order', 'order__user', 'delivery_person', 'delivery_person__user'
    ).prefetch_related('order__items').order_by('-created_at')
    
    # Search filter
    search = request.GET.get('search', '')
    if search:
        deliveries = deliveries.filter(
            Q(order__order_number__icontains=search) |
            Q(order__user__username__icontains=search) |
            Q(order__user__email__icontains=search) |
            Q(recipient_name__icontains=search) |
            Q(recipient_phone__icontains=search)
        )
    
    # Status filter
    status = request.GET.get('status', '')
    if status:
        deliveries = deliveries.filter(status=status)
    
    # Delivery person filter
    delivery_person_id = request.GET.get('delivery_person', '')
    if delivery_person_id:
        deliveries = deliveries.filter(delivery_person_id=delivery_person_id)
    
    # Date range filter
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    if start_date:
        deliveries = deliveries.filter(created_at__date__gte=start_date)
    if end_date:
        deliveries = deliveries.filter(created_at__date__lte=end_date)
    
    # Statistics
    total_count = deliveries.count()
    pending_count = deliveries.filter(status='pending').count()
    active_count = deliveries.filter(status__in=['assigned', 'picked_up', 'in_transit']).count()
    completed_count = deliveries.filter(status='delivered').count()
    failed_count = deliveries.filter(status='failed').count()
    
    context = {
        'deliveries': deliveries,
        'status_choices': Delivery.STATUS_CHOICES,
        'delivery_persons': DeliveryPerson.objects.filter(is_active=True).select_related('user'),
        'total_count': total_count,
        'pending_count': pending_count,
        'active_count': active_count,
        'completed_count': completed_count,
        'failed_count': failed_count,
    }
    
    return render(request, 'admin_dashboard/delivery_list.html', context)


@login_required
@user_passes_test(is_staff_or_admin)
def delivery_assign(request, delivery_id):
    """Phân công giao hàng"""
    delivery = get_object_or_404(Delivery, id=delivery_id)
    
    if request.method == 'POST':
        form = DeliveryAssignmentForm(request.POST, instance=delivery)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery_person = form.cleaned_data['delivery_person']
            delivery.assign_to_person(delivery_person)
            
            # Check if email was sent
            if delivery_person.user.email:
                messages.success(
                    request, 
                    f'Đã phân công đơn hàng cho {delivery_person.user.get_full_name()} và gửi email thông báo!'
                )
            else:
                messages.success(
                    request, 
                    f'Đã phân công đơn hàng cho {delivery_person.user.get_full_name()}!'
                )
                messages.warning(
                    request,
                    'Không thể gửi email vì nhân viên chưa có địa chỉ email.'
                )
            return redirect('delivery:dashboard')
    else:
        form = DeliveryAssignmentForm(instance=delivery)
    
    context = {
        'form': form,
        'delivery': delivery,
    }
    
    return render(request, 'delivery/assign.html', context)


@login_required
@user_passes_test(is_staff_or_admin)
def delivery_detail(request, delivery_id):
    """Chi tiết đơn giao hàng"""
    delivery = get_object_or_404(
        Delivery.objects.select_related('order', 'delivery_person', 'delivery_person__user'),
        id=delivery_id
    )
    
    tracking_logs = delivery.tracking_logs.select_related('created_by').all()
    
    context = {
        'delivery': delivery,
        'tracking_logs': tracking_logs,
    }
    
    return render(request, 'delivery/detail.html', context)


# ==================== DELIVERY PERSON VIEWS ====================

@login_required
@user_passes_test(is_delivery_person)
def my_deliveries(request):
    """Danh sách đơn hàng của nhân viên giao hàng"""
    delivery_person = request.user.delivery_person
    
    # Đơn hàng hiện tại
    active_deliveries = delivery_person.deliveries.filter(
        status__in=['assigned', 'picked_up', 'in_transit']
    ).select_related('order')
    
    # Lịch sử giao hàng
    completed_deliveries = delivery_person.deliveries.filter(
        status__in=['delivered', 'failed', 'returned']
    ).select_related('order')[:20]
    
    context = {
        'delivery_person': delivery_person,
        'active_deliveries': active_deliveries,
        'completed_deliveries': completed_deliveries,
    }
    
    return render(request, 'delivery/my_deliveries.html', context)


@login_required
@user_passes_test(is_delivery_person)
def delivery_update_status(request, delivery_id):
    """Cập nhật trạng thái giao hàng"""
    delivery = get_object_or_404(Delivery, id=delivery_id, delivery_person=request.user.delivery_person)
    
    if request.method == 'POST':
        form = DeliveryStatusUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            status = form.cleaned_data['status']
            message = form.cleaned_data.get('message', '')
            location_name = form.cleaned_data.get('location_name', '')
            image = form.cleaned_data.get('image')
            
            # Cập nhật trạng thái
            if status == 'picked_up':
                delivery.mark_picked_up(request.user)
            elif status == 'in_transit':
                delivery.mark_in_transit(request.user)
            elif status == 'delivered':
                delivery.mark_delivered(request.user, image)
            elif status == 'failed':
                failure_reason = form.cleaned_data.get('failure_reason', 'Không rõ lý do')
                delivery.mark_failed(failure_reason, request.user)
            
            # Tạo tracking log nếu có message
            if message:
                DeliveryTracking.objects.create(
                    delivery=delivery,
                    status=status,
                    message=message,
                    location_name=location_name,
                    image=image,
                    created_by=request.user
                )
            
            messages.success(request, 'Đã cập nhật trạng thái giao hàng')
            return redirect('delivery:my_deliveries')
    else:
        form = DeliveryStatusUpdateForm()
    
    context = {
        'form': form,
        'delivery': delivery,
    }
    
    return render(request, 'delivery/update_status.html', context)


@login_required
@user_passes_test(is_delivery_person)
def delivery_mark_delivered(request, delivery_id):
    """Xác nhận giao hàng thành công"""
    delivery = get_object_or_404(Delivery, id=delivery_id, delivery_person=request.user.delivery_person)
    
    if request.method == 'POST':
        form = DeliveryProofForm(request.POST, request.FILES)
        if form.is_valid():
            proof_image = form.cleaned_data['proof_image']
            notes = form.cleaned_data.get('notes', '')
            
            delivery.mark_delivered(request.user, proof_image)
            
            if notes:
                DeliveryTracking.objects.create(
                    delivery=delivery,
                    status='delivered',
                    message=notes,
                    location_name=delivery.delivery_address,
                    created_by=request.user
                )
            
            messages.success(request, 'Đã xác nhận giao hàng thành công!')
            return redirect('delivery:my_deliveries')
    else:
        form = DeliveryProofForm()
    
    context = {
        'form': form,
        'delivery': delivery,
    }
    
    return render(request, 'delivery/mark_delivered.html', context)


# ==================== CUSTOMER VIEWS ====================

@login_required
def customer_track_delivery(request, order_id):
    """Khách hàng theo dõi đơn hàng"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    try:
        delivery = order.delivery
        tracking_logs = delivery.tracking_logs.select_related('created_by').all()
    except Delivery.DoesNotExist:
        delivery = None
        tracking_logs = []
    
    context = {
        'order': order,
        'delivery': delivery,
        'tracking_logs': tracking_logs,
    }
    
    return render(request, 'delivery/customer_tracking.html', context)


@login_required
def customer_rate_delivery(request, delivery_id):
    """Khách hàng đánh giá dịch vụ giao hàng"""
    delivery = get_object_or_404(Delivery, id=delivery_id, order__user=request.user)
    
    if delivery.status != 'delivered':
        messages.error(request, 'Chỉ có thể đánh giá sau khi đơn hàng được giao thành công')
        return redirect('orders:order_detail', pk=delivery.order.id)
    
    if request.method == 'POST':
        form = CustomerRatingForm(request.POST, instance=delivery)
        if form.is_valid():
            form.save()
            
            # Cập nhật rating của nhân viên giao hàng
            if delivery.delivery_person:
                person = delivery.delivery_person
                avg_rating = person.deliveries.filter(
                    customer_rating__isnull=False
                ).aggregate(Avg('customer_rating'))['customer_rating__avg']
                
                if avg_rating:
                    person.rating = round(avg_rating, 2)
                    person.save()
            
            messages.success(request, 'Cảm ơn bạn đã đánh giá!')
            return redirect('orders:order_detail', pk=delivery.order.id)
    else:
        form = CustomerRatingForm(instance=delivery)
    
    context = {
        'form': form,
        'delivery': delivery,
    }
    
    return render(request, 'delivery/rate_delivery.html', context)


# ==================== API ENDPOINTS ====================

@login_required
def api_delivery_status(request, delivery_id):
    """API lấy trạng thái giao hàng (real-time)"""
    delivery = get_object_or_404(Delivery, id=delivery_id)
    
    # Kiểm tra quyền truy cập
    if not (request.user.is_staff or 
            request.user == delivery.order.user or 
            (hasattr(request.user, 'delivery_person') and 
             request.user.delivery_person == delivery.delivery_person)):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    # Lấy tracking logs mới nhất
    latest_logs = delivery.tracking_logs.select_related('created_by').order_by('-created_at')[:5]
    
    data = {
        'status': delivery.status,
        'status_display': delivery.get_status_display(),
        'is_delayed': delivery.is_delayed,
        'current_location': {
            'latitude': float(delivery.current_latitude) if delivery.current_latitude else None,
            'longitude': float(delivery.current_longitude) if delivery.current_longitude else None,
        },
        'tracking_logs': [
            {
                'status': log.status,
                'message': log.message,
                'location': log.location_name,
                'time': log.created_at.isoformat(),
                'created_by': log.created_by.get_full_name() if log.created_by else 'System',
            }
            for log in latest_logs
        ],
        'delivery_person': {
            'name': delivery.delivery_person.user.get_full_name() if delivery.delivery_person else None,
            'phone': delivery.delivery_person.phone if delivery.delivery_person else None,
        } if delivery.delivery_person else None,
        'estimated_delivery': delivery.estimated_delivery_time.isoformat() if delivery.estimated_delivery_time else None,
    }
    
    return JsonResponse(data)


@login_required
@user_passes_test(is_delivery_person)
@require_POST
def api_update_location(request, delivery_id):
    """API cập nhật vị trí hiện tại"""
    delivery = get_object_or_404(Delivery, id=delivery_id, delivery_person=request.user.delivery_person)
    
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    
    if latitude and longitude:
        delivery.current_latitude = latitude
        delivery.current_longitude = longitude
        delivery.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Invalid coordinates'}, status=400)


# ==================== STATISTICS ====================

@login_required
@user_passes_test(is_staff_or_admin)
def delivery_statistics(request):
    """Thống kê hiệu quả giao hàng"""
    # Thời gian
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Thống kê tổng quan
    total_deliveries = Delivery.objects.count()
    successful_deliveries = Delivery.objects.filter(status='delivered').count()
    failed_deliveries = Delivery.objects.filter(status='failed').count()
    success_rate = (successful_deliveries / total_deliveries * 100) if total_deliveries > 0 else 0
    
    # Thống kê theo thời gian
    week_stats = {
        'total': Delivery.objects.filter(created_at__date__gte=week_ago).count(),
        'delivered': Delivery.objects.filter(status='delivered', delivered_at__date__gte=week_ago).count(),
        'failed': Delivery.objects.filter(status='failed', updated_at__date__gte=week_ago).count(),
    }
    
    month_stats = {
        'total': Delivery.objects.filter(created_at__date__gte=month_ago).count(),
        'delivered': Delivery.objects.filter(status='delivered', delivered_at__date__gte=month_ago).count(),
        'failed': Delivery.objects.filter(status='failed', updated_at__date__gte=month_ago).count(),
    }
    
    # Thống kê theo nhân viên
    person_stats = DeliveryPerson.objects.annotate(
        total=Count('deliveries'),
        delivered=Count('deliveries', filter=Q(deliveries__status='delivered')),
        failed=Count('deliveries', filter=Q(deliveries__status='failed')),
    ).filter(total__gt=0).order_by('-delivered')
    
    # Thời gian giao hàng trung bình
    avg_delivery_time = Delivery.objects.filter(
        status='delivered',
        picked_up_at__isnull=False,
        delivered_at__isnull=False
    ).annotate(
        duration=F('delivered_at') - F('picked_up_at')
    ).aggregate(Avg('duration'))
    
    context = {
        'total_deliveries': total_deliveries,
        'successful_deliveries': successful_deliveries,
        'failed_deliveries': failed_deliveries,
        'success_rate': round(success_rate, 2),
        'week_stats': week_stats,
        'month_stats': month_stats,
        'person_stats': person_stats,
        'avg_delivery_time': avg_delivery_time['duration__avg'],
    }
    
    return render(request, 'delivery/statistics.html', context)
