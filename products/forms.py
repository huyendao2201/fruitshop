from django import forms
from .models import Review, Product, ShopReview, Newsletter


class ReviewForm(forms.ModelForm):
    """Form để gửi đánh giá sản phẩm"""
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} Sao') for i in range(1, 6)],
                attrs={'class': 'form-select'}
            ),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tóm tắt đánh giá của bạn'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Chia sẻ trải nghiệm của bạn về sản phẩm này...'
            }),
        }
        labels = {
            'rating': 'Đánh giá của bạn',
            'title': 'Tiêu đề đánh giá',
            'comment': 'Nội dung đánh giá',
        }


class ShopReviewForm(forms.ModelForm):
    """Form để gửi đánh giá cửa hàng"""
    class Meta:
        model = ShopReview
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.HiddenInput(),  # Sẽ dùng star rating UI
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tiêu đề đánh giá của bạn',
                'required': True
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Chia sẻ trải nghiệm của bạn về cửa hàng...',
                'required': True
            }),
        }
        labels = {
            'rating': 'Đánh giá của bạn',
            'title': 'Tiêu đề',
            'comment': 'Nội dung đánh giá',
        }


class ProductSearchForm(forms.Form):
    """Form tìm kiếm sản phẩm nâng cao"""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tìm kiếm trái cây...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='Tất Cả Danh Mục',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Giá Tối Thiểu'
        })
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Giá Tối Đa'
        })
    )
    in_stock = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Mặc Định'),
            ('name', 'Tên (A-Z)'),
            ('-name', 'Tên (Z-A)'),
            ('price', 'Giá (Thấp đến Cao)'),
            ('-price', 'Giá (Cao đến Thấp)'),
            ('-created_at', 'Mới Nhất'),
            ('created_at', 'Cũ Nhất'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Category
        self.fields['category'].queryset = Category.objects.filter(is_active=True)


class NewsletterForm(forms.ModelForm):
    """Form đăng ký nhận tin"""
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập địa chỉ email của bạn',
                'required': True
            }),
        }
        labels = {
            'email': '',  # Không hiển thị label
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Kiểm tra xem email đã đăng ký chưa
        if Newsletter.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError('Email này đã được đăng ký nhận tin.')
        return email

