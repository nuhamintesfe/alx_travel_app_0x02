import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Payment
import uuid

@api_view(['POST'])
def initiate_payment(request):
    data = request.data
    booking_ref = data.get('booking_reference')
    amount = data.get('amount')

    transaction_id = str(uuid.uuid4())
    callback_url = "http://yourdomain.com/api/verify-payment/"  # Replace accordingly

    chapa_payload = {
        "amount": amount,
        "currency": "ETB",
        "email": "test@example.com",
        "tx_ref": transaction_id,
        "return_url": callback_url,
        "callback_url": callback_url,
        "customization[title]": "Travel Payment",
    }

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
    }

    response = requests.post('https://api.chapa.co/v1/transaction/initialize', json=chapa_payload, headers=headers)

    if response.status_code == 200:
        Payment.objects.create(
            booking_reference=booking_ref,
            amount=amount,
            transaction_id=transaction_id,
            status="Pending"
        )
        return Response(response.json())
    return Response({"error": "Failed to initiate payment"}, status=400)
@api_view(['GET'])
def verify_payment(request):
    tx_ref = request.GET.get('tx_ref')

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
    }

    verify_url = f'https://api.chapa.co/v1/transaction/verify/{tx_ref}'
    response = requests.get(verify_url, headers=headers)
    data = response.json()

    if data.get('status') == 'success':
        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
            payment.status = "Completed"
            payment.save()
            return Response({"status": "Payment successful"})
        except Payment.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=404)
    else:
        return Response({"status": "Payment failed"})

