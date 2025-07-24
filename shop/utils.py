import json
import requests
from django.conf import settings
from django .template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


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
    
    response = requests.post(settings.SSLCOMMERZ_API_URL, data=post_Data)
    return json.loads(response.text)


def send_order_confirmation_email(order):
    subject = f"Order Confirmation - Order #{order.id}"
    message = render_to_string('shop/order_confirmation_email.html', {
        'order': order,
    })
    to = order.email
    send_mail = EmailMultiAlternatives(subject, '', to=[to])
    send_mail.attach_alternative(message, "text/html")
    send_mail.send()
    
    
    
   