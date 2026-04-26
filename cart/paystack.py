import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class PayStackService:
    """PayStack payment service for Tanzania"""
    
    BASE_URL = 'https://api.paystack.co'
    
    def __init__(self):
        self.secret_key = settings.PAYSTACK_SECRET_KEY
        self.public_key = settings.PAYSTACK_PUBLIC_KEY
    
    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json'
        }
    
    def initialize_transaction(self, email, amount, reference, callback_url, metadata=None):
        """
        Initialize a PayStack transaction
        amount should be in kobo (smallest currency unit)
        """
        try:
            url = f'{self.BASE_URL}/transaction/initialize'
            payload = {
                'email': email,
                'amount': int(amount * 100),  # Convert to kobo
                'reference': reference,
                'callback_url': callback_url,
                'currency': 'TZS',
                'metadata': metadata or {}
            }
            
            response = requests.post(url, json=payload, headers=self._get_headers(), timeout=30)
            data = response.json()
            
            if data.get('status'):
                return {
                    'success': True,
                    'authorization_url': data['data']['authorization_url'],
                    'reference': data['data']['reference']
                }
            else:
                logger.error(f"PayStack initialization failed: {data}")
                return {
                    'success': False,
                    'message': data.get('message', 'Payment initialization failed')
                }
        except requests.RequestException as e:
            logger.error(f"PayStack API error: {str(e)}")
            return {
                'success': False,
                'message': 'Unable to connect to payment server'
            }
    
    def verify_transaction(self, reference):
        """Verify a PayStack transaction"""
        try:
            url = f'{self.BASE_URL}/transaction/verify/{reference}'
            response = requests.get(url, headers=self._get_headers(), timeout=30)
            data = response.json()
            
            if data.get('status') and data['data']['status'] == 'success':
                return {
                    'success': True,
                    'amount': data['data']['amount'] / 100,  # Convert from kobo
                    'currency': data['data']['currency'],
                    'reference': data['data']['reference'],
                    'status': data['data']['status']
                }
            else:
                return {
                    'success': False,
                    'message': data.get('message', 'Transaction verification failed')
                }
        except requests.RequestException as e:
            logger.error(f"PayStack verification error: {str(e)}")
            return {
                'success': False,
                'message': 'Unable to verify payment'
            }


def get_paystack_service():
    """Get PayStack service instance"""
    return PayStackService()
