import json
import requests
from django.conf import settings


def generate_sslcommerz_payment(order, request):
    
    post_Data ={
        'store_id': settings.SSLCOMMERZ_STORE_ID,
        'store_passwd': settings.SSLCOMMERZ_STORE_PASSWORD,
        'total_amount': float(order.get_total_cost()),
        'currency': 'BDT',
        'tran_id': str(order.id),
        'success_url': request.build_absolute_uri(f'/payment/success/{order.id}/'),
        'fail_url': request.build_absolute_uri(f'/payment/fail/{order.id}/'),
        'cancel_url': request.build_absolute_uri(f'/payment/cancel/{order.id}/'),
        # change the customer details as per your requirement
        'cus_name': f"{order.first_name} {order.last_name}",
        'cus_email': order.email,
        'cus_add1': order.address,
        'cus_city': order.city,
        'cus_country': 'Bangladesh',
        'shipping_method': 'NO',
        'product_name': 'Products from your store',
        'product_category': 'General',
        'product_profile': 'general',
    }