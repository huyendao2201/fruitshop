from django import forms
from .models import Delivery, DeliveryTracking, DeliveryPerson


class DeliveryAssignmentForm(forms.ModelForm):
    """Form phân công giao hàng"""
    
    class Meta:
        model = Delivery
        fields = ['delivery_person', 'estimated_delivery_time', 'notes']
        widgets = {
            'delivery_person': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'estimated_delivery_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ghi chú cho nhân viên giao hàng...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Chỉ hiển thị nhân viên đang hoạt động
        self.fields['delivery_person'].queryset = DeliveryPerson.objects.filter(is_active=True)
        self.fields['delivery_person'].label = 'Nhân viên giao hàng'
        self.fields['estimated_delivery_time'].label = 'Thời gian giao dự kiến'
        self.fields['notes'].label = 'Ghi chú'


class DeliveryStatusUpdateForm(forms.Form):
    """Form cập nhật trạng thái giao hàng"""
    STATUS_CHOICES = [
        ('picked_up', 'Đã lấy hàng'),
        ('in_transit', 'Đang giao'),
        ('delivered', 'Đã giao thành công'),
        ('failed', 'Giao thất bại'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Trạng thái'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Mô tả chi tiết...'
        }),
        label='Ghi chú',
        required=False
    )
    location_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Vị trí hiện tại...'
        }),
        label='Địa điểm',
        required=False
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        label='Hình ảnh',
        required=False
    )
    
    # Cho trạng thái failed
    failure_reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Lý do giao hàng thất bại...'
        }),
        label='Lý do thất bại',
        required=False
    )


class DeliveryProofForm(forms.Form):
    """Form xác nhận giao hàng thành công"""
    proof_image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'capture': 'camera'  # Mở camera trên mobile
        }),
        label='Ảnh xác nhận giao hàng',
        required=True
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ghi chú khi giao hàng...'
        }),
        label='Ghi chú',
        required=False
    )
    recipient_signature = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tên người nhận hàng'
        }),
        label='Người nhận hàng',
        required=False
    )


class CustomerRatingForm(forms.ModelForm):
    """Form đánh giá của khách hàng"""
    
    class Meta:
        model = Delivery
        fields = ['customer_rating', 'customer_feedback']
        widgets = {
            'customer_rating': forms.RadioSelect(
                choices=[(i, '⭐' * i) for i in range(1, 6)],
                attrs={'class': 'rating-radio'}
            ),
            'customer_feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Chia sẻ trải nghiệm của bạn về dịch vụ giao hàng...'
            }),
        }
        labels = {
            'customer_rating': 'Đánh giá dịch vụ giao hàng',
            'customer_feedback': 'Nhận xét của bạn'
        }


class DeliveryPersonForm(forms.ModelForm):
    """Form quản lý nhân viên giao hàng"""
    
    class Meta:
        model = DeliveryPerson
        fields = ['phone', 'vehicle_type', 'vehicle_number', 'is_active']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0123456789'
            }),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'vehicle_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '29A-12345'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DeliverySearchForm(forms.Form):
    """Form tìm kiếm đơn giao hàng"""
    order_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mã đơn hàng...'
        }),
        label='Mã đơn hàng',
        required=False
    )
    status = forms.ChoiceField(
        choices=[('', 'Tất cả')] + list(Delivery.STATUS_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Trạng thái',
        required=False
    )
    delivery_person = forms.ModelChoiceField(
        queryset=DeliveryPerson.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Nhân viên giao hàng',
        required=False,
        empty_label='Tất cả'
    )
    date_from = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Từ ngày',
        required=False
    )
    date_to = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Đến ngày',
        required=False
    )
















