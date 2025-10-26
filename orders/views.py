from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from products.models import Product
from .models import Order, OrderItem, OrderTracking
from .forms import CheckoutForm, DiscountCodeForm
from .utils import (
    get_cart_items, get_cart_count, add_to_cart, update_cart, 
    remove_from_cart, clear_cart, validate_discount_code, 
    calculate_shipping_fee, send_order_confirmation_email
)
from .vnpay import VNPay


class CartView(TemplateView):
    template_name = 'orders/cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items, total = get_cart_items(self.request)
        context['cart_items'] = cart_items
        context['cart_total'] = total
        context['cart_count'] = get_cart_count(self.request)
        return context


class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_active=True)
        quantity = int(request.POST.get('quantity', 1))
        
        if product.stock < quantity:
            messages.error(request, f'Xin lỗi, chỉ còn {product.stock} sản phẩm trong kho.')
            return redirect('products:product_detail', slug=product.slug)
        
        add_to_cart(request, product_id, quantity)
        messages.success(request, f'Đã thêm {product.name} vào giỏ hàng!')
        
        # AJAX response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': get_cart_count(request),
                'message': f'Đã thêm {product.name} vào giỏ hàng!'
            })
        
        return redirect('orders:cart')


class RemoveFromCartView(View):
    def post(self, request, product_id):
        remove_from_cart(request, product_id)
        messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng!')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            cart_items, total = get_cart_items(request)
            return JsonResponse({
                'success': True,
                'cart_total': float(total),
                'cart_count': get_cart_count(request)
            })
        
        return redirect('orders:cart')


class UpdateCartView(View):
    def post(self, request, product_id):
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        
        if quantity > product.stock:
            messages.error(request, f'Chỉ còn {product.stock} sản phẩm.')
            quantity = product.stock
        
        if quantity > 0:
            update_cart(request, product_id, quantity)
            messages.success(request, 'Đã cập nhật giỏ hàng!')
        else:
            remove_from_cart(request, product_id)
            messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng!')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            cart_items, total = get_cart_items(request)
            return JsonResponse({
                'success': True,
                'cart_total': float(total),
                'cart_count': get_cart_count(request)
            })
        
        return redirect('orders:cart')


class ClearCartView(View):
    """Clear all items from cart"""
    def post(self, request):
        clear_cart(request)
        messages.success(request, 'Đã xóa toàn bộ giỏ hàng!')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': 0,
                'message': 'Đã xóa toàn bộ giỏ hàng!'
            })
        
        return redirect('orders:cart')


class ApplyDiscountView(LoginRequiredMixin, View):
    """Apply discount code to cart"""
    
    def get(self, request):
        # Redirect to checkout if accessed via GET
        messages.warning(request, 'Vui lòng sử dụng form để áp dụng mã giảm giá.')
        return redirect('orders:checkout')
    
    def post(self, request):
        print("=== APPLY DISCOUNT DEBUG ===")
        code = request.POST.get('discount_code', '').strip().upper()
        print(f"Code received: {code}")
        
        # Check where the request came from (cart or checkout)
        referer = request.META.get('HTTP_REFERER', '')
        redirect_to = 'orders:checkout'  # default
        
        if 'cart' in referer:
            redirect_to = 'orders:cart'
        
        if not code:
            messages.error(request, 'Vui lòng nhập mã giảm giá.')
            return redirect(redirect_to)
        
        is_valid, discount, message = validate_discount_code(code, request.user)
        print(f"Validation result - Valid: {is_valid}, Discount: {discount}, Message: {message}")
        
        if is_valid:
            request.session['discount_code'] = code
            request.session['discount_id'] = discount.id
            request.session.modified = True  # Force session save
            print(f"Session updated - discount_code: {request.session.get('discount_code')}, discount_id: {request.session.get('discount_id')}")
            messages.success(request, message)
        else:
            messages.error(request, message)
        
        print("=== END DEBUG ===")
        return redirect(redirect_to)


class RemoveDiscountView(LoginRequiredMixin, View):
    """Remove applied discount code"""
    def get(self, request):
        if 'discount_code' in request.session:
            del request.session['discount_code']
        if 'discount_id' in request.session:
            del request.session['discount_id']
        messages.info(request, 'Đã xóa mã giảm giá.')
        return redirect('orders:checkout')


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/checkout.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items, subtotal = get_cart_items(self.request)
        
        if not cart_items:
            return context
        
        # Calculate shipping
        shipping_fee = calculate_shipping_fee(subtotal)
        
        # Apply discount if exists
        discount = None
        discount_amount = 0
        discount_code = self.request.session.get('discount_code')
        print(f"=== CHECKOUT VIEW DEBUG === discount_code from session: {discount_code}")
        
        if discount_code:
            from products.models import Discount
            from django.contrib import messages
            try:
                discount = Discount.objects.get(code=discount_code, is_active=True)
                is_valid, _, _ = validate_discount_code(discount_code, self.request.user)
                if is_valid and discount.is_valid:
                    # Check min purchase requirement
                    if subtotal >= discount.min_purchase:
                        discount_amount = discount.calculate_discount(subtotal)
                        print(f"Discount applied! Amount: ${discount_amount}")
                    else:
                        # Keep discount in session but show warning
                        min_needed = float(discount.min_purchase - subtotal)
                        messages.warning(
                            self.request,
                            f'Mã giảm giá "{discount_code}" yêu cầu đơn hàng tối thiểu {discount.min_purchase:,.0f}đ. Thêm {min_needed:,.0f}đ nữa để áp dụng mã này.'
                        )
                        discount = None  # Don't show in summary
                else:
                    # Clear invalid discount
                    if 'discount_code' in self.request.session:
                        del self.request.session['discount_code']
                    if 'discount_id' in self.request.session:
                        del self.request.session['discount_id']
                    discount = None
                    messages.error(self.request, f'Mã giảm giá "{discount_code}" không còn hiệu lực.')
            except Discount.DoesNotExist:
                # Clear non-existent discount
                if 'discount_code' in self.request.session:
                    del self.request.session['discount_code']
                if 'discount_id' in self.request.session:
                    del self.request.session['discount_id']
                discount = None
                messages.error(self.request, f'Không tìm thấy mã giảm giá "{discount_code}".')
        
        total = subtotal + shipping_fee - discount_amount
        
        context.update({
            'cart_items': cart_items,
            'subtotal': subtotal,
            'shipping_fee': shipping_fee,
            'discount': discount,
            'discount_amount': discount_amount,
            'total': total,
            'form': CheckoutForm(user=self.request.user),
            'discount_form': DiscountCodeForm()
        })
        
        return context
    
    def post(self, request):
        cart_items, subtotal = get_cart_items(request)
        
        if not cart_items:
            messages.error(request, 'Giỏ hàng của bạn đang trống!')
            return redirect('orders:cart')
        
        form = CheckoutForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Vui lòng sửa các lỗi bên dưới.')
            # Re-render with form errors
            context = self.get_context_data()
            context['form'] = form  # Pass form with errors
            return self.render_to_response(context)
        
        # Calculate totals
        shipping_fee = calculate_shipping_fee(subtotal)
        discount_amount = 0
        discount = None
        
        discount_code = request.session.get('discount_code')
        if discount_code:
            from products.models import Discount
            try:
                discount = Discount.objects.get(code=discount_code, is_active=True)
                is_valid, _, _ = validate_discount_code(discount_code, request.user)
                if is_valid and discount.is_valid and subtotal >= discount.min_purchase:
                    discount_amount = discount.calculate_discount(subtotal)
            except Discount.DoesNotExist:
                discount = None
        
        total = subtotal + shipping_fee - discount_amount
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            shipping_address=form.cleaned_data['shipping_address'],
            phone=form.cleaned_data['phone'],
            email=form.cleaned_data['email'],
            payment_method=form.cleaned_data['payment_method'],
            notes=form.cleaned_data.get('notes', ''),
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            discount_amount=discount_amount,
            discount_code=discount_code if discount_code else '',
            total_amount=total
        )
        
        # Create order items and update stock
        for item in cart_items:
            product = item['product']
            quantity = item['quantity']
            
            if product.stock < quantity:
                messages.error(request, f'Không đủ số lượng cho {product.name}')
                order.delete()
                return redirect('orders:cart')
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=item['price']
            )
            
            # Update stock
            product.stock -= quantity
            product.save()
        
        # Create initial tracking
        OrderTracking.objects.create(
            order=order,
            status='pending',
            message='Order placed successfully',
            created_by=request.user
        )
        
        # Update discount usage
        if discount:
            discount.used_count += 1
            discount.save()
        
        # Clear cart and discount
        clear_cart(request)
        if 'discount_code' in request.session:
            del request.session['discount_code']
        if 'discount_id' in request.session:
            del request.session['discount_id']
        
        # Check payment method
        if form.cleaned_data['payment_method'] == 'vnpay':
            # Redirect to VNPay payment
            return redirect('orders:vnpay_payment', order_id=order.id)
        
        # Send confirmation email for non-VNPay orders
        send_order_confirmation_email(order)
        
        messages.success(request, f'Đặt hàng #{order.order_number} thành công!')
        return redirect('orders:order_detail', order_number=order.order_number)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user).prefetch_related('items__product')
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Order.STATUS_CHOICES
        context['current_status'] = self.request.GET.get('status', '')
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            'items__product', 'tracking'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracking_history'] = self.object.tracking.all().order_by('-created_at')
        return context


class CancelOrderView(LoginRequiredMixin, View):
    """Cancel an order (only if pending/processing)"""
    def post(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        
        if order.status not in ['pending', 'processing']:
            messages.error(request, 'Không thể hủy đơn hàng này.')
            return redirect('orders:order_detail', order_number=order_number)
        
        # Restore stock
        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()
        
        # Update order status
        order.status = 'cancelled'
        order.save()
        
        # Add tracking
        OrderTracking.objects.create(
            order=order,
            status='cancelled',
            message='Order cancelled by customer',
            created_by=request.user
        )
        
        messages.success(request, f'Đã hủy đơn hàng #{order.order_number}.')
        return redirect('orders:order_detail', order_number=order_number)


# ===================================
# VNPAY PAYMENT VIEWS
# ===================================

class VNPayPaymentView(LoginRequiredMixin, View):
    """Initiate VNPay payment"""
    
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        # Check if order is already paid
        if order.payment_status == 'paid':
            messages.warning(request, 'Đơn hàng này đã được thanh toán.')
            return redirect('orders:order_detail', order_number=order.order_number)
        
        # Create VNPay payment URL
        vnpay = VNPay()
        payment_url = vnpay.create_payment_url(order, request)
        
        # Save transaction ID
        order.vnpay_transaction_id = order.order_number
        order.save()
        
        # Redirect to VNPay
        return redirect(payment_url)


class VNPayReturnView(View):
    """Handle VNPay return callback"""
    
    def get(self, request):
        # Get all query parameters
        params = dict(request.GET.items())
        
        # Validate response
        vnpay = VNPay()
        is_valid, response_data = vnpay.validate_response(params)
        
        if not is_valid:
            messages.error(request, 'Phản hồi thanh toán không hợp lệ. Vui lòng liên hệ hỗ trợ.')
            return render(request, 'orders/vnpay_return.html', {
                'success': False,
                'message': 'Chữ ký không hợp lệ',
            })
        
        # Get order
        try:
            order = Order.objects.get(order_number=response_data['order_number'])
        except Order.DoesNotExist:
            messages.error(request, 'Không tìm thấy đơn hàng.')
            return render(request, 'orders/vnpay_return.html', {
                'success': False,
                'message': 'Không tìm thấy đơn hàng',
            })
        
        # Check response code
        response_code = response_data['response_code']
        
        if response_code == '00':
            # Payment successful
            order.payment_status = 'paid'
            order.vnpay_transaction_no = response_data['transaction_no']
            order.vnpay_bank_code = response_data['bank_code']
            order.vnpay_card_type = response_data['card_type']
            order.vnpay_response_code = response_code
            order.vnpay_paid_at = timezone.now()
            order.save()
            
            # Add tracking
            OrderTracking.objects.create(
                order=order,
                status='paid',
                message=f'Thanh toán VNPay thành công. Mã GD: {response_data["transaction_no"]}',
                created_by=order.user
            )
            
            # Send confirmation email
            send_order_confirmation_email(order)
            
            messages.success(request, 'Thanh toán thành công! Đơn hàng của bạn đã được xác nhận.')
            
            return render(request, 'orders/vnpay_return.html', {
                'success': True,
                'order': order,
                'response_data': response_data,
                'message': vnpay.get_response_message(response_code),
            })
        else:
            # Payment failed
            order.payment_status = 'failed'
            order.vnpay_response_code = response_code
            order.save()
            
            # Add tracking
            OrderTracking.objects.create(
                order=order,
                status='failed',
                message=f'Thanh toán VNPay thất bại. Mã lỗi: {response_code}',
                created_by=order.user
            )
            
            messages.error(request, f'Thanh toán thất bại: {vnpay.get_response_message(response_code)}')
            
            return render(request, 'orders/vnpay_return.html', {
                'success': False,
                'order': order,
                'response_data': response_data,
                'message': vnpay.get_response_message(response_code),
            })


@method_decorator(csrf_exempt, name='dispatch')
class VNPayIPNView(View):
    """Handle VNPay IPN (Instant Payment Notification)"""
    
    def get(self, request):
        # Get all query parameters
        params = dict(request.GET.items())
        
        # Validate response
        vnpay = VNPay()
        is_valid, response_data = vnpay.validate_response(params)
        
        if not is_valid:
            return JsonResponse({
                'RspCode': '97',
                'Message': 'Invalid Signature'
            })
        
        # Get order
        try:
            order = Order.objects.get(order_number=response_data['order_number'])
        except Order.DoesNotExist:
            return JsonResponse({
                'RspCode': '01',
                'Message': 'Order not found'
            })
        
        # Check if already processed
        if order.payment_status == 'paid':
            return JsonResponse({
                'RspCode': '02',
                'Message': 'Order already confirmed'
            })
        
        # Check response code
        response_code = response_data['response_code']
        
        if response_code == '00':
            # Payment successful
            order.payment_status = 'paid'
            order.vnpay_transaction_no = response_data['transaction_no']
            order.vnpay_bank_code = response_data['bank_code']
            order.vnpay_card_type = response_data['card_type']
            order.vnpay_response_code = response_code
            order.vnpay_paid_at = timezone.now()
            order.save()
            
            # Add tracking
            OrderTracking.objects.create(
                order=order,
                status='paid',
                message=f'Thanh toán VNPay thành công (IPN). Mã GD: {response_data["transaction_no"]}',
                created_by=order.user
            )
            
            return JsonResponse({
                'RspCode': '00',
                'Message': 'Success'
            })
        else:
            # Payment failed
            order.payment_status = 'failed'
            order.vnpay_response_code = response_code
            order.save()
            
            return JsonResponse({
                'RspCode': '00',
                'Message': 'Success'
            })
