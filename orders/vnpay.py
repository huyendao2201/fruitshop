"""
VNPay Payment Gateway Integration
Based on: https://sandbox.vnpayment.vn/apis/docs/thanh-toan-pay/pay.html
"""

import hashlib
import hmac
import urllib.parse
from datetime import datetime
from django.conf import settings


class VNPay:
    """VNPay Payment Gateway Handler"""
    
    def __init__(self):
        self.vnp_url = settings.VNPAY_PAYMENT_URL
        self.vnp_return_url = settings.VNPAY_RETURN_URL
        self.vnp_tmn_code = settings.VNPAY_TMN_CODE
        self.vnp_hash_secret = settings.VNPAY_HASH_SECRET
        self.vnp_api_url = settings.VNPAY_API_URL
        
    def create_payment_url(self, order, request):
        """
        Tạo URL thanh toán VNPay
        
        Args:
            order: Order object
            request: Django request object
            
        Returns:
            str: Payment URL to redirect customer
        """
        # Build VNPay parameters
        vnp_params = {
            'vnp_Version': '2.1.0',
            'vnp_Command': 'pay',
            'vnp_TmnCode': self.vnp_tmn_code,
            'vnp_Amount': int(order.total_amount * 100),  # VNPay requires amount * 100
            'vnp_CurrCode': 'VND',
            'vnp_TxnRef': order.order_number,
            'vnp_OrderInfo': f'Thanh toan don hang {order.order_number}',
            'vnp_OrderType': 'other',
            'vnp_Locale': 'vn',
            'vnp_ReturnUrl': self.vnp_return_url,
            'vnp_IpAddr': self.get_client_ip(request),
            'vnp_CreateDate': datetime.now().strftime('%Y%m%d%H%M%S'),
        }
        
        # Optional: Bank code (if customer selected specific bank)
        bank_code = request.POST.get('bank_code', '')
        if bank_code:
            vnp_params['vnp_BankCode'] = bank_code
        
        # Create secure hash
        vnp_params['vnp_SecureHash'] = self.create_secure_hash(vnp_params)
        
        # Build payment URL
        query_string = urllib.parse.urlencode(vnp_params)
        payment_url = f"{self.vnp_url}?{query_string}"
        
        return payment_url
    
    def create_secure_hash(self, params):
        """
        Tạo secure hash theo chuẩn VNPay (HMAC SHA512)
        
        Args:
            params: Dictionary of parameters
            
        Returns:
            str: Secure hash string
        """
        # Remove vnp_SecureHash if exists
        params_copy = params.copy()
        if 'vnp_SecureHash' in params_copy:
            del params_copy['vnp_SecureHash']
        if 'vnp_SecureHashType' in params_copy:
            del params_copy['vnp_SecureHashType']
        
        # Sort parameters by key
        sorted_params = sorted(params_copy.items())
        
        # Create query string with URL encoding
        query_string = '&'.join([
            f"{key}={urllib.parse.quote_plus(str(value))}" 
            for key, value in sorted_params
        ])
        
        # Create HMAC SHA512 hash
        secure_hash = hmac.new(
            self.vnp_hash_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha512
        ).hexdigest()
        
        return secure_hash
    
    def validate_response(self, params):
        """
        Xác thực phản hồi từ VNPay
        
        Args:
            params: Dictionary of response parameters from VNPay
            
        Returns:
            tuple: (is_valid, response_data)
        """
        # Get secure hash from response
        vnp_secure_hash = params.get('vnp_SecureHash', '')
        
        # Calculate hash from response params
        calculated_hash = self.create_secure_hash(params)
        
        # Validate hash
        is_valid = vnp_secure_hash == calculated_hash
        
        # Parse response data
        response_data = {
            'order_number': params.get('vnp_TxnRef', ''),
            'amount': int(params.get('vnp_Amount', 0)) / 100,  # Convert back to VND
            'response_code': params.get('vnp_ResponseCode', ''),
            'transaction_no': params.get('vnp_TransactionNo', ''),
            'bank_code': params.get('vnp_BankCode', ''),
            'card_type': params.get('vnp_CardType', ''),
            'pay_date': params.get('vnp_PayDate', ''),
            'transaction_status': params.get('vnp_TransactionStatus', ''),
        }
        
        return is_valid, response_data
    
    def get_client_ip(self, request):
        """
        Lấy IP address của client
        
        Args:
            request: Django request object
            
        Returns:
            str: Client IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @staticmethod
    def get_response_message(response_code):
        """
        Lấy thông báo tương ứng với mã phản hồi VNPay
        
        Args:
            response_code: VNPay response code
            
        Returns:
            str: Message in Vietnamese
        """
        messages = {
            '00': 'Giao dịch thành công',
            '07': 'Trừ tiền thành công. Giao dịch bị nghi ngờ (liên quan tới lừa đảo, giao dịch bất thường)',
            '09': 'Giao dịch không thành công do: Thẻ/Tài khoản của khách hàng chưa đăng ký dịch vụ InternetBanking tại ngân hàng',
            '10': 'Giao dịch không thành công do: Khách hàng xác thực thông tin thẻ/tài khoản không đúng quá 3 lần',
            '11': 'Giao dịch không thành công do: Đã hết hạn chờ thanh toán. Xin quý khách vui lòng thực hiện lại giao dịch',
            '12': 'Giao dịch không thành công do: Thẻ/Tài khoản của khách hàng bị khóa',
            '13': 'Giao dịch không thành công do Quý khách nhập sai mật khẩu xác thực giao dịch (OTP)',
            '24': 'Giao dịch không thành công do: Khách hàng hủy giao dịch',
            '51': 'Giao dịch không thành công do: Tài khoản của quý khách không đủ số dư để thực hiện giao dịch',
            '65': 'Giao dịch không thành công do: Tài khoản của Quý khách đã vượt quá hạn mức giao dịch trong ngày',
            '75': 'Ngân hàng thanh toán đang bảo trì',
            '79': 'Giao dịch không thành công do: KH nhập sai mật khẩu thanh toán quá số lần quy định',
            '99': 'Các lỗi khác (lỗi còn lại, không có trong danh sách mã lỗi đã liệt kê)',
        }
        return messages.get(response_code, 'Lỗi không xác định')
    
    @staticmethod
    def get_bank_list():
        """
        Danh sách ngân hàng hỗ trợ VNPay
        
        Returns:
            list: List of bank dictionaries
        """
        return [
            {'code': 'VNPAYQR', 'name': 'Thanh toán quét mã QR'},
            {'code': 'VNBANK', 'name': 'Thẻ ATM - Tài khoản ngân hàng nội địa'},
            {'code': 'INTCARD', 'name': 'Thẻ thanh toán quốc tế'},
            {'code': 'VIETCOMBANK', 'name': 'Ngân hàng TMCP Ngoại Thương Việt Nam'},
            {'code': 'VIETINBANK', 'name': 'Ngân hàng TMCP Công Thương Việt Nam'},
            {'code': 'BIDV', 'name': 'Ngân hàng TMCP Đầu tư và Phát triển Việt Nam'},
            {'code': 'AGRIBANK', 'name': 'Ngân hàng Nông nghiệp và Phát triển Nông thôn Việt Nam'},
            {'code': 'SACOMBANK', 'name': 'Ngân hàng TMCP Sài Gòn Thương Tín'},
            {'code': 'TECHCOMBANK', 'name': 'Ngân hàng TMCP Kỹ Thương Việt Nam'},
            {'code': 'ACB', 'name': 'Ngân hàng TMCP Á Châu'},
            {'code': 'VPBANK', 'name': 'Ngân hàng TMCP Việt Nam Thịnh Vượng'},
            {'code': 'TPBANK', 'name': 'Ngân hàng TMCP Tiên Phong'},
            {'code': 'MBBANK', 'name': 'Ngân hàng TMCP Quân Đội'},
            {'code': 'HDBANK', 'name': 'Ngân hàng TMCP Phát triển Thành phố Hồ Chí Minh'},
            {'code': 'SHBBANK', 'name': 'Ngân hàng TMCP Sài Gòn - Hà Nội'},
        ]

