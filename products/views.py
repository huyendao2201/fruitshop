from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from .models import Product, Category, Review, Wishlist, ProductImage, ShopReview, Newsletter
from .forms import ReviewForm, ProductSearchForm, ShopReviewForm, NewsletterForm
from .utils import search_products, get_featured_products, get_new_products, get_bestsellers, get_related_products


class HomeView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        """Thêm danh mục và sản phẩm nổi bật vào context"""
        context = super().get_context_data(**kwargs)
        # Sử dụng @property product_count đã có từ Category model
        context['categories'] = Category.objects.filter(is_active=True)[:8]
        context['featured_products'] = Product.objects.filter(
            is_active=True
        ).select_related('category')[:12]
        
        # Lấy đánh giá cửa hàng (hiển thị tối đa 6 reviews)
        context['shop_reviews'] = ShopReview.objects.filter(
            is_approved=True
        ).select_related('user').order_by('-created_at')[:6]
        
        # Thêm danh sách wishlist cho người dùng hiện tại
        if self.request.user.is_authenticated:
            wishlist_product_ids = Wishlist.objects.filter(
                user=self.request.user
            ).values_list('product_id', flat=True)
            context['user_wishlist_ids'] = list(wishlist_product_ids)
            
            # Kiểm tra user đã mua hàng chưa (để hiển thị nút viết review)
            # Chấp nhận cả 'delivered' (đã giao hàng) và 'completed' (hoàn thành)
            from orders.models import Order
            has_purchased = Order.objects.filter(
                user=self.request.user,
                status__in=['delivered', 'completed']
            ).exists()
            context['has_purchased'] = has_purchased
            
            # Kiểm tra đã review cửa hàng chưa
            has_reviewed = ShopReview.objects.filter(
                user=self.request.user
            ).exists()
            context['has_reviewed'] = has_reviewed
        else:
            context['user_wishlist_ids'] = []
            context['has_purchased'] = False
            context['has_reviewed'] = False
        
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        """Lấy danh sách sản phẩm với các bộ lọc tìm kiếm"""
        form = ProductSearchForm(self.request.GET)
        
        if form.is_valid():
            query = form.cleaned_data.get('query')
            category = form.cleaned_data.get('category')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            in_stock = form.cleaned_data.get('in_stock')
            sort_by = form.cleaned_data.get('sort_by')
            
            queryset = search_products(
                query=query,
                category=category,
                min_price=min_price,
                max_price=max_price,
                in_stock=in_stock,
                sort_by=sort_by
            )
        else:
            queryset = Product.objects.filter(is_active=True).order_by('-created_at')
        
        # Xử lý category từ URL (sử dụng slug thay vì ID)
        category_slug = self.kwargs.get('slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        """Thêm danh mục và form tìm kiếm vào context"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['search_form'] = ProductSearchForm(self.request.GET)
        
        category_slug = self.kwargs.get('slug')
        if category_slug:
            context['current_category'] = get_object_or_404(Category, slug=category_slug)
        
        # Thêm danh sách wishlist cho người dùng hiện tại
        if self.request.user.is_authenticated:
            wishlist_product_ids = Wishlist.objects.filter(
                user=self.request.user
            ).values_list('product_id', flat=True)
            context['user_wishlist_ids'] = list(wishlist_product_ids)
        else:
            context['user_wishlist_ids'] = []
        
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        """Lấy sản phẩm đang hoạt động kèm theo hình ảnh và đánh giá"""
        return Product.objects.filter(is_active=True).prefetch_related('images', 'reviews')
    
    def get_context_data(self, **kwargs):
        """Thêm sản phẩm liên quan, hình ảnh, và đánh giá vào context"""
        context = super().get_context_data(**kwargs)
        product = self.object
        
        # Sản phẩm liên quan
        context['related_products'] = get_related_products(product, 4)
        
        # Hình ảnh sản phẩm
        context['product_images'] = product.images.all()
        
        # Đánh giá
        context['reviews'] = product.reviews.filter(is_approved=True).order_by('-created_at')[:10]
        context['review_form'] = ReviewForm()
        
        # Kiểm tra người dùng đã mua sản phẩm này chưa
        if self.request.user.is_authenticated:
            from orders.models import OrderItem
            has_purchased = OrderItem.objects.filter(
                order__user=self.request.user,
                product=product,
                order__status__in=['delivered', 'completed']
            ).exists()
            context['has_purchased'] = has_purchased
            
            # Kiểm tra người dùng đã đánh giá chưa
            has_reviewed = Review.objects.filter(
                user=self.request.user,
                product=product
            ).exists()
            context['has_reviewed'] = has_reviewed
            
            # Kiểm tra có trong wishlist không
            in_wishlist = Wishlist.objects.filter(
                user=self.request.user,
                product=product
            ).exists()
            context['in_wishlist'] = in_wishlist
        
        return context


class AddReviewView(LoginRequiredMixin, View):
    """Thêm đánh giá sản phẩm"""
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        
        # Kiểm tra người dùng đã đánh giá chưa
        if Review.objects.filter(user=request.user, product=product).exists():
            messages.error(request, 'Bạn đã đánh giá sản phẩm này rồi.')
            return redirect('products:product_detail', slug=slug)
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            
            # Kiểm tra đã mua hàng chưa
            from orders.models import OrderItem
            has_purchased = OrderItem.objects.filter(
                order__user=request.user,
                product=product,
                order__status__in=['delivered', 'completed']
            ).exists()
            review.is_verified_purchase = has_purchased
            
            review.save()
            messages.success(request, 'Cảm ơn bạn đã đánh giá!')
        else:
            messages.error(request, 'Vui lòng sửa các lỗi trong đánh giá của bạn.')
        
        return redirect('products:product_detail', slug=slug)


class ToggleWishlistView(LoginRequiredMixin, View):
    """Thêm/xóa sản phẩm khỏi wishlist"""
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if created:
            message = f'{product.name} đã được thêm vào danh sách yêu thích!'
            in_wishlist = True
        else:
            wishlist_item.delete()
            message = f'{product.name} đã được xóa khỏi danh sách yêu thích!'
            in_wishlist = False
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'in_wishlist': in_wishlist,
                'message': message
            })
        
        messages.success(request, message)
        return redirect('products:product_detail', slug=slug)


class WishlistView(LoginRequiredMixin, ListView):
    """Xem danh sách yêu thích của người dùng"""
    model = Wishlist
    template_name = 'products/wishlist.html'
    context_object_name = 'wishlist_items'
    paginate_by = 12
    
    def get_queryset(self):
        """Lấy danh sách wishlist của người dùng hiện tại"""
        return Wishlist.objects.filter(user=self.request.user).select_related('product')


class AddShopReviewView(LoginRequiredMixin, View):
    """Thêm đánh giá cửa hàng"""
    def post(self, request):
        # Kiểm tra người dùng đã đánh giá chưa
        if ShopReview.objects.filter(user=request.user).exists():
            messages.error(request, 'Bạn đã đánh giá cửa hàng rồi.')
            return redirect('home')
        
        # Kiểm tra đã mua hàng chưa
        # Chấp nhận cả 'delivered' (đã giao hàng) và 'completed' (hoàn thành)
        from orders.models import Order
        has_purchased = Order.objects.filter(
            user=request.user,
            status__in=['delivered', 'completed']
        ).exists()
        
        if not has_purchased:
            messages.error(request, 'Chỉ khách hàng đã từng mua hàng mới có thể đánh giá.')
            return redirect('home')
        
        form = ShopReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.is_verified_purchase = True
            review.save()
            messages.success(request, 'Cảm ơn bạn đã đánh giá cửa hàng của chúng tôi!')
        else:
            messages.error(request, 'Vui lòng sửa các lỗi trong đánh giá của bạn.')
        
        return redirect('home')


class CategoryListView(ListView):
    """Danh sách tất cả các danh mục"""
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        """Lấy các danh mục đang hoạt động"""
        return Category.objects.filter(is_active=True)


class NewsletterSubscribeView(View):
    """Đăng ký nhận tin qua email"""
    
    def post(self, request):
        form = NewsletterForm(request.POST)
        
        if form.is_valid():
            try:
                newsletter = form.save()
                messages.success(
                    request,
                    f'Cảm ơn bạn đã đăng ký! Chúng tôi sẽ gửi tin tức mới nhất đến {newsletter.email}'
                )
            except Exception as e:
                messages.error(
                    request,
                    'Đã có lỗi xảy ra. Vui lòng thử lại sau.'
                )
        else:
            # Lấy lỗi đầu tiên từ form
            error_message = list(form.errors.values())[0][0] if form.errors else 'Email không hợp lệ.'
            messages.error(request, error_message)
        
        # Redirect về trang trước đó hoặc trang chủ
        return redirect(request.META.get('HTTP_REFERER', 'home'))
